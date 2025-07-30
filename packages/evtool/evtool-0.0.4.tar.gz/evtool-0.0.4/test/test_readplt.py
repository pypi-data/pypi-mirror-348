#!/bin/env python
# PYTHON_ARGCOMPLETE_OK
# -*- coding: utf-8 -*-

""" readplt.py:  Read a ev/STARS/TWIN plt file.
    2023-09-08, MvdS: initial version.
"""


import colored_traceback
colored_traceback.add_hook()

import argparse
import argcomplete

import evtool.plt as evplt


def main():
    """Main function."""
    
    # Get command-line arguments:
    args = get_cli_arguments()
    
    # read_plt('01.00Mo-2005.plt1', 9)
    df = evplt.read_plt('01.00Mo.plt1', args.verbosity)
    print(df)
    
    
    exit(0)
    
    
def get_cli_arguments():
    """Get the command-line arguments.
    
    Returns:
      (struct):  Struct containing command-line arguments.
    """
    
    # Parse command-line arguments:
    parser = argparse.ArgumentParser(description='Read a ev/STARS/TWIN plt file.',
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)  # Use capital, period, add default values
    
    parser.add_argument('-v', '--verbosity', action='count', default=0, help='increase output verbosity')  # Counts number of occurrences
    
    argcomplete.autocomplete(parser)
    args = parser.parse_args()
    
    return args




if __name__ == '__main__':
    main()

