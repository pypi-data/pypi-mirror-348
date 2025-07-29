from setuptools import setup, find_packages

setup(
    name="pytedit",
    version="0.1.1",
    author="Rachit Sharma, Lavkesh Dongre",
    author_email="rachits999003@example.com",
    description="A lightweight terminal-based text editor library for Python",
    long_description='''# PyTEdit

A lightweight, fast, terminal-based text editor library for Python. PyTEdit provides a modular and extensible framework for building terminal text editors, similar to `nano` or `micro`, but with modern Python features.

## Features

- File loading and saving
- Arrow key navigation
- Basic editing (insert, delete, backspace)
- Save & quit shortcuts (`Ctrl+S`, `Ctrl+Q`)
- Responsive interface with smooth cursor movement
- Clean, modular code structure
- Can be used as a library or standalone application

## Installation

```bash
pip install pytedit
```

## Quick Start

### Using as a standalone editor

```bash
# Launch editor
pytedit

# Open a file
pytedit myfile.txt
```

### Using as a library in your project

```python
from pytedit import Editor, TextBuffer

# Create a custom editor
class MyCustomEditor(Editor):
    def __init__(self):
        super().__init__()
        # Add custom initialization
        self.status_message = "My Custom Editor"
    
    def create_key_bindings(self):
        kb = super().create_key_bindings()
        
        # Add custom key bindings
        @kb.add('c-f')
        def _(event):
            self.status_message = "Find functionality (custom)"
            self.refresh_screen()
            
        return kb

# Run your custom editor
if __name__ == "__main__":
    editor = MyCustomEditor()
    editor.run()
```

## Architecture

PyTEdit is built around these core components:

1. **TextBuffer**: Manages text content and cursor position
2. **Editor**: Handles input, rendering, and coordinates components
3. **Key Bindings**: Configurable keyboard shortcuts for editor functions

## Development Roadmap

- Undo/redo stack
- Syntax highlighting with Pygments
- Line numbers
- Search & replace functionality
- Configurable themes and keybindings
- Multiple file buffers
- Split-screen editing

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.''',
    long_description_content_type="text/markdown",
    url="https://github.com/rachits999003/pytedit",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Environment :: Console",
        "Topic :: Text Editors",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.7",
    install_requires=[
        "prompt_toolkit>=3.0.0",
    ],
    entry_points={
        "console_scripts": [
            "pytedit=pytedit.cli:main",
        ],
    },
)