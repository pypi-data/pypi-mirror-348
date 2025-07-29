"""
Utility functions module.

This module contains various helper functions used throughout the project.
"""

import os
import random
import logging
from pathlib import Path


def setup_logging(log_dir="logs", level=logging.INFO):
    """
    Set up logging configuration.
    
    Args:
        log_dir (str): Directory to save log files
        level: Logging level
        
    Returns:
        Logger instance
    """
    # Ensure log directory exists
    os.makedirs(log_dir, exist_ok=True)
    
    # Configure logging
    log_file = os.path.join(log_dir, "training.log")
    
    # This is a placeholder implementation
    # In a real project, you would:
    # 1. Configure file and console handlers
    # 2. Set formatting
    # 3. Set log levels
    
    logger = logging.getLogger("${project_name}")
    logger.setLevel(level)
    
    return logger


def set_seed(seed=42):
    """
    Set random seed for reproducibility.
    
    Args:
        seed (int): Random seed
    """
    random.seed(seed)
    # In a real project, you would also set seeds for:
    # 1. numpy
    # 2. torch
    # 3. tensorflow
    # 4. etc.
    
    print(f"Random seed set to {seed}")


def load_config(config_path):
    """
    Load configuration from a file.
    
    Args:
        config_path (str): Path to configuration file
        
    Returns:
        dict: Configuration parameters
    """
    print(f"Loading configuration from {config_path}")
    
    # This is a placeholder implementation
    # In a real project, you would:
    # 1. Read the config file (YAML, JSON, etc.)
    # 2. Parse into a dictionary
    # 3. Validate configuration
    
    # Placeholder config
    config = {
        "data": {
            "batch_size": 32
        },
        "model": {
            "hidden_size": 128
        },
        "training": {
            "epochs": 100,
            "learning_rate": 0.001
        }
    }
    
    return config
