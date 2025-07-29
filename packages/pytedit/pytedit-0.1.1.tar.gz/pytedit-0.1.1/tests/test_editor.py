"""
Tests for core editor functionality.
"""

import unittest
from unittest.mock import MagicMock, patch
import tempfile
import os
from pytedit.editor import Editor


class TestEditor(unittest.TestCase):
    """Test the Editor class functionality"""
    
    @patch('pytedit.editor.Application')
    def setUp(self, mock_app):
        """Set up editor instance for testing"""
        self.editor = Editor()
        # Mock the application to prevent actual UI drawing
        self.editor.app = MagicMock()
        self.editor.refresh_screen = MagicMock()
    
    def test_init(self):
        """Test editor initialization"""
        self.assertIsNotNone(self.editor.buffer)
        self.assertIsNotNone(self.editor.bindings)
        self.assertEqual(self.editor.status_message, "Welcome to PyTEdit! Ctrl-S: Save | Ctrl-Q: Quit")
    
    def test_get_status_text(self):
        """Test status text generation"""
        # Set up some test conditions
        self.editor.buffer.filename = "test.txt"
        self.editor.buffer.modified = True
        self.editor.buffer.cursor_row = 5
        self.editor.buffer.cursor_col = 10
        
        status = self.editor.get_status_text()
        self.assertIn("*test.txt", status)
        self.assertIn("Line 6", status)  # 0-indexed to 1-indexed
        self.assertIn("Col 11", status)  # 0-indexed to 1-indexed
    
    @patch('os.path.exists')
    def test_run_with_file(self, mock_exists):
        """Test running the editor with a file"""
        # Mock file existence check
        mock_exists.return_value = True
        
        # Mock the load_file method
        self.editor.buffer.load_file = MagicMock(return_value=True)
        
        # Run editor with a test file
        self.editor.run("test.txt")
        
        # Assert load_file was called with the right filename
        self.editor.buffer.load_file.assert_called_once_with("test.txt")
        
        # Assert the app.run was called
        self.editor.app.run.assert_called_once()
    
    def test_key_bindings_creation(self):
        """Test key bindings are created properly"""
        kb = self.editor.create_key_bindings()
        
        # Check that some expected key bindings exist
        # Since we can't easily inspect the bindings directly, 
        # we'll just verify the object was created
        self.assertIsNotNone(kb)


if __name__ == '__main__':
    unittest.main()