import os
import string
import sys
from pathlib import Path
from typing import List
import re
import music_tag
import objects


def set_music_information(album_obj: objects.AlbumObject, ):
    """
    Set information from album object in the music file and saves this to disk.
    :param album_obj:
    :param file_path:
    """
    music_file = music_tag.load_file(album_obj.complete_file_path)
    music_file["artist"] = album_obj.artist_name
    music_file["year"] = album_obj.release_year
    music_file["tracktitle"] = album_obj.title_name
    music_file["album"] = album_obj.title_name
    music_file["genre"] = album_obj.genre
    music_file.save()


def list_files(folder_path):
    """
    List all files contains in the folder and sub-folders.
    :param folder_path:
    :return: List[string]
    """
    file_list: List[string] = []

    for current_dir, subdirs, files in os.walk(folder_path):
        for filename in files:
            relative_path = os.path.join(current_dir, filename)
            absolute_path = os.path.abspath(relative_path)
            file_list.append(absolute_path)

    return file_list


def get_album_from_file_path(file_path):
    album_object = objects.AlbumObject()
    album_object.complete_file_path = file_path
    album_object.file_name = os.path.basename(file_path)
    album_object.file_ending = album_object.file_name.endswith(file_path)

    # used in clean path
    clean_file_separator = "-"

    # Identify used the seperator
    if "-" in file_path:
        seperator = "-"
    elif "–" in file_path:
        seperator = "–"
    else:
        sys.stderr.write("No seperator in file path! " + file_path)
        return

    seperator_index: int = file_path.rfind(seperator)
    seperator_index_slash: int = file_path.rfind("/")
    artist_name = file_path[seperator_index_slash + 1:seperator_index - 1].strip()
    album_object.artist_name = artist_name
    print("artist_name " + str(artist_name))

    album_object.file_ending = get_file_ending(file_path)

    title_name = file_path[seperator_index + 1:].strip()
    # TODO ADD MORE CASES
    title_name = re.sub(r"\s\(Full Album\)", "", title_name)
    title_name = re.sub(r"\s\[Full Album]", "", title_name)
    title_name.strip()

    file_ending_len = (len(album_object.file_ending))
    title_name = title_name[:(len(title_name) - file_ending_len)]

    album_object.title_name = title_name

    print("title_name " + str(title_name))

    year_pattern = "\s\d{4}"; # TODO MORE CASES
    match_object = re.search(year_pattern, title_name)
    if match_object is not None:
        album_object.release_year = match_object.group().strip()
        album_object.title_name = re.sub(year_pattern,"",title_name)
        print("album_object.release_year " + str(album_object.release_year))
    else:
        print("No date was set " + file_path)

    # Get genre from folder that the album contains
    path = Path(file_path)
    album_object.genre = path.parent.absolute().name

    # clean_file_path # TODO Write to file as new file name
    album_object.clean_file_name = artist_name + " " + clean_file_separator + " " \
                                   + album_object.title_name + album_object.file_ending
    print("album_object.clean_file_name: " + album_object.clean_file_name)

    return album_object


def get_file_ending(file_path):
    index_of_dot = file_path.rfind(".")
    file_ending: string = file_path[index_of_dot:]
    return file_ending
