import os
import string
import sys
from pathlib import Path
from typing import List, Optional
import re
import music_tag
import objects
from objects import AlbumObject


def set_music_information(album_obj: objects.AlbumObject):
    """
    Set information from album object in the music file and saves this to disk.
    :param album_obj:
    :param file_path:
    """
    if album_obj != None:
        try:
            music_file = music_tag.load_file(album_obj.complete_file_path)
            print("set_music_information save " + album_obj.complete_file_path)
        except Exception as ex:
            sys.stdout.write("ERROR: set_music_information load file " + album_obj.complete_file_path + str(ex))
            print("         ")
            return None

        if album_obj.artist_name != "":
            music_file["artist"] = album_obj.artist_name

        if album_obj.release_year != 0:
            music_file["year"] = album_obj.release_year

        if music_file["tracktitle"] != "":
            music_file["tracktitle"] = album_obj.title_name

        if album_obj.title_name != "":
            music_file["album"] = album_obj.title_name

        if album_obj.genre != "":
            music_file["genre"] = album_obj.genre

        try:
            music_file.save()
            print("set_music_information save " + album_obj.complete_file_path)
        except Exception as ex:
            sys.stdout.write("ERROR: set_music_information save " + album_obj.complete_file_path + str(ex))
            print("         ")
            return None

    else:
        return None


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


def get_album_from_file_path(file_path: string) -> Optional[AlbumObject]:
    """
    Get information form file name and adds to albumObject.
    Renames file with cleaned file name.
    :param file_path:
    :return: filled album object, null if error
    """
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
        print("ERROR: No seperator in file path! " + file_path)
        return None

    # Split into artist name and album/track title
    seperator_index: int = file_path.find(seperator)
    seperator_index_slash: int = file_path.rfind("/")

    # Removes Trash like this S̲y̲s̲tem o̲f a D̲o̲wn
    # In normal txt editor it looks like the ̲ would be under the latter's.
    artist_name: string = file_path[seperator_index_slash + 1:seperator_index - 1].strip()
    album_object.artist_name = artist_name.replace("̲", "")

    print("artist_name " + str(artist_name))

    album_object.file_ending = get_file_ending(file_path)

    title_name: string = file_path[seperator_index + 1:].strip().replace("̲", "")

    title_name = title_name.replace("_", " ")

    # TODO ADD MORE CASES
    title_name = re.sub("\[?\(?Full Album\)?]?", "", title_name, flags=re.IGNORECASE)
    title_name.strip()

    file_ending_len = (len(album_object.file_ending))
    title_name = title_name[:(len(title_name) - file_ending_len)]

    album_object.title_name = title_name

    # 2001
    # [2001]
    # (2001)
    # (2001-2011)
    year_pattern: string = "\[?\(?\d{4}\)?]?\-?"
    match_object = re.search(year_pattern, title_name)
    if match_object is not None:
        album_object.release_year = re.search("\d{4}", match_object.group()).group()
        album_object.title_name = re.sub(year_pattern, "", title_name)
        print("release_year " + str(album_object.release_year))
    else:
        print("No release_year contained in " + file_path)

    print("title_name " + album_object.title_name)

    # Get genre from folder that the album contains
    path: Path = Path(file_path)
    album_object.genre = path.parent.absolute().name
    print("genre " + album_object.genre)

    # clean file name
    album_object.clean_file_name = (artist_name + " " + clean_file_separator + " "
                                    + album_object.title_name).strip() + album_object.file_ending

    # TODO Do more path cleaning
    # Also remove trash like this:  🎸

    destination_path: string = str(path.parent.absolute()) + "/" + album_object.clean_file_name

    # rename file using clean file name
    try:
        if album_object.complete_file_path != destination_path:
            os.rename(album_object.complete_file_path, destination_path)
            print("Renamed file:" + album_object.complete_file_path + " -> " + destination_path)
            album_object.complete_file_path = destination_path
    except Exception as ex:
        sys.stdout.write("ERROR: Rename file failed exception: " + str(ex))
        print("         ")
        return None

    return album_object


def get_file_ending(file_path):
    index_of_dot = file_path.rfind(".")
    file_ending: string = file_path[index_of_dot:]
    return file_ending
