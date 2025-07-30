#!/usr/bin/env python3

import sys

from tiled2bin import ioUser
from tiled2bin.Tiled2ZX0 import Tiled2ZX0
from tiled2bin import helper

def main(argv=None):
    if argv is None:
        argv = sys.argv[1:]

    try:
        # Check if Tiled is installed in linux and windows
        if sys.platform.startswith('linux'):
            import subprocess
            result = subprocess.run(['which', 'tiled'], stdout=subprocess.PIPE)
            if result.returncode != 0:
                raise Exception("Tiled is not installed or not found in PATH")

        elif sys.platform.startswith('win32'):
            import os
            if not os.path.exists('C:\\Program Files\\Tiled\\tiled.exe'):
                raise Exception("Tiled is not installed or not found in PATH")
        
        args = ioUser.validateArguments(argv)
        
        # Export Tiled map
        helper.runCommand(helper.tiledExport(args['mapFile']))

        Tiled2ZX0(args['map'], args['offsets'], args['basic']).convert()

    except Exception as e:
        print(f"Error: {e}")
        ioUser.validateArguments(['-h'])

if __name__ == "__main__":
   main(sys.argv[1:])
