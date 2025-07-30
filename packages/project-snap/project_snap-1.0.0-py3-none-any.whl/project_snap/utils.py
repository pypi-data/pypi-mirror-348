"""
Utility functions for the Project Snap package.
"""

import os
import sys
from typing import List, Dict, Any, Optional, Set

def get_terminal_size() -> Dict[str, int]:
    """Get the size of the terminal window."""
    try:
        columns, lines = os.get_terminal_size()
        return {"columns": columns, "lines": lines}
    except (AttributeError, OSError):
        return {"columns": 80, "lines": 24}


def format_size(size_in_bytes: int) -> str:
    """Format a size in bytes to a human-readable string."""
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size_in_bytes < 1024 or unit == 'TB':
            return f"{size_in_bytes:.2f} {unit}"
        size_in_bytes /= 1024


def print_progress(current: int, total: int, prefix: str = '', suffix: str = '', length: int = 30) -> None:
    """Print a progress bar to the console."""
    filled_length = int(length * current // total)
    bar = '█' * filled_length + '-' * (length - filled_length)
    
    percent = f"{100 * (current / total):.1f}%" if total > 0 else "0.0%"
        progress_str = f"\r{prefix} |{bar}| {percent} {suffix}"    
    sys.stdout.write(progress_str)
    sys.stdout.flush()    
    if current >= total:
        sys.stdout.write('\n')
        sys.stdout.flush()


def print_project_tree(directory: str, excluded_dirs: Set[str] = None, max_depth: int = 3) -> None:
    """Print a tree representation of the project structure."""
    excluded_dirs = excluded_dirs or set()
    
    def _print_tree(dir_path: str, prefix: str = '', depth: int = 0):
        if depth > max_depth:
            return
            
        try:
            items = list(os.listdir(dir_path))
        except PermissionError:
            print(f"{prefix}├── [Permission denied]")
            return
            
        items.sort(key=lambda x: (not os.path.isdir(os.path.join(dir_path, x)), x.lower()))
                for i, item in enumerate(items):
            item_path = os.path.join(dir_path, item)
            is_last = i == len(items) - 1            

            if is_last:
                print(f"{prefix}└── {item}")
                new_prefix = prefix + "    "
            else:
                print(f"{prefix}├── {item}")
                new_prefix = prefix + "│   "
                
            if os.path.isdir(item_path) and item not in excluded_dirs:
                _print_tree(item_path, new_prefix, depth + 1)
        print(os.path.basename(directory) or directory)
    _print_tree(directory)
