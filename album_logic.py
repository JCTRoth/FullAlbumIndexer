import os
import shutil
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
    """
    if album_obj != None:
        try:
            music_file = music_tag.load_file(album_obj.complete_file_path)
        except Exception as ex:
            sys.stdout.write("ERROR: set_music_information load file " + album_obj.complete_file_path + str(ex))
            print("         ")
            return None

        if album_obj.artist_name != "":
            music_file["artist"] = album_obj.artist_name

        if album_obj.release_year != "":
            album_obj.release_year = re.sub(r"[^a-zA-Z0-9 ]", "", album_obj.release_year)
            music_file["year"] = int(album_obj.release_year)

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

    folder_path: Path = Path(file_path).parent.absolute()

    # Clean file path from masking
    # Removes Trash like this S̲y̲s̲tem o̲f a D̲o̲wn
    # In normal txt editor it looks like the ̲ would be under the latter's.
    file_path = file_path.replace("̤", "")
    file_path = file_path.replace("̲", "")
    file_path = file_path.replace("_", "")
    file_path = file_path.replace("∙", "")

    # used in clean path for rename
    clean_file_separator = "-"

    separator: string = get_separator_from_filepath(file_path)
    if separator is None:
        return

    # Split into artist name and album/track title
    seperator_index: int = file_path.find(separator)
    seperator_index_slash: int = file_path.rfind("/")

    # Artist_name ---------
    artist_name: string = file_path[seperator_index_slash + 1:seperator_index - 1].strip()
    album_object.artist_name = artist_name
    print("artist_name " + str(artist_name))

    album_object.file_ending = get_file_ending(file_path)

    title_name: string = file_path[seperator_index + 1:].strip()

    # Title ---------
    title_name = title_name.replace("  ", " ")
    title_name = title_name.replace("  ", " ")

    title_name = re.sub("\[?\(?Full Album\)?]?", "", title_name, flags=re.IGNORECASE)
    title_name = re.sub("\[?\(?complete album\)?]?", "", title_name, flags=re.IGNORECASE)
    title_name = re.sub("\[?\(?High Quality\)?]?", "", title_name, flags=re.IGNORECASE)
    title_name = re.sub("(\[?\(?HQ\s?\)?]?)\s", "", title_name, flags=re.IGNORECASE)

    title_name.strip()

    file_ending_len = (len(album_object.file_ending))
    title_name = title_name[:(len(title_name) - file_ending_len)]

    album_object.title_name = title_name

    # Date ---------
    # 2001
    # [2001]
    # (2001)
    # (2001-2011)
    year_pattern: string = "\[?\(?\d{4}\)?]?\-?"
    album_date_string: string = re.findall(year_pattern, title_name)
    if album_date_string:
        album_object.release_year = album_date_string[0][:4]  # 2002- to 2002
        if len(album_date_string) > 1:  # Match 2001-2002
            album_object.title_name = title_name
            # TODO Should be there some changes to the year in the file name?
        else:
            album_object.title_name = re.sub(year_pattern, "", title_name)
            album_object.title_name = album_object.title_name.replace("-", "")
        print("release_year " + str(album_object.release_year))
    else:
        print("No release_year contained in " + file_path)

    # THE BAND - TEST TEST TEST
    # to
    # The Band - Test Test Test
    capital_latters_pattern: string = "[A-Z]{4,}"
    capital_latters_stings = re.findall(capital_latters_pattern, title_name)
    if capital_latters_stings:
        if len(capital_latters_stings) > 1:
            album_object.title_name = album_object.title_name.title()

    print("title_name " + album_object.title_name)

    # Genre ---------
    # Get genre from folder that the album contains
    album_object.genre = folder_path.name
    print("genre " + album_object.genre)

    # Create clean file name
    # Used to rename file with clean file name
    album_object.clean_file_name = (artist_name + " " + clean_file_separator + " "
                                    + album_object.title_name).strip() + album_object.file_ending

    destination_path: string = str(folder_path.absolute()) + "/" + album_object.clean_file_name

    # Rename file using clean file name
    try:
        if album_object.complete_file_path != destination_path:
            os.rename(album_object.complete_file_path,destination_path)
            print("Renamed file:" + album_object.complete_file_path + " -> " + destination_path)
            album_object.complete_file_path = destination_path
    except FileNotFoundError as ex:
        print("ERROR: Rename file failed exception: " + str(ex))
    except FileExistsError as ex:
        print("ERROR: Rename file failed exception: " + str(ex))
    except Exception as ex:
        print("ERROR: Rename file failed exception: " + str(ex))
        print("         ")
        return None

    return album_object


def get_file_ending(file_path: string) -> string:
    """
    Get File Ending from Filename
    :rtype: string
    """
    index_of_dot = file_path.rfind(".")
    file_ending: string = file_path[index_of_dot:]
    return file_ending


def get_separator_from_filepath(file_path: string) -> string:
    """
    Identify Seperator that is used
    Input e.g.: The Artist - Song Name.opus
    :param file_path:
    :return:
    """
    # Identify Seperator that is used
    if "-" in file_path:
        separator = "-"
    elif "–" in file_path:
        separator = "–"
    elif "—" in file_path:
        separator = "—"
    else:
        print("WARN: No seperator in file path! " + file_path)
        return None
    return separator
