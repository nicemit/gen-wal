#!/usr/bin/env python3
"""
Legacy entrypoint for Gen-Wal.
Please use the `genwal` bash wrapper or run `python src/cli.py` instead.
This file is kept for backwards compatibility during the architectural transition 
and forwards all arguments to the new CLI.
"""
from src.cli import main

if __name__ == "__main__":
    main()
