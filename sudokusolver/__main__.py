import sys
import os
from ._handler import handler

if __name__ == '__main__':
    cwd = os.getcwd()

    # Call the handler function with the current working directory and the command line arguments
    handler(cwd, sys.argv)
