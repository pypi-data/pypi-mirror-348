"""
Command-line interface for PyTEdit.
Handles command-line arguments and launches the editor.
"""

import sys
import argparse
from .editor import Editor


def main():
    """Main entry point for the editor"""
    parser = argparse.ArgumentParser(description="PyTEdit - A lightweight terminal text editor")
    parser.add_argument('filename', nargs='?', help='File to open')
    parser.add_argument('--version', action='store_true', help='Display version information')
    
    args = parser.parse_args()
    
    if args.version:
        from . import __version__
        print(f"PyTEdit version {__version__}")
        return
    
    editor = Editor()
    editor.run(args.filename)


if __name__ == "__main__":
    main()