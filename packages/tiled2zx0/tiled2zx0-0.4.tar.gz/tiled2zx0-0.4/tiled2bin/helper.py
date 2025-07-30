import os
import sys
from pathlib import Path
import subprocess

def runCommand(command):
    result = subprocess.call(command, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    if result != 0:
        print("Error executing command: " + command)
        sys.exit(1)

def tiledExport(mapsFile):
    if os.name == "nt":
        program_files = os.environ["ProgramFiles"]
        return "\"" + program_files + "\\Tiled\\tiled.exe\" --export-map json " + mapsFile + " " + str(Path("output/maps.json"))
    else:
        return "tiled --export-map json " + mapsFile + " " + str(Path("output/maps.json"))