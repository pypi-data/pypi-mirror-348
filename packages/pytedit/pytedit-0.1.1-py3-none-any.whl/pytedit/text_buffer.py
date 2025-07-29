"""
TextBuffer module for PyTEdit.
Manages the text content and cursor position.
"""

import os


class TextBuffer:
    """Manages the text content and cursor position"""
    
    def __init__(self):
        """Initialize a new text buffer"""
        self.lines = ['']
        self.cursor_row = 0
        self.cursor_col = 0
        self.filename = None
        self.modified = False
    
    def insert_char(self, char):
        """
        Insert a character at the current cursor position
        
        Args:
            char (str): The character to insert
        """
        current_line = self.lines[self.cursor_row]
        new_line = current_line[:self.cursor_col] + char + current_line[self.cursor_col:]
        self.lines[self.cursor_row] = new_line
        self.cursor_col += 1
        self.modified = True
    
    def insert_newline(self):
        """Insert a new line at the current cursor position"""
        current_line = self.lines[self.cursor_row]
        self.lines[self.cursor_row] = current_line[:self.cursor_col]
        self.lines.insert(self.cursor_row + 1, current_line[self.cursor_col:])
        self.cursor_row += 1
        self.cursor_col = 0
        self.modified = True
    
    def backspace(self):
        """Delete the character before the cursor"""
        if self.cursor_col > 0:
            # Delete character in current line
            current_line = self.lines[self.cursor_row]
            new_line = current_line[:self.cursor_col-1] + current_line[self.cursor_col:]
            self.lines[self.cursor_row] = new_line
            self.cursor_col -= 1
            self.modified = True
        elif self.cursor_row > 0:
            # Join with previous line
            previous_line = self.lines[self.cursor_row - 1]
            current_line = self.lines[self.cursor_row]
            self.cursor_col = len(previous_line)
            self.lines[self.cursor_row - 1] = previous_line + current_line
            self.lines.pop(self.cursor_row)
            self.cursor_row -= 1
            self.modified = True
    
    def delete(self):
        """Delete the character at the cursor"""
        current_line = self.lines[self.cursor_row]
        if self.cursor_col < len(current_line):
            # Delete character in current line
            new_line = current_line[:self.cursor_col] + current_line[self.cursor_col+1:]
            self.lines[self.cursor_row] = new_line
            self.modified = True
        elif self.cursor_row < len(self.lines) - 1:
            # Join with next line
            next_line = self.lines[self.cursor_row + 1]
            self.lines[self.cursor_row] = current_line + next_line
            self.lines.pop(self.cursor_row + 1)
            self.modified = True
    
    def move_cursor(self, rows=0, cols=0):
        """
        Move the cursor by the specified number of rows and columns
        
        Args:
            rows (int): Number of rows to move (negative for up)
            cols (int): Number of columns to move (negative for left)
        """
        if rows != 0:
            self.cursor_row = max(0, min(len(self.lines) - 1, self.cursor_row + rows))
            # Adjust column if new line is shorter
            self.cursor_col = min(self.cursor_col, len(self.lines[self.cursor_row]))
        
        if cols != 0:
            if cols < 0:
                # Moving left
                if self.cursor_col > 0:
                    self.cursor_col = max(0, self.cursor_col + cols)
                elif self.cursor_row > 0:
                    # Move to end of previous line
                    self.cursor_row -= 1
                    self.cursor_col = len(self.lines[self.cursor_row])
            else:
                # Moving right
                if self.cursor_col < len(self.lines[self.cursor_row]):
                    self.cursor_col = min(len(self.lines[self.cursor_row]), self.cursor_col + cols)
                elif self.cursor_row < len(self.lines) - 1:
                    # Move to beginning of next line
                    self.cursor_row += 1
                    self.cursor_col = 0
    
    def get_text(self):
        """
        Get the entire text content as a string
        
        Returns:
            str: The full text content
        """
        return '\n'.join(self.lines)
    
    def load_file(self, filename):
        """
        Load content from a file
        
        Args:
            filename (str): Path to the file to load
            
        Returns:
            bool: True if file loaded successfully, False otherwise
        """
        try:
            with open(filename, 'r') as f:
                content = f.read()
                self.lines = content.splitlines()
                if not self.lines:
                    self.lines = ['']
                self.filename = filename
                self.cursor_row = 0
                self.cursor_col = 0
                self.modified = False
            return True
        except Exception as e:
            return False
    
    def save_file(self, filename=None):
        """
        Save content to a file
        
        Args:
            filename (str, optional): Path to save the file. If None, uses the current filename.
            
        Returns:
            bool: True if file saved successfully, False otherwise
        """
        save_filename = filename or self.filename
        if not save_filename:
            return False
        
        try:
            with open(save_filename, 'w') as f:
                f.write(self.get_text())
            self.filename = save_filename
            self.modified = False
            return True
        except Exception as e:
            return False