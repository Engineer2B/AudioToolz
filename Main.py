__author__ = 'Boris Breuer'
from id3tag import TrackInfo
import IO
import os
import time
import subprocess
strFileName = 'Jason Fried and David Heinemeier Hansson - Rework'
strPathInput = 'd:\\' + os.path.join('Sync', 'Audiobooks\\')
strPathMP3Direct = 'c:\\' + os.path.join('Program Files (x86)', 'mp3DirectCut\\')
strPathOutput = strPathInput + strFileName
IO.mkdir(strPathOutput)
IO.set_path(IO.get_script_path())
print strPathInput + strFileName + '.mp3'
myTrack = TrackInfo(filename=strPathInput + strFileName + '.mp3',
                    newtracklength=30 * 60,
                    genre='Audiobook',
                    albumyear='2006')
myCueSheet = myTrack.cue_sheet()
myCueSheet.to_file(strPathInput, strFileName)

theCommand = '"{0} "{1}" {2} "{3}"'.format(
    IO.s_p(strPathMP3Direct) + 'MP3DIR~1.exe',
    IO.s_p(strPathInput) + strFileName + '.cue',
    '/split',
    IO.s_p(strPathOutput))
print theCommand
time.sleep(1)
os.system(theCommand)
print strPathOutput
myTrack.add_track_numbers(strPathOutput)