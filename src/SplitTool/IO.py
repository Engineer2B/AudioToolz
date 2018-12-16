__author__ = 'Boris Breuer'
from os import chdir, path, makedirs, listdir
import sys
import subprocess


def list_file_names(str_path_name):
    return listdir(str_path_name)


def get_extension(str_file_name):
    return path.splitext(str_file_name)[1]


def get_file_name(str_file_name):
    return path.splitext(str_file_name)[0]


def file_exists(str_file_name):
    return path.isfile(str_file_name)


def get_script_path():
    return path.dirname(path.realpath(sys.argv[0]))


def set_path(str_path):
    chdir(str_path)


def s_p(str_path):
    return strip_eol(subprocess.check_output('command "{0}"'.format(str_path), shell=True))


def strip_eol(str_input):
    return str_input.decode("utf-8") .replace('\r', '').replace('\n', '')


def mkdir(str_path):
    if not path.exists(str_path):
        makedirs(str_path)