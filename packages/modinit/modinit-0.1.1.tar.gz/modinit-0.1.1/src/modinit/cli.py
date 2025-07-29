"""
Command-line interface for the modinit package.

This module provides the command-line interface for creating
new AI model training project directories with a standardized structure.
"""

import argparse
import os
import sys
from pathlib import Path

from . import __version__
from .generator import create_project


def parse_args(args=None):
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        prog="modinit",
        description="Initialize a new AI model training project with a standardized structure.",
    )
    
    parser.add_argument(
        "project_name",
        help="Name of the project to create"
    )
    
    parser.add_argument(
        "--version",
        action="version",
        version=f"%(prog)s {__version__}"
    )
    
    # Future Additions; commented out for now
    # parser.add_argument(
    #     "--template",
    #     choices=["default", "pytorch", "tensorflow"],
    #     default="default",
    #     help="Template to use for project creation"
    # )
    
    return parser.parse_args(args)


def main(args=None):
    """Main entry point for the CLI."""
    args = parse_args(args)
    
    # Validate project name
    if os.path.exists(args.project_name):
        print(f"Error: Directory '{args.project_name}' already exists.")
        return 1
    
    try:
        # Create the project
        create_project(args.project_name)
        print(f"Successfully created project: {args.project_name}")
        print(f"To get started, navigate to the project directory:")
        print(f"  cd {args.project_name}")
        return 0
    except Exception as e:
        print(f"Error creating project: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
