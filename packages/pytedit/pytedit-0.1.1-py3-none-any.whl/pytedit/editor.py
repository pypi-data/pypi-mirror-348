"""
Editor module for PyTEdit.
Main editor class that coordinates between components.
"""

import os
from prompt_toolkit import Application
from prompt_toolkit.buffer import Buffer
from prompt_toolkit.layout.containers import HSplit, Window
from prompt_toolkit.layout.controls import BufferControl, FormattedTextControl
from prompt_toolkit.layout.layout import Layout
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.application import get_app
from prompt_toolkit.filters import Condition

from .text_buffer import TextBuffer


class Editor:
    """Main editor class that coordinates between components"""
    
    def __init__(self, custom_keys=None):
        """
        Initialize the editor
        
        Args:
            custom_keys (dict, optional): Dictionary of custom key bindings
        """
        self.buffer = TextBuffer()
        self.status_message = "Welcome to PyTEdit! Ctrl-S: Save | Ctrl-Q: Quit"
        self.bindings = self.create_key_bindings()
        
        # Add any custom key bindings
        if custom_keys:
            for key, func in custom_keys.items():
                self.bindings.add(key)(func)
        
        # Create prompt_toolkit components
        self.text_buffer = Buffer(
            multiline=True, 
            # read_only=True  # We'll handle editing ourselves
        )
        
        # Create the layout
        self.layout = Layout(
            HSplit([
                # Main editing area
                Window(
                    content=BufferControl(buffer=self.text_buffer),
                    wrap_lines=True,
                ),
                # Status bar
                Window(
                    height=1,
                    content=FormattedTextControl(self.get_status_text),
                    style="class:status"
                )
            ])
        )
        
        # Create the application
        self.app = Application(
            layout=self.layout,
            key_bindings=self.bindings,
            full_screen=True,
            mouse_support=True
        )
        
        # Update the display
        self.refresh_screen()
    
    def create_key_bindings(self):
        """
        Create key bindings for the editor
        
        Returns:
            KeyBindings: The keyboard bindings for the editor
        """
        kb = KeyBindings()
        
        # Quit binding
        @kb.add('c-q')
        def _(event):
            """Quit the editor"""
            if not self.buffer.modified:
                event.app.exit()
            else:
                self.status_message = "Unsaved changes! Press Ctrl-Q again to quit without saving"
                
                # Set up a condition for the next press
                @Condition
                def quit_pressed():
                    return True
                
                @kb.add('c-q', filter=quit_pressed)
                def _(event):
                    event.app.exit()
        
        # Save binding
        @kb.add('c-s')
        def _(event):
            """Save the current file"""
            if self.buffer.filename:
                if self.buffer.save_file():
                    self.status_message = f"Saved {self.buffer.filename}"
                else:
                    self.status_message = f"Error saving {self.buffer.filename}"
            else:
                # In a real implementation, we would add a file dialog
                self.status_message = "No filename set (save dialog not implemented yet)"
            self.refresh_screen()
        
        # Clear status message
        @kb.add('escape')
        def _(event):
            self.status_message = "Welcome to PyTEdit! Ctrl-S: Save | Ctrl-Q: Quit"
            self.refresh_screen()
        
        # Navigation keys
        @kb.add('up')
        def _(event):
            self.buffer.move_cursor(rows=-1)
            self.refresh_screen()
        
        @kb.add('down')
        def _(event):
            self.buffer.move_cursor(rows=1)
            self.refresh_screen()
        
        @kb.add('left')
        def _(event):
            self.buffer.move_cursor(cols=-1)
            self.refresh_screen()
        
        @kb.add('right')
        def _(event):
            self.buffer.move_cursor(cols=1)
            self.refresh_screen()
        
        # Editing keys
        @kb.add('backspace')
        def _(event):
            self.buffer.backspace()
            self.refresh_screen()
        
        @kb.add('delete')
        def _(event):
            self.buffer.delete()
            self.refresh_screen()
        
        @kb.add('enter')
        def _(event):
            self.buffer.insert_newline()
            self.refresh_screen()
        
        # Regular character input
        @kb.add_binding(' ')
        def _(event):
            self.buffer.insert_char(' ')
            self.refresh_screen()
        
        # Add handlers for all printable characters
        for i in range(32, 127):
            char = chr(i)
            if char != ' ':  # Space already handled above
                @kb.add_binding(char)
                def _(event, char=char):
                    self.buffer.insert_char(char)
                    self.refresh_screen()
        
        return kb
    
    def get_status_text(self):
        """
        Get the text for the status bar
        
        Returns:
            str: Formatted status bar text
        """
        filename = self.buffer.filename or "[No File]"
        modified = "*" if self.buffer.modified else ""
        position = f"Line {self.buffer.cursor_row+1}, Col {self.buffer.cursor_col+1}"
        return f"{modified}{filename} | {position} | {self.status_message}"
    
    def refresh_screen(self):
        """Update the screen content"""
        # Update the buffer text
        self.text_buffer.text = self.buffer.get_text()
        
        # Set cursor position
        # We need to convert our row/col to a buffer position
        position = 0
        for i in range(self.buffer.cursor_row):
            position += len(self.buffer.lines[i]) + 1  # +1 for newline
        position += self.buffer.cursor_col
        
        # Get the app and update cursor position
        app = get_app()
        if app.layout and app.layout.current_buffer:
            app.layout.current_buffer.cursor_position = position
    
    def run(self, filename=None):
        """
        Run the editor with an optional file to open
        
        Args:
            filename (str, optional): Path to a file to open
        """
        if filename and os.path.exists(filename):
            self.buffer.load_file(filename)
            self.status_message = f"Loaded {filename}"
        
        self.refresh_screen()
        self.app.run()