"""Command-line interface for pypitester."""

import argparse
import sys
from . import utils, __version__

def main():
    """Run the pypitester CLI."""
    parser = argparse.ArgumentParser(description="A simple PyPI test package")
    parser.add_argument("--version", action="store_true", help="Show version and exit")
    parser.add_argument("--name", default="User", help="Name to greet")
    
    args = parser.parse_args()
    
    if args.version:
        print(f"pypitester version {__version__}")
        return 0
    
    print(utils.greet(args.name))
    return 0

if __name__ == "__main__":
    sys.exit(main()) 