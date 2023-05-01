from src.Track.id3tag import TrackInfo
import json
import src.Helper.IO as IO
import os
import time
__author__ = 'Boris Breuer'
# read file
with open(os.path.join('private','splitToolConfig.json'), 'r') as myfile:
    configText=myfile.read()
# parse file
config = json.loads(configText)
# show values
inputDirectoryPath = os.path.join(*config['AudioFile']['DirectoryPath'])
inputFilePath = os.path.join(inputDirectoryPath, config['AudioFile']['FileName'] + '.mp3')
print('Reading from file: ', inputFilePath)

outputPath = inputDirectoryPath + ' - cut'
IO.mkdir(outputPath)
IO.set_path(IO.get_script_path())
myTrack = TrackInfo(filename=inputFilePath,
                    newtracklength=30 * 60,
                    genre=config['AudioFile']['Genre'],
                    albumname=config['AudioFile']['AlbumName'],
                    albumyear=config['AudioFile']['AlbumYear'])
myCueSheet = myTrack.cue_sheet()
myCueSheet.to_file(inputDirectoryPath, config['AudioFile']['FileName'])

theCommand = '{0} "{1}" {2} "{3}"'.format(
    IO.s_p(os.path.join(*config['mp3DirectCutPath'], 'mp3DirectCut.exe')),
    IO.s_p(os.path.join(inputDirectoryPath, config['AudioFile']['FileName'] + '.cue')),
    '/split',
    IO.s_p(outputPath))
print(theCommand)
time.sleep(1)
os.system(theCommand)
print(outputPath)
myTrack.add_track_numbers(outputPath)
