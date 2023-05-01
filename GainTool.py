import pydub
import json
import os
import sys
import argparse
import src.Helper.IO as IO
from src.Helper import PathType

parser = argparse.ArgumentParser()
parser.add_argument("inputFolderPath", help="Path to the input folder.",
                    type=PathType.PathType(exists=True, type='dir'))
parser.add_argument(
    "-o",
    "--outputFolderPath",
    help="Path to the output folder,\
                     will generate files in '$inputFolderPath$-gain'if not \
                     specified.",
    type=PathType.PathType(
        exists=False,
         type='dir'))
args = parser.parse_args()
inputFolderPath = args.inputFolderPath
outputFolderPath = args.outputFolderPath if args.outputFolderPath else \
    inputFolderPath.rstrip(
        '/').rstrip('\\') + '-Gain'
print(outputFolderPath)
IO.mkdir(outputFolderPath)

# If your current working directory may change during script execution, it's
# recommended to immediately convert program arguments to an absolute path.
# Then the variable root below will be an absolute path as well. Example:
# walk_dir = os.path.abspath(walk_dir)
print('walk_dir (absolute) = ' + os.path.abspath(inputFolderPath))

with open(os.path.join(sys.path[0], "FFmpegFormats.json")) as \
        ffmpegFormatsFile:
    ffmpegFormats = json.load(ffmpegFormatsFile)
    decodeExtensions = ffmpegFormats["Only decode"] + \
        ffmpegFormats["Decode and encode"]
    for root, subdirs, files in os.walk(inputFolderPath):
        print('--\nroot = ' + root)
        for subdir in subdirs:
            print('\t- subdirectory ' + subdir)
        for filename in files:
            fileAndExt = os.path.splitext(filename)
            if(fileAndExt[1] in decodeExtensions):
                filePath = os.path.join(root, filename)
                print('\t- file %s (full path: %s)' % (filename, filePath))
                with open(filePath, 'rb') as fileHandle:
                    audioSegment = pydub.AudioSegment.from_file(fileHandle)
                    # Increase volume by 50 dB
                    audioSegment_50db_louder = audioSegment + 50
                    # save the output
                    outFilePath = os.path.join(
                        outputFolderPath, fileAndExt[0] + ".mp3")
                    fileHandle = audioSegment_50db_louder.export(
                        outFilePath, "mp3")
