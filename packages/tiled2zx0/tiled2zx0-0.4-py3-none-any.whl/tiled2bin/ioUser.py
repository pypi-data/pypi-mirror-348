import argparse
import os.path

def validateArguments(argv):
    parser = argparse.ArgumentParser(description='Process some arguments.')
    parser.add_argument('mapFile', type=str, help='Input map file')
    parser.add_argument('-m', '--map', type=str, required=False, help='Output map file (optional)')
    parser.add_argument('-o', '--offsets', type=str, required=False, help='Output offsets file (optional)')
    parser.add_argument('-b', '--basic', type=str, required=False, help='Output BASIC file (optional)')

    args = parser.parse_args(argv)

    map = os.path.join(os.getcwd(), "map.zx0") if args.map is None else args.map
    offsets = os.path.join(os.getcwd(), "screenOffsets.bin") if args.offsets is None else args.offsets
    basic = os.path.join(os.getcwd(), "output.bas") if args.basic is None else args.basic

    if not os.path.exists(args.mapFile):
        raise FileNotFoundError(f"Map file '{args.mapFile}' does not exist.")

    result = {
        "mapFile": args.mapFile,
        "map": map,
        "offsets": offsets,
        "basic": basic
    }

    return result