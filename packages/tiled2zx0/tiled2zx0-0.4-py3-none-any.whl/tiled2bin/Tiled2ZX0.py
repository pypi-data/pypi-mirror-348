import json
import os
import subprocess
from pathlib import Path
import array

class Tiled2ZX0:
    def __init__(self, outputMapFile=None, outputMapOffsetsFile=None, outputBasicFile=None):
        self.outputDir = 'output/'
        if not os.path.exists(self.outputDir):
            os.makedirs(self.outputDir)
        if outputMapFile is None:
            outputMapFile = Path(self.outputDir) / 'map.tmx.zx0'
        self.output_map_file = outputMapFile
        if outputMapOffsetsFile is None:
            outputMapOffsetsFile = Path(self.outputDir) / 'screenOffsets.bin'
        self.output_map_offsets_file = outputMapOffsetsFile
        self.output_basic_file = outputBasicFile

    def convert(self):
        currentOffset = 0
        screenOffsets = []
        screens = []

        data = json.load(open(self.outputDir + 'maps.json', 'r', encoding='utf-8'))

        # Screens count per row
        screenWidth = data['editorsettings']['chunksize']['width']
        screenHeight = data['editorsettings']['chunksize']['height']
        cellsPerScreen = screenWidth * screenHeight

        tileHeight = data['tileheight']
        tileWidth = data['tilewidth']

        screenPixelsWidth = screenWidth * tileWidth
        screenPixelsHeight = screenHeight * tileHeight

        spriteTileOffset = 0

        for layer in data['layers']:
            if layer['type'] == 'tilelayer':
                screens = []
                for idx, screen in enumerate(layer['chunks']):
                    screens.append(array.array('B', screen['data']))

        for idx, screen in enumerate(screens):
            label = 'screen' + str(idx).zfill(3)
            with open(self.outputDir + label + '.bin', 'wb') as f:
                screen.tofile(f)
            subprocess.run(['bin/zx0', '-f', self.outputDir + label + '.bin', self.outputDir + label + '.bin.zx0'],
               stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            currentOffset += os.path.getsize(self.outputDir + label + '.bin.zx0')
            screenOffsets.append(currentOffset)
        
        # Concatenate all screens into one file
        with open(self.output_map_file, 'wb') as f:
            for idx, screen in enumerate(screens):
                label = 'screen' + str(idx).zfill(3) + '.bin.zx0'
                with open(self.outputDir + label, 'rb') as screenFile:
                    f.write(screenFile.read())
        
        # Remove output/screen* files
        for idx, screen in enumerate(screens):
            label = 'screen' + str(idx).zfill(3) + '.bin'
            os.remove(self.outputDir + label)
            label = 'screen' + str(idx).zfill(3) + '.bin.zx0'
            os.remove(self.outputDir + label)

        with open(self.output_map_offsets_file, "wb") as f:
            for offset in screenOffsets:
                f.write(offset.to_bytes(2, byteorder='little'))
        
        if self.output_basic_file is not None:
            basicStr = "Const SCREENS_COUNT = " + str(len(screens)) + "\n"
            basicStr += "Dim screensOffsets(SCREENS_COUNT) As Uinteger at MAP_OFFSETS_ADDRESS" + "\n"
            basicStr += "const SCREEN_LENGTH as uinteger = " + str(len(screens[0]) - 1) + "\n"
            basicStr += "dim decompressedMap(SCREEN_LENGTH) as ubyte\n\n"

            basicStr += "Sub swapScreen(screen As Ubyte)\n"
            basicStr += "    dzx0Standard(MAPS_DATA_ADDRESS + screensOffsets(screen), @decompressedMap)\n"
            basicStr += "End Sub\n\n"

            basicStr += "Sub mapDraw()\n"
            basicStr += "    Dim index As Uinteger\n"
            basicStr += "    Dim y, x As Ubyte\n"
            basicStr += "    \n"
            basicStr += "    x = 0\n"
            basicStr += "    y = 0\n"
            basicStr += "    \n"
            basicStr += "    For index=0 To SCREEN_LENGTH\n"
            basicStr += "        drawTile(Peek(@decompressedMap + index) - 1, x, y)\n"
            basicStr += "        \n"
            basicStr += "        x = x + 1\n"
            basicStr += "        If x = screenWidth Then\n"
            basicStr += "            x = 0\n"
            basicStr += "            y = y + 1\n"
            basicStr += "        End If\n"
            basicStr += "    Next index\n"
            basicStr += "End Sub\n\n"

            basicStr += "MAP_DATA_ADDRESS:\n"
            basicStr += "    Asm\n"
            basicStr += "        incbin \"" + self.output_map_file + "\"\n"
            basicStr += "    End Asm\n"
            basicStr += "MAP_OFFSETS_ADDRESS:\n"
            basicStr += "    Asm\n"
            basicStr += "        incbin \"" + self.output_map_offsets_file + "\"\n"
            basicStr += "    End Asm"

            with open(self.output_basic_file, "w") as f:
                f.write(basicStr)
