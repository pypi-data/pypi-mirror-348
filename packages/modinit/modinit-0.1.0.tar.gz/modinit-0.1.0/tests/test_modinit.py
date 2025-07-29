"""
Basic tests for the modinit package.

This module contains tests to verify the basic functionality of the modinit package.
"""

import os
import shutil
import tempfile
import unittest
from pathlib import Path

from modinit.cli import main


class TestModinit(unittest.TestCase):
    """Test cases for the modinit package."""
    
    def setUp(self):
        """Set up test fixtures."""
        # Create a temporary directory for testing
        self.test_dir = tempfile.mkdtemp()
        self.old_cwd = os.getcwd()
        os.chdir(self.test_dir)
    
    def tearDown(self):
        """Tear down test fixtures."""
        # Clean up the temporary directory
        os.chdir(self.old_cwd)
        shutil.rmtree(self.test_dir)
    
    def test_project_creation(self):
        """Test that a project can be created."""
        # Call the main function with a project name
        main(["test_project"])
        
        # Check that the project directory was created
        project_dir = Path(self.test_dir) / "test_project"
        self.assertTrue(project_dir.exists())
        
        # Check that key directories and files were created
        self.assertTrue((project_dir / "notebooks").exists())
        self.assertTrue((project_dir / "src").exists())
        self.assertTrue((project_dir / "data").exists())
        self.assertTrue((project_dir / "configs").exists())
        self.assertTrue((project_dir / "tests").exists())
        self.assertTrue((project_dir / "main.py").exists())
        self.assertTrue((project_dir / "requirements.txt").exists())
        self.assertTrue((project_dir / "README.md").exists())
        self.assertTrue((project_dir / ".gitignore").exists())


if __name__ == "__main__":
    unittest.main()
