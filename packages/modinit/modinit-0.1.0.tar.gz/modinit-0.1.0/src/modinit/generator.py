"""
Project generator for the modinit package.

This module contains the core functionality for generating
AI model training project directories with a standardized structure.
"""

import os
import shutil
from pathlib import Path
import datetime

from .utils.file_utils import ensure_directory, copy_template_file, render_template


def create_project(project_name):
    """
    Create a new AI model training project with a standardized structure.
    
    Args:
        project_name (str): Name of the project to create
    
    Returns:
        Path: Path to the created project directory
    
    Raises:
        FileExistsError: If the project directory already exists
        IOError: If there's an error creating the project structure
    """
    # Get the absolute path for the new project
    project_path = Path(os.path.abspath(project_name))
    
    # Check if the directory already exists
    if project_path.exists():
        raise FileExistsError(f"Directory '{project_path}' already exists")
    
    try:
        # Create the project directory
        ensure_directory(project_path)
        
        # Create the main project structure
        create_directory_structure(project_path)
        
        # Create template files
        create_template_files(project_path, project_name)
        
        return project_path
    
    except Exception as e:
        # Clean up if there's an error
        if project_path.exists():
            shutil.rmtree(project_path)
        raise IOError(f"Failed to create project: {str(e)}")


def create_directory_structure(project_path):
    """
    Create the directory structure for the project.
    
    Args:
        project_path (Path): Path to the project directory
    """
    # Create main directories
    directories = [
        "notebooks",
        "src",
        "src/__pycache__",  # Create __pycache__ directory to avoid issues
        "data",
        "data/raw",
        "data/processed",
        "data/interim",
        "configs",
        "tests",
        "tests/__pycache__",  # Create __pycache__ directory to avoid issues
    ]
    
    for directory in directories:
        ensure_directory(project_path / directory)


def create_template_files(project_path, project_name):
    """
    Create template files for the project.
    
    Args:
        project_path (Path): Path to the project directory
        project_name (str): Name of the project
    """
    # Get the package directory
    package_dir = Path(__file__).parent
    templates_dir = package_dir / "templates"
    
    # Variables for template rendering
    template_vars = {
        "project_name": project_name,
        "date": datetime.datetime.now().strftime("%Y-%m-%d"),
        "year": datetime.datetime.now().year,
    }
    
    # Create base files
    create_base_files(project_path, templates_dir, template_vars)
    
    # Create source files
    create_source_files(project_path, templates_dir, template_vars)
    
    # Create notebook files
    create_notebook_files(project_path, templates_dir, template_vars)
    
    # Create config files
    create_config_files(project_path, templates_dir, template_vars)
    
    # Create test files
    create_test_files(project_path, templates_dir, template_vars)


def create_base_files(project_path, templates_dir, template_vars):
    """
    Create base files for the project.
    
    Args:
        project_path (Path): Path to the project directory
        templates_dir (Path): Path to the templates directory
        template_vars (dict): Variables for template rendering
    """
    # Create README.md
    readme_template = templates_dir / "base" / "README.md"
    readme_path = project_path / "README.md"
    render_template(readme_template, readme_path, template_vars)
    
    # Create .gitignore
    gitignore_template = templates_dir / "base" / ".gitignore"
    gitignore_path = project_path / ".gitignore"
    copy_template_file(gitignore_template, gitignore_path)
    
    # Create requirements.txt
    requirements_template = templates_dir / "base" / "requirements.txt"
    requirements_path = project_path / "requirements.txt"
    copy_template_file(requirements_template, requirements_path)
    
    # Create main.py
    main_template = templates_dir / "project" / "main.py"
    main_path = project_path / "main.py"
    render_template(main_template, main_path, template_vars)


def create_source_files(project_path, templates_dir, template_vars):
    """
    Create source files for the project.
    
    Args:
        project_path (Path): Path to the project directory
        templates_dir (Path): Path to the templates directory
        template_vars (dict): Variables for template rendering
    """
    src_path = project_path / "src"
    
    # Create __init__.py
    init_template = templates_dir / "project" / "src" / "__init__.py"
    init_path = src_path / "__init__.py"
    render_template(init_template, init_path, template_vars)
    
    # Create data.py
    data_template = templates_dir / "project" / "src" / "data.py"
    data_path = src_path / "data.py"
    render_template(data_template, data_path, template_vars)
    
    # Create model.py
    model_template = templates_dir / "project" / "src" / "model.py"
    model_path = src_path / "model.py"
    render_template(model_template, model_path, template_vars)
    
    # Create train.py
    train_template = templates_dir / "project" / "src" / "train.py"
    train_path = src_path / "train.py"
    render_template(train_template, train_path, template_vars)
    
    # Create evaluate.py
    evaluate_template = templates_dir / "project" / "src" / "evaluate.py"
    evaluate_path = src_path / "evaluate.py"
    render_template(evaluate_template, evaluate_path, template_vars)
    
    # Create utils.py
    utils_template = templates_dir / "project" / "src" / "utils.py"
    utils_path = src_path / "utils.py"
    render_template(utils_template, utils_path, template_vars)


def create_notebook_files(project_path, templates_dir, template_vars):
    """
    Create notebook files for the project.
    
    Args:
        project_path (Path): Path to the project directory
        templates_dir (Path): Path to the templates directory
        template_vars (dict): Variables for template rendering
    """
    notebooks_path = project_path / "notebooks"
    
    # Create prototype.ipynb
    prototype_template = templates_dir / "project" / "notebooks" / "prototype.ipynb"
    prototype_path = notebooks_path / "prototype.ipynb"
    render_template(prototype_template, prototype_path, template_vars)


def create_config_files(project_path, templates_dir, template_vars):
    """
    Create configuration files for the project.
    
    Args:
        project_path (Path): Path to the project directory
        templates_dir (Path): Path to the templates directory
        template_vars (dict): Variables for template rendering
    """
    configs_path = project_path / "configs"
    
    # Create config.yaml
    config_template = templates_dir / "project" / "configs" / "config.yaml"
    config_path = configs_path / "config.yaml"
    render_template(config_template, config_path, template_vars)


def create_test_files(project_path, templates_dir, template_vars):
    """
    Create test files for the project.
    
    Args:
        project_path (Path): Path to the project directory
        templates_dir (Path): Path to the templates directory
        template_vars (dict): Variables for template rendering
    """
    tests_path = project_path / "tests"
    
    # Create __init__.py
    init_template = templates_dir / "project" / "tests" / "__init__.py"
    init_path = tests_path / "__init__.py"
    render_template(init_template, init_path, template_vars)
    
    # Create test_data.py
    test_data_template = templates_dir / "project" / "tests" / "test_data.py"
    test_data_path = tests_path / "test_data.py"
    render_template(test_data_template, test_data_path, template_vars)
    
    # Create test_model.py
    test_model_template = templates_dir / "project" / "tests" / "test_model.py"
    test_model_path = tests_path / "test_model.py"
    render_template(test_model_template, test_model_path, template_vars)
    
    # Create test_train.py
    test_train_template = templates_dir / "project" / "tests" / "test_train.py"
    test_train_path = tests_path / "test_train.py"
    render_template(test_train_template, test_train_path, template_vars)
