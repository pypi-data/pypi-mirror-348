"""
File and directory utility functions for the modinit package.

This module provides utility functions for file and directory operations
used in the project generation process.
"""

import os
import shutil
from pathlib import Path
import string


def ensure_directory(path):
    """
    Ensure a directory exists, creating it if necessary.
    
    Args:
        path (Path or str): Path to the directory
    
    Returns:
        Path: Path to the created directory
    """
    path = Path(path)
    path.mkdir(parents=True, exist_ok=True)
    return path


def copy_template_file(src, dst):
    """
    Copy a template file to the destination.
    
    Args:
        src (Path or str): Source file path
        dst (Path or str): Destination file path
    
    Raises:
        FileNotFoundError: If the source file doesn't exist
    """
    src = Path(src)
    dst = Path(dst)
    
    if not src.exists():
        raise FileNotFoundError(f"Template file not found: {src}")
    
    shutil.copy2(src, dst)


def render_template(src, dst, variables):
    """
    Render a template file with the given variables and write to destination.
    
    Args:
        src (Path or str): Source template file path
        dst (Path or str): Destination file path
        variables (dict): Variables for template rendering
    
    Raises:
        FileNotFoundError: If the source file doesn't exist
        KeyError: If a required variable is missing
    """
    src = Path(src)
    dst = Path(dst)
    
    if not src.exists():
        raise FileNotFoundError(f"Template file not found: {src}")
    
    # Read the template content
    with open(src, 'r', encoding='utf-8') as f:
        template_content = f.read()
    
    # Render the template using string.Template
    template = string.Template(template_content)
    try:
        rendered_content = template.substitute(variables)
    except KeyError as e:
        raise KeyError(f"Missing template variable: {e}")
    
    # Write the rendered content to the destination
    with open(dst, 'w', encoding='utf-8') as f:
        f.write(rendered_content)
