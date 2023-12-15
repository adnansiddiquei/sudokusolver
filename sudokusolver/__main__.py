import sys
import os
from ._handler import handler

if __name__ == '__main__':
    cwd = os.getcwd()
    handler(cwd, sys.argv)
