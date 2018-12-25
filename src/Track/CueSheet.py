__author__ = 'Boris Breuer'
import numpy as np
import math
import os
from src.Helper.Variables import assert_int_or_float, assert_str


def str_track(track_number):
    return 'TRACK ' + track_number.zfill(2) + ' AUDIO'


def seconds_to_hhmmss(seconds):
    minutes = int(math.floor(seconds / 60))
    seconds = int(math.floor((seconds % 3600) % 60))
    return str(minutes).zfill(2) + ":" + str(seconds).zfill(2) + ':00'


def get_intervals(seconds, time_interval):
    assert_int_or_float(seconds)
    np_intervals = np.arange(0, seconds, time_interval)
    return np_intervals


class CueSheet:
    def __init__(self, album_name, track_name, performer, album_genre, album_year, track_length, new_track_length):
        assert_str(album_genre)
        self.albumGenre = album_genre
        assert_str(album_year)
        self.albumYear = album_year
        assert_str(album_name)
        self.albumName = album_name
        assert_str(track_name)
        self.trackName = track_name
        assert_str(performer)
        self.performer = performer
        self.newTrackLengths = get_intervals(track_length, new_track_length)

    def str_file(self, file_name):
        return 'FILE "' + file_name + '.mp3' + '" MP3'

    def str_genre(self):
        return 'REM GENRE "' + self.albumGenre + '"'

    def str_year(self):
        return 'REM DATE "' + self.albumYear + '"'

    def str_album(self):
        return 'TITLE "' + self.albumName + '"'

    def str_title(self):
        return 'TITLE "' + self.trackName + '"'

    def str_performer(self):
        return 'PERFORMER ' + '"' + self.performer + '"'

    def str_index(self, track_number):
        return 'INDEX 01 ' + seconds_to_hhmmss(self.newTrackLengths[track_number])

    def to_file(self, path_name, file_name):
        the_file = open(os.path.join(path_name, file_name + ".cue"), "w")
        the_file.write('{0}\n{1}\n{2}\n{3}\n{4}\n'.format(
            self.str_genre(),
            self.str_year(),
            self.str_performer(),
            self.str_album(),
            self.str_file(file_name)))
        str_out = ''
        for index_track in range(0, len(self.newTrackLengths)):
            track_number = str(index_track + 1)
            the_file.write('{0}  {1}\n    {2}\n    {3}\n    {4}\n'.format(
                str_out,
                str_track(track_number),
                self.str_title(),
                self.str_performer(),
                self.str_index(index_track)))
        the_file.close()


'''
FILE
    Names a file containing the data and its format (such as MP3,
    and WAVE audio file formats, and plain "binary" disc images)
TRACK
    Defines a track context, providing its number and type or mode
    (for instance AUDIO or various CD-ROM modes). Some commands
    that follow this command apply to the track rather than
    the entire disc.
INDEX
    Indicates an index (position) within the current FILE.
    The position is specified in mm:ss:ff (minute-second-frame)
    format. There are 75 such frames per second of audio.
    In the context of cue sheets, "frames" refer to CD sectors,
    despite a different, lower-level structure in CDs also
    being known as frames.[5] INDEX 01 is required and denotes
    the start of the track, while INDEX 00 is optional and
    denotes the pregap. The pregap of Track 1 is used for
    Hidden Track One Audio (HTOA). Optional higher-numbered
    indexes (02 through 99) are also allowed.
PREGAP and POSTGAP
    Indicates the length of a track's pregap or postgap, which
    is not stored in any data file. The length is specified
    in the same minute-second-frame format as for INDEX.
REM
    Adds a comment that usually has no bearing on the written
    CD at all, with the exception of some applications that
    use it to store additional metadata (e.g. Exact Audio
    Copy writes some additional fields, which foobar2000 can read)
CDTEXTFILE
    Identifies a file containing CD-Text information
FLAGS
    Sets subcode flags of a track
CATALOG
    Contains the UPC/EAN code of the disc
ISRC
    Define the ISRC of the current TRACK
TITLE, PERFORMER and SONGWRITER
    CD-Text metadata; applies to the whole disc or a
    specific track, depending on the context

REM GENRE "Electronica"
REM DATE "1998"
PERFORMER "Faithless"
TITLE "Live in Berlin"
FILE "Faithless - Live in Berlin.mp3" MP3
  TRACK 01 AUDIO
    TITLE "Reverence"
    PERFORMER "Faithless"
    INDEX 01 00:00:00
  TRACK 02 AUDIO
    TITLE "She's My Baby"
    PERFORMER "Faithless"
    INDEX 01 06:42:00
'''
