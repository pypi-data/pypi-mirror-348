#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
A library for extracting and preparing code and text snippets from various file types,
primarily intended for consumption by Large Language Models (LLMs).

This module allows sourcing content from individual files, directories, or Python packages,
and provides mechanisms for filtering and specific parsing based on file extensions
(e.g., special handling for .ipynb files).
"""

import importlib
import importlib.util
import json
import os
import re
import site
import sys
from pathlib import Path
from typing import (
    Dict,
    List,
    Literal,
    NamedTuple,
    Optional,
    Sequence,
    Set,
    Tuple,
    Union,
    cast,
)

# Type alias for notebook cell content types
NotebookContent = Literal["code", "markdown"]

# Type alias for the file tree structure
# A non-None FileTree is a dictionary mapping names to either None (file) or another FileTree (directory)
FileTree = Dict[str, Optional["FileTree"]]

# Constants
DEFAULT_GLOB_PATTERNS: Sequence[str] = ("*.py", "*.ipynb", "*.md", "*.txt", "*.rst")
"""Default glob patterns to match files if none are specified."""


class TextSnippets(NamedTuple):
    """
    Represents code / text snippets extracted from files.

    Contains paths to the files, concatenated text of all snippets,
    and the base directory of the files.
    """

    paths: List[Path]
    snippets_text: str
    base_dir: Path

    @classmethod
    def from_path_or_pkgname(
        cls,
        path_or_pkgname: str,
        glob_patterns: Union[str, Sequence[str]] = DEFAULT_GLOB_PATTERNS,
        case_sensitive: bool = False,
        ban_file_patterns: Optional[Sequence[str]] = None,
        parse_ipynb_cells: Union[
            NotebookContent, Sequence[NotebookContent]
        ] = "code",  # "code", "markdown", or ["code", "markdown"]
    ):
        """
        Creates a CodeSnippets instance from a file path, directory, or package name.

        Args:
            path_or_pkgname: Path to a file/directory or a Python package name.
            glob_patterns: Pattern(s) to match files (e.g., "*.py", ["**/*.py", "*.ipynb"]).
                           Defaults to `DEFAULT_GLOB_PATTERNS`.
            case_sensitive: Whether glob pattern matching should be case-sensitive.
            ban_file_patterns: Optional list of fnmatch-style patterns to exclude files.
                               These patterns are matched against the full POSIX path.
            parse_ipynb_cells: Specifies which cell types to extract from .ipynb files.
                               Can be "code", "markdown", or a list like ["code", "markdown"].
                               Defaults to "code".

        Returns:
            A new CodeSnippets instance with extracted code snippets.

        Raises:
            ValueError: If path_or_pkgname is not found or invalid.
        """
        if isinstance(parse_ipynb_cells, str):
            parse_ipynb_cells = [parse_ipynb_cells]
        return cls(
            paths=(
                found_paths := _get_filepaths(
                    path_or_pkgname=path_or_pkgname,
                    glob_patterns=glob_patterns,
                    case_sensitive=case_sensitive,
                    ban_file_patterns=ban_file_patterns,
                )
            ),
            snippets_text="".join(
                _create_formatted_snippet(file_path=p, ipynb_cells_to_include=parse_ipynb_cells) for p in found_paths
            ),
            base_dir=_get_base_dir(found_paths),
        )

    @property
    def metadata(self) -> str:
        """
        Generates metadata about the code snippets.

        Returns a string containing information about the file tree structure,
        total number of files, and the base directory.
        The file tree is displayed in a hierarchical format.

        Returns:
            str: Formatted metadata string.
        """
        if not self.paths:
            return f"Base directory: {self.base_dir.as_posix()}\n- Total files: 0"

        results: List[str] = [f"Base directory: {self.base_dir.as_posix()}"]
        file_tree: FileTree = {}

        def ensure_directory(tree: FileTree, path_parts: Sequence[str]) -> FileTree:
            current = tree
            for part in path_parts:
                if part not in current or current[part] is None:
                    current[part] = {}
                current = cast(FileTree, current[part])
            return current

        for file_path in sorted(self.paths):
            try:
                rel_path = file_path.relative_to(self.base_dir)
            except ValueError:
                # Fallback if path is not relative to base_dir (should be rare)
                rel_path = Path(file_path.name)

            *dir_parts, file_name = rel_path.parts

            if dir_parts:
                parent_dir = ensure_directory(file_tree, dir_parts)
                parent_dir[file_name] = None
            else:
                file_tree[file_name] = None

        def _display_tree(tree: FileTree, prefix: str = "") -> None:
            items: List[Tuple[str, Optional[FileTree]]] = sorted(tree.items())
            count: int = len(items)
            for idx, (name, subtree) in enumerate(items):
                branch: str = "└── " if idx == count - 1 else "├── "
                results.append(f"{prefix}{branch}{name}")
                if subtree is not None:
                    extension: str = "    " if idx == count - 1 else "│   "
                    _display_tree(tree=subtree, prefix=prefix + extension)

        _display_tree(file_tree)
        results.append(f"- Total files: {len(self.paths)}")
        return "\n".join(results)


def _pattern_to_regex_str(pattern: str) -> str:
    """
    Converts an fnmatch-style pattern to a regex string.
    '**' matches any characters including '/',
    '*' matches any characters except '/',
    '?' matches any single character except '/'.
    The pattern is anchored to match the entire string.
    """
    escaped_pattern = re.escape(pattern)
    regex_str = escaped_pattern.replace(r"\*\*", ".*")
    regex_str = regex_str.replace(r"\*", r"[^/]*")
    regex_str = regex_str.replace(r"\?", r"[^/]")
    return "^" + regex_str + "$"


def _is_path_banned(
    path_to_check: Path,
    ban_patterns: Sequence[str],
    case_sensitive: bool,
) -> bool:
    """
    Checks if a given path matches any of the ban patterns.
    Ban patterns are matched against the full POSIX path.
    """
    path_str = path_to_check.as_posix()
    for pattern_str in ban_patterns:
        regex_str = _pattern_to_regex_str(pattern_str)
        flags = 0 if case_sensitive else re.IGNORECASE
        try:
            compiled_regex = re.compile(regex_str, flags)
            if compiled_regex.match(path_str):
                return True
        except re.error:
            # Malformed regex pattern, could log this.
            # print(f"Warning: Invalid regex from ban pattern '{pattern_str}'. Skipping.")
            pass
    return False


def _is_path_relative_to(path: Path, other: Path) -> bool:
    """Compatibility wrapper for Path.is_relative_to (Python 3.9+)."""
    if sys.version_info >= (3, 9):
        return path.is_relative_to(other)  # type: ignore[attr-defined]
    else:
        try:
            path.relative_to(other)
            return True
        except ValueError:
            return False


def _parse_ipynb_content(file_path: Path, cells_to_include: Sequence[NotebookContent]) -> str:
    """
    Parses an .ipynb file and extracts content from specified cell types.

    Args:
        file_path: Path to the .ipynb file.
        cells_to_include: A list of cell types (e.g., ["code", "markdown"]) to extract.

    Returns:
        A string containing the concatenated content of the specified cells.
        Returns an error message string if parsing fails.
    """
    try:
        with file_path.open("r", encoding="utf-8") as f:
            notebook_content = json.load(f)
    except (json.JSONDecodeError, OSError, UnicodeDecodeError) as e:
        return f"[Error reading or parsing IPYNB file {file_path.name}: {e}]"

    extracted_parts: List[str] = []
    if "cells" not in notebook_content or not isinstance(notebook_content["cells"], list):
        return f"[Error: IPYNB file {file_path.name} has no 'cells' list or it's malformed]"

    for i, cell in enumerate(notebook_content["cells"]):
        if isinstance(cell, dict) and "cell_type" in cell and "source" in cell:
            cell_type = cell["cell_type"]
            source = cell["source"]
            if cell_type in cells_to_include:
                header = f"# --- Cell {i + 1} ({cell_type}) ---"
                if isinstance(source, list):
                    extracted_parts.append(f"{header}\n{''.join(source)}")
                elif isinstance(source, str):
                    extracted_parts.append(f"{header}\n{source}")
    return "\n\n".join(extracted_parts)


def _extract_content_from_file(file_path: Path, ipynb_cells_to_include: Sequence[NotebookContent] = ("code",)) -> str:
    """
    Extracts content from a file, with special handling for .ipynb files.

    Args:
        file_path: The path to the file.
        ipynb_cells_to_include: Cell types to parse from .ipynb files.

    Returns:
        The extracted content as a string.
    """
    if not file_path.is_file():
        return ""  # Should not happen if _get_filepaths works correctly

    try:
        file_suffix = file_path.suffix.lower()

        if file_suffix == ".ipynb":
            return _parse_ipynb_content(file_path, ipynb_cells_to_include)
        else:
            # For .py, .txt, .md, .rst, etc., read as plain text
            return file_path.read_text(encoding="utf-8")

    except Exception as e:
        # Broad except to catch any unexpected errors during file processing
        # print(f"Warning: Could not read or process file {file_path}: {e}")
        return f"[Error processing file {file_path.name}: {e}]"


def _create_formatted_snippet(file_path: Path, ipynb_cells_to_include: Sequence[NotebookContent]) -> str:
    """
    Reads a file, extracts its content based on type, and formats it
    with a path header.
    """
    extracted_content = _extract_content_from_file(file_path, ipynb_cells_to_include)

    # Determine the display path (relative to site-packages, cwd, or absolute)
    display_path_obj: Path
    site_package_match_path: Optional[Path] = None

    resolved_file_path = file_path.resolve()

    # site.getsitepackages() can return paths that need resolution (e.g. symlinks)
    # We want the most specific site-packages directory that contains the file_path.
    # Sort by length descending to check more specific paths first.
    sorted_site_paths = sorted(
        (Path(d).resolve() for d in site.getsitepackages()), key=lambda p: len(str(p)), reverse=True
    )

    for sp_path in sorted_site_paths:
        if _is_path_relative_to(resolved_file_path, sp_path):
            site_package_match_path = sp_path
            break

    try:
        current_working_dir = Path.cwd().resolve()
    except OSError:  # cwd might not be accessible
        current_working_dir = None

    if site_package_match_path:
        display_path_obj = resolved_file_path.relative_to(site_package_match_path)
        # Prepend with a marker if it's from site-packages for clarity
        display_path_obj = Path("site-packages") / display_path_obj
    elif current_working_dir and _is_path_relative_to(resolved_file_path, current_working_dir):
        display_path_obj = resolved_file_path.relative_to(current_working_dir)
    else:
        display_path_obj = resolved_file_path  # Fallback to absolute path

    return f"```[{display_path_obj.as_posix()}]\n{extracted_content.strip()}\n```\n\n"


def _get_base_dir(target_files: Sequence[Path]) -> Path:
    """
    Determines the common base directory for a sequence of file paths.
    """
    if not target_files:
        try:
            return Path.cwd()
        except OSError:
            return Path(".").resolve()

    resolved_path_strs = [str(p.resolve()) for p in target_files]
    common_prefix_str = os.path.commonpath(resolved_path_strs)

    if not common_prefix_str:
        return Path(target_files[0].resolve().anchor)

    common_path = Path(common_prefix_str)

    # If common_path is one of the files, its parent is the base.
    # Check if common_path itself is a file that exists, or if it doesn't exist but has a suffix
    # and matches one of the resolved target file paths exactly.
    if common_path.exists():
        if common_path.is_file():
            return common_path.parent
    elif common_path.suffix:  # Doesn't exist, but has a suffix (likely a file path)
        if any(common_path == Path(p_str) for p_str in resolved_path_strs):
            return common_path.parent
    return common_path


def _get_filepaths(
    path_or_pkgname: str,
    glob_patterns: Union[str, Sequence[str]],
    case_sensitive: bool,
    ban_file_patterns: Optional[Sequence[str]],
) -> List[Path]:
    """
    Gets paths to files from a directory, file, or Python package name.
    Filters them using glob patterns and ban patterns.
    """
    input_path_obj = Path(path_or_pkgname)
    glob_patterns_list: Sequence[str] = [glob_patterns] if isinstance(glob_patterns, str) else glob_patterns
    candidate_files: Set[Path] = set()

    is_input_path_resolved = False

    if input_path_obj.is_file():
        candidate_files.add(input_path_obj.resolve())
        is_input_path_resolved = True
    elif input_path_obj.is_dir():
        for item in input_path_obj.rglob("*"):
            if item.is_file():
                candidate_files.add(item.resolve())
        is_input_path_resolved = True
    else:  # Assume it's a package or module name
        try:
            spec = importlib.util.find_spec(path_or_pkgname)
            if spec is None:
                # If spec is not found, it might still be a path that doesn't exist yet.
                # The later check will handle this.
                pass  # Keep going to see if it's a non-existent path.
            elif spec.submodule_search_locations:  # It's a package
                for loc_str in spec.submodule_search_locations:
                    loc_path = Path(loc_str).resolve()
                    init_file = loc_path / "__init__.py"
                    if init_file.is_file():  # Ensure __init__.py is considered for glob
                        candidate_files.add(init_file)
                    for item in loc_path.rglob("*"):
                        if item.is_file():
                            candidate_files.add(item.resolve())
                is_input_path_resolved = True  # Package was found
            elif spec.origin:  # It's a single-file module
                module_file_path = Path(spec.origin).resolve()
                if module_file_path.is_file():
                    candidate_files.add(module_file_path)
                is_input_path_resolved = True  # Module was found
            # If spec was found but no files (e.g. namespace package), is_input_path_resolved remains true
            if spec is not None:  # If find_spec returned something, we consider the name "resolved"
                is_input_path_resolved = True

        except ImportError:
            # This can happen if path_or_pkgname is not a valid module name.
            # We'll let the path existence check below handle it.
            pass
        except Exception as e:
            raise ValueError(f"Unexpected error processing '{path_or_pkgname}' as a package/module: {e}")

    if not candidate_files and not is_input_path_resolved and not input_path_obj.exists():
        raise ValueError(
            f"Input '{path_or_pkgname}' does not exist as a file/directory "
            f"and could not be resolved as a Python package/module."
        )
    if not candidate_files and is_input_path_resolved and not input_path_obj.exists():
        # This means it was a package/module but no files were found within it (e.g. empty package)
        # or no files after initial rglob. This is not an error itself, glob filtering will handle it.
        pass

    matched_by_glob: List[Path] = []
    if not glob_patterns_list:  # If glob_patterns is empty, match nothing.
        return []

    for cf_path in candidate_files:
        for g_pattern in glob_patterns_list:
            is_path_pattern = "/" in g_pattern or "**" in g_pattern
            path_str_for_glob = cf_path.as_posix() if is_path_pattern else cf_path.name
            regex_str = _pattern_to_regex_str(g_pattern)
            flags = 0 if case_sensitive else re.IGNORECASE
            try:
                compiled_regex = re.compile(regex_str, flags)
                if compiled_regex.match(path_str_for_glob):
                    matched_by_glob.append(cf_path)
                    break
            except re.error:
                # print(f"Warning: Invalid regex from glob pattern '{g_pattern}'. Skipping.")
                pass

    final_paths: List[Path]
    if ban_file_patterns:
        final_paths = [p for p in matched_by_glob if not _is_path_banned(p, ban_file_patterns, case_sensitive)]
    else:
        final_paths = matched_by_glob

    # If after all processing, no files are selected, but the original input was valid
    # and might have simply not matched any globs.
    if not final_paths and is_input_path_resolved and not input_path_obj.exists():
        # This condition means input was a package/module, it was resolved,
        # but no files matched glob/ban patterns. Return empty list.
        return []
    elif not final_paths and input_path_obj.exists() and not any(glob_patterns_list):
        # Input was a file/dir, but no glob patterns were specified (or empty list)
        return []
    elif not final_paths and (input_path_obj.is_dir() or (input_path_obj.is_file() and not any(glob_patterns_list))):
        # Input was a dir with no matching files, or a single file that didn't match any glob
        # (unless glob_patterns was empty, then it should have been included if it existed)
        # This path is subtle: if input is a file, and glob_patterns are specific and don't match, it's fine.
        # The ValueError at the start should catch truly non-existent paths.
        pass

    return sorted(list(set(final_paths)))


# Example Usage (comment out for library distribution)
# if __name__ == "__main__":
#     import shutil
#
#     # Setup a temporary test directory
#     test_dir_name = "temp_llm_text_source_test"
#     test_dir = Path(test_dir_name)
#     if test_dir.exists():
#         shutil.rmtree(test_dir)
#     test_dir.mkdir(parents=True, exist_ok=True)
#
#     sub_dir = test_dir / "subdir"
#     sub_dir.mkdir()
#
#     # Create dummy files
#     (test_dir / "file1.py").write_text("print('Hello from file1.py')\n# Python comment")
#     (test_dir / "FILE2.PY").write_text("print('Hello from FILE2.PY')") # For case sensitivity test
#     (sub_dir / "file3.py").write_text("def my_func():\n    pass # In subdir")
#     (test_dir / "doc.md").write_text("# Markdown Title\nSome text.")
#     (test_dir / "notes.txt").write_text("Simple text file.")
#     (test_dir / "banned_file.py").write_text("# This should be banned")
#     (test_dir / "other.dat").write_text("Binary data or other format")
#
#     # Create a dummy .ipynb file
#     dummy_ipynb_content = {
#         "cells": [
#             {"cell_type": "code", "source": ["print('Hello from ipynb code cell')"], "metadata": {}, "outputs": [], "execution_count": 1},
#             {"cell_type": "markdown", "source": ["This is **markdown** in *ipynb*."], "metadata": {}},
#             {"cell_type": "raw", "source": ["Raw cell content"], "metadata": {}},
#             {"cell_type": "code", "source": "import os\nos.getcwd()", "metadata": {}, "outputs": [], "execution_count": 2}
#         ],
#         "metadata": {}, "nbformat": 4, "nbformat_minor": 2
#     }
#     (test_dir / "notebook.ipynb").write_text(json.dumps(dummy_ipynb_content, indent=2))
#     (sub_dir / "another.ipynb").write_text(json.dumps({ # Simpler one
#         "cells": [{"cell_type": "code", "source": ["print(1+1)"]}], "metadata": {}, "nbformat": 4, "nbformat_minor": 2
#     }))
#
#     print(f"--- Testing with local directory: '{test_dir_name}' ---")
#     try:
#         snippets_all = CodeSnippets.from_path_or_pkgname(
#             test_dir_name,
#             glob_patterns=["**/*.py", "*.md", "*.txt", "**/*.ipynb"], # Recursive for py and ipynb
#             parse_ipynb_cells=["code", "markdown"]
#         )
#         print("\n[All Files (py, md, txt, ipynb - code & markdown cells)]")
#         print(snippets_all.metadata)
#         # print(snippets_all.snippets_text) # Can be verbose
#         assert len(snippets_all.paths) == 7 # file1.py, FILE2.PY, subdir/file3.py, doc.md, notes.txt, notebook.ipynb, subdir/another.ipynb
#
#         snippets_dir_cs_false = CodeSnippets.from_path_or_pkgname(
#             test_dir_name,
#             glob_patterns="*.py", # Only .py in top level
#             case_sensitive=False,
#             ban_file_patterns=[f"{test_dir_name}/banned_file.py"] # ban uses full path pattern
#         )
#         print("\n[Case Insensitive (*.py in top, banned 'banned_file.py')]")
#         print(snippets_dir_cs_false.metadata)
#         # print(snippets_dir_cs_false.snippets_text)
#         # Expected: file1.py, FILE2.PY (banned_file.py is excluded)
#         assert len(snippets_dir_cs_false.paths) == 2
#         assert not any("banned_file.py" in p.name for p in snippets_dir_cs_false.paths)
#
#         snippets_dir_cs_true = CodeSnippets.from_path_or_pkgname(
#             test_dir_name,
#             glob_patterns="*.py", # Only .py in top level
#             case_sensitive=True
#         )
#         print("\n[Case Sensitive (*.py in top)]")
#         print(snippets_dir_cs_true.metadata)
#         # Expected: file1.py (FILE2.PY is excluded due to case)
#         assert len(snippets_dir_cs_true.paths) == 1
#         assert "file1.py" in snippets_dir_cs_true.paths[0].name
#
#         snippets_ipynb_code_only = CodeSnippets.from_path_or_pkgname(
#             test_dir_name,
#             glob_patterns="**/*.ipynb",
#             parse_ipynb_cells="code" # Default, but explicit
#         )
#         print("\n[IPYNB files, only code cells]")
#         print(snippets_ipynb_code_only.metadata)
#         # print(snippets_ipynb_code_only.snippets_text)
#         assert len(snippets_ipynb_code_only.paths) == 2
#         assert "markdown" not in snippets_ipynb_code_only.snippets_text.lower()
#         assert "raw cell content" not in snippets_ipynb_code_only.snippets_text.lower()
#         assert "print('Hello from ipynb code cell')" in snippets_ipynb_code_only.snippets_text
#         assert "os.getcwd()" in snippets_ipynb_code_only.snippets_text
#
#     except ValueError as e:
#         print(f"Error during directory test: {e}")
#     except Exception as e:
#         print(f"An unexpected error occurred: {e}")
#         import traceback
#         traceback.print_exc()
#
#     # Test with a standard library package (e.g., 'json')
#     try:
#         print("\n--- Testing with 'json' package (standard library) ---")
#         # We only expect .py files from stdlib packages typically.
#         snippets_pkg = CodeSnippets.from_path_or_pkgname("json", glob_patterns="*.py")
#         print(snippets_pkg.metadata)
#         # print(snippets_pkg.snippets_text) # This might be very long
#         print(f"Number of Python snippets found in 'json': {len(snippets_pkg.paths)}")
#         if snippets_pkg.paths:
#             print(f"First file from 'json' package: {snippets_pkg.paths[0]}")
#         assert len(snippets_pkg.paths) > 0 # 'json' package should have .py files
#
#     except ValueError as e:
#         print(f"Error during package test: {e}")
#     except Exception as e:
#         print(f"An unexpected error occurred: {e}")
#
#     # Test with a single file
#     single_file_path = test_dir / "single_test_file.py"
#     try:
#         print("\n--- Testing with a single file ---")
#         single_file_path.write_text("def my_single_func():\n    pass")
#         snippets_file = CodeSnippets.from_path_or_pkgname(str(single_file_path))
#         print(snippets_file.metadata)
#         # print(snippets_file.snippets_text)
#         assert len(snippets_file.paths) == 1
#     except ValueError as e:
#         print(f"Error during single file test: {e}")
#
#     # Test non-existent path
#     try:
#         print("\n--- Testing with non-existent path ---")
#         CodeSnippets.from_path_or_pkgname("non_existent_path_for_sure_123")
#     except ValueError as e:
#         print(f"Successfully caught error for non-existent path: {e}")
#         assert "does not exist" in str(e) or "could not be resolved" in str(e)
#
#     # Test empty directory
#     empty_dir = test_dir / "empty_subdir"
#     empty_dir.mkdir()
#     try:
#         print("\n--- Testing with an empty directory ---")
#         snippets_empty = CodeSnippets.from_path_or_pkgname(str(empty_dir))
#         print(snippets_empty.metadata)
#         assert len(snippets_empty.paths) == 0
#     except ValueError as e:
#         print(f"Error with empty directory: {e}") # Should not error, just find 0 files
#
#
#     # Clean up
#     # print(f"\nCleaning up test directory: {test_dir_name}")
#     # shutil.rmtree(test_dir)
#     pass
