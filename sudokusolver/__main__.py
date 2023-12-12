import sys
import os
from .utils import handler

if __name__ == '__main__':
    cwd = os.getcwd()
    handler(cwd, sys.argv)
