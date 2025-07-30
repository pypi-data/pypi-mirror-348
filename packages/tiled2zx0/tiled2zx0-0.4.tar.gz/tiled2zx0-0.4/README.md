# tiled2zx0
Simple command to convert Tiled map (.tmx) into compressed (with Einar Saukas ZX0) bin file.

If you for example have an "infinite" Tiled map it has defined screens size, 32x22 for example. This command will compress each
screen separately and then join all parte in only one file and return screens offsets binary file in order to know where each screen starts.

If you specify -b OUTPUT_BORIEL_FILE, the command retuns boriel code to draw a screen and swap/decompress current screen.

## Install
pip install tiled2zx0

## Run
```bash
usage: tiled2zx0 [-h] [-m OUTPUT_MAP_FILE] [-o OUTPUT_MAP_OFFSETS_FILE] [-b OUTPUT_BORIEL_FILE] /path/map.tmx
```

## Attribution
This project use [ZX0 compressor by Einar Saukas](https://github.com/einar-saukas/ZX0) binaries.
