from src.Track.id3tag import TrackInfo
import src.Helper.IO as IO
import os
import time
import subprocess
__author__ = 'Boris Breuer'
fileName = 'Google - congressional'
inputDirectoryPath = os.path.join(
    'd:\\', 'work', 'GitHub', 'AudioToolz', 'data')
inputFilePath = os.path.join(inputDirectoryPath, fileName + '.mp3')
print('Reading from file: ', inputFilePath)
mp3DirectPath = os.path.join('c:\\', 'Program Files (x86)', 'mp3DirectCut')
outputPath = inputDirectoryPath + ' - cut'
IO.mkdir(outputPath)
IO.set_path(IO.get_script_path())
myTrack = TrackInfo(filename=inputFilePath,
                    newtracklength=30 * 60,
                    genre='Hearing',
                    albumname='CNET',
                    albumyear='2018')
myCueSheet = myTrack.cue_sheet()
myCueSheet.to_file(inputDirectoryPath, fileName)

theCommand = '{0} "{1}" {2} "{3}"'.format(
    IO.s_p(os.path.join(mp3DirectPath, 'mp3DirectCut.exe')),
    IO.s_p(os.path.join(inputDirectoryPath, fileName + '.cue')),
    '/split',
    IO.s_p(outputPath))
print(theCommand)
time.sleep(1)
os.system(theCommand)
print(outputPath)
myTrack.add_track_numbers(outputPath)
