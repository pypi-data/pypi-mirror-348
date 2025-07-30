#!/usr/bin/env python3

from project_snap.core import ProjectSnapshotTool, find_config_file, create_sample_config
import argparse
import sys


def main():
    """Main entry point for the command-line tool."""
    parser = argparse.ArgumentParser(description='Generate a project snapshot in markdown format')
    parser.add_argument('-c', '--config', help='Path to configuration file')
    parser.add_argument('-o', '--output', help='Output file name')
    parser.add_argument('-t', '--target', help='Target directory to snapshot')
    parser.add_argument('--init', action='store_true', help='Create a sample configuration file')
    parser.add_argument('-v', '--version', action='store_true', help='Show version information')
    
    args = parser.parse_args()
    
    if args.version:
        print("Project Snapshot Tool v1.0.0")
        return
        
    if args.init:
        create_sample_config()
        return
    
    # Find config file if not specified
    config_path = args.config or find_config_file()
    
    # Create tool instance
    tool = ProjectSnapshotTool(config_path)
    
    # Override config with command line arguments
    if args.output:
        tool.snapshot_path = Path(args.output).absolute()
        
    if args.target:
        tool.target_folder = Path(args.target).absolute()
    
    # Run the snapshot
    tool.create_snapshot()
    tool.print_stats()


if __name__ == "__main__":
    main()
