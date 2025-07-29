#!/usr/bin/env python
"""
Command-line interface for LLM Insight Forge
"""

import argparse
import sys
from . import __version__

def main():
    """Main entry point for the CLI"""
    parser = argparse.ArgumentParser(
        description="LLM Insight Forge - A toolkit for LLMs"
    )
    parser.add_argument(
        '-v', '--version', 
        action='version', 
        version=f'llm_insight_forge {__version__}'
    )
    
    # Add more command line arguments and subcommands here as needed
    args = parser.parse_args()
    
    # If no arguments are provided, show help
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(0)

if __name__ == "__main__":
    main()
