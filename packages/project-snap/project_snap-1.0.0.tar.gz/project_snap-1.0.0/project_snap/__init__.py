"""
Project Snap - A utility to create Markdown snapshots of project structures for LLMs
"""

__version__ = "1.0.0"

from project_snap.core import ProjectSnapshotTool, find_config_file, create_sample_config

__all__ = ["ProjectSnapshotTool", "find_config_file", "create_sample_config"]
