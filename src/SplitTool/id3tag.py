__author__ = 'Boris Breuer'
from mutagen.easyid3 import EasyID3
from mutagen.mp3 import MP3
import IO
from CueSheet import CueSheet
from Variables import assert_int_or_float, assert_str
import re


def tryGet(dictionary, key):
    value = dictionary.get(key, None)
    if value is not None:
        return value
    else:
        raise ValueError('ID3tag does not have a value for ' + key + ', bitch!')


class TrackInfo:
    def __init__(self, filename, newtracklength,
                 albumname='', trackname='', performer='', genre='', albumyear=''):
        assert_str(filename)
        if IO.file_exists(filename):
            self.fileName = filename
            if filename.endswith('.mp3'):
                self.EasyID3 = EasyID3(filename)
                self.mp3 = MP3(filename)
                assert_int_or_float(newtracklength)
                self.newTrackLength = newtracklength
                assert_str(trackname)
                if trackname != '':
                    self.trackName = trackname
                else:
                    self.trackName = str(tryGet(self.EasyID3, 'title')[0])
                assert_str(performer)
                if performer != '':
                    self.performer = performer
                else:
                    self.performer = str(tryGet(self.EasyID3, 'artist')[0])
                assert_str(albumname)
                if albumname != '':
                    self.albumName = albumname
                else:
                    self.albumName = str(tryGet(self.EasyID3, 'album')[0])
                assert_str(genre)
                if genre != '':
                    self.albumGenre = genre
                else:
                    self.albumGenre = str(tryGet(self.EasyID3, 'genre')[0])
                assert_str(albumyear)
                if albumyear != '':
                    self.albumYear = albumyear
                else:
                    self.albumYear = str(tryGet(self.EasyID3, 'date')[0])
                self.trackLength = self.mp3.info.length
            else:
                raise ValueError('File should be an mp3, bitch!')
        else:
            raise ValueError('Enter a valid file name, bitch!')

    def cue_sheet(self):
        return CueSheet(self.albumName, self.trackName, self.performer, self.albumGenre,
                        self.albumYear, self.trackLength, self.newTrackLength)

    def add_track_numbers(self, str_path_name):
        ls_str_files = IO.list_file_names(str_path_name)
        for strFileName in ls_str_files:
            easy_id3_object = EasyID3(str_path_name + "\\" + strFileName)
            regex_title = re.match(self.trackName + " (\d{2})\-(\d{2})$",
                                   IO.get_file_name(strFileName))
            track_number = regex_title.group(1)
            total_tracks = regex_title.group(2)
            easy_id3_object["tracknumber"] = track_number + "/" + total_tracks
            easy_id3_object["title"] = self.trackName + " " + \
                                       track_number + " of " + total_tracks
            easy_id3_object["genre"] = self.albumGenre
            easy_id3_object["date"] = self.albumYear
            easy_id3_object["encodedby"] = "AudioToolz with MP3DirectCut"
            easy_id3_object.save()



            # for strFile in lsstrFiles:
            #     # Construct a reader from a file or filename.
            #     strPath = strDir + strFile
            #     mp3Object = EasyID3(strPath)
            #     lsstrTrackTitle = mp3Object["title"]

            # #regexTitle = re.search("^\(([0-9]{1,2})", lsstrTrackTitle[0])
            # #strTrackNumber = lsstrTrackTitle[0][indexStart:indexEnd]
            #
            # regexFileName = re.search("\(Part ([0-9])\) ([0-9]{1,2}) of (13).mp3$", strFile)
            # indexStart1 = regexFileName.regs[1][0]
            # indexEnd1 = regexFileName.regs[1][1]
            # indexStart2 = regexFileName.regs[2][0]
            # indexEnd2 = regexFileName.regs[2][1]
            # indexStart3 = regexFileName.regs[3][0]
            # indexEnd3 = regexFileName.regs[3][1]
            # strDiscNumber = strFile[indexStart1:indexEnd1]
            # strTrackNumber = strFile[indexStart2:indexEnd2]
            # if len(strTrackNumber) < 2:
            #     strTrackNumber = "0"+strTrackNumber
            # strTotalTracks = strFile[indexStart3:indexEnd3]
            # strTitle = strFile[0:indexStart1-7]
            #
            # mp3Object["tracknumber"] = strTrackNumber+"/"+strTotalTracks
            # mp3Object["discnumber"] = strDiscNumber+"/2"
            # mp3Object["title"] = strTitle + " " + strTrackNumber + "/" + strTotalTracks + " disc " + strDiscNumber + "/" + "2"
            # # strTrackNumber + " - Nudge: Improving Decisions About Health, Wealth, and Happiness"
            # mp3Object.save()
