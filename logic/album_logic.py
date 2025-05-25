import os
import shutil
import string
import sys
from pathlib import Path
from typing import List, Optional
import re
import music_tag
from logic import objects
from logic.objects import AlbumObject
from logic.char_replacer_helper import TextCleaner


def set_music_information(album_obj: objects.AlbumObject):
    """
    Set information from album object in the music file and saves this to disk.
    :param album_obj: AlbumObject containing the metadata to set
    """
    if album_obj is None:
        print("ERROR: Album object is None")
        return None

    try:
        print(f"INFO: Loading music file: {album_obj.complete_file_path}")
        music_file = music_tag.load_file(album_obj.complete_file_path)
    except Exception as ex:
        print(f"ERROR: Failed to load music file")
        print(f"  File: {album_obj.complete_file_path}")
        print(f"  Error type: {type(ex).__name__}")
        print(f"  Error message: {str(ex)}")
        return None

    try:
        # Artist
        if album_obj.artist_name is not None and album_obj.artist_name.strip() != "":
            music_file["artist"] = album_obj.artist_name.strip()
            print(f"INFO: Set artist tag: {album_obj.artist_name}")

        # Year
        if album_obj.release_year is not None and album_obj.release_year.strip() != "":
            try:
                clean_year = re.sub(r"[^0-9]", "", album_obj.release_year)
                if clean_year.isdigit():
                    music_file["year"] = int(clean_year)
                    print(f"INFO: Set year tag: {clean_year}")
            except (ValueError, TypeError) as ex:
                print(f"WARNING: Failed to set year tag")
                print(f"  Invalid year format: {album_obj.release_year}")
                print(f"  Error: {str(ex)}")

        # Track title
        if "tracktitle" in music_file and album_obj.title_name is not None and album_obj.title_name.strip() != "":
            music_file["tracktitle"] = album_obj.title_name.strip()
            print(f"INFO: Set track title tag: {album_obj.title_name}")

        # Album title
        if album_obj.title_name is not None and album_obj.title_name.strip() != "":
            music_file["album"] = album_obj.title_name.strip()
            print(f"INFO: Set album tag: {album_obj.title_name}")

        # Genre
        if album_obj.genre is not None and album_obj.genre.strip() != "":
            music_file["genre"] = album_obj.genre.strip()
            print(f"INFO: Set genre tag: {album_obj.genre}")

        try:
            print(f"INFO: Saving changes to file: {album_obj.complete_file_path}")
            music_file.save()
            print(f"INFO: Successfully saved metadata changes")
        except Exception as ex:
            print(f"ERROR: Failed to save metadata changes")
            print(f"  File: {album_obj.complete_file_path}")
            print(f"  Error type: {type(ex).__name__}")
            print(f"  Error message: {str(ex)}")
            return None

    except Exception as ex:
        print(f"ERROR: Failed to set metadata")
        print(f"  File: {album_obj.complete_file_path}")
        print(f"  Error type: {type(ex).__name__}")
        print(f"  Error message: {str(ex)}")
        return None

    return True


def list_files(folder_path):
    """
    List all files contains in the folder and sub-folders.
    :param folder_path:
    :return: List[string]
    """
    file_list = []

    for current_dir, subdirs, files in os.walk(folder_path):
        for filename in files:
            relative_path = os.path.join(current_dir, filename)
            absolute_path = os.path.abspath(relative_path)
            file_list.append(absolute_path)

    return file_list


def get_album_from_file_path(file_path: string) -> Optional[AlbumObject]:
    """
    Get information from file name and adds to albumObject.
    Renames file with cleaned file name.
    :param file_path: Path to the music file
    :return: filled album object, null if error
    """
    try:
        album_object = objects.AlbumObject()
        album_object.complete_file_path = file_path
        album_object.file_name = os.path.basename(file_path)
        album_object.file_ending = album_object.file_name.endswith(file_path)

        folder_path: Path = Path(file_path).parent.absolute()

        # Clean file path from special characters
        original_file_path = file_path
        file_path = TextCleaner.clean_special_characters(file_path)
        if file_path != original_file_path:
            print(f"INFO: Cleaned special characters from file path")
            print(f"  Original: {original_file_path}")
            print(f"  Cleaned: {file_path}")

        # used in clean path for rename
        clean_file_separator = "-"

        separator: string = get_separator_from_filepath(file_path)
        if separator is None:
            print(f"ERROR: No valid separator found in file name")
            print(f"  Expected one of: -, –, or —")
            print(f"  File: {file_path}")
            return None

        # Split into artist name and album/track title
        seperator_index: int = file_path.find(separator)
        seperator_index_slash: int = file_path.rfind("/")

        if seperator_index <= seperator_index_slash:
            print(f"ERROR: Invalid file name format")
            print(f"  Separator found before last directory separator")
            print(f"  File: {file_path}")
            return None

        # Artist_name ---------
        artist_name: string = file_path[seperator_index_slash + 1:seperator_index - 1].strip()
        if not artist_name:
            print(f"ERROR: Empty artist name after parsing")
            print(f"  File: {file_path}")
            return None
            
        artist_name = TextCleaner.clean_special_characters(artist_name)
        album_object.artist_name = artist_name
        print(f"INFO: Extracted artist name: {artist_name}")

        album_object.file_ending = get_file_ending(file_path)
        if not album_object.file_ending:
            print(f"ERROR: No file extension found")
            print(f"  File: {file_path}")
            return None

        title_name: string = file_path[seperator_index + 1:].strip()
        if not title_name:
            print(f"ERROR: Empty title after parsing")
            print(f"  File: {file_path}")
            return None

        # Title ---------
        title_name = title_name.replace("  ", " ")
        title_name = title_name.replace("  ", " ")

        # Store original title for logging
        original_title = title_name

        title_name = re.sub(r"\[?\(?Full Album\)?]?", "", title_name, flags=re.IGNORECASE)
        title_name = re.sub(r"\[?\(?complete album\)?]?", "", title_name, flags=re.IGNORECASE)
        title_name = re.sub(r"\[?\(?High Quality\)?]?", "", title_name, flags=re.IGNORECASE)
        title_name = re.sub(r"(\[?\(?HQ\s?\)?]?)", "", title_name, flags=re.IGNORECASE)

        if title_name != original_title:
            print(f"INFO: Removed album/quality tags from title")
            print(f"  Original: {original_title}")
            print(f"  Cleaned: {title_name}")

        title_name = title_name.strip()
        file_ending_len = (len(album_object.file_ending))
        title_name = title_name[:(len(title_name) - file_ending_len)]

        album_object.title_name = title_name

        # Date ---------
        year_pattern: string = r"(?:\[|\()?\d{4}(?:\]|\))?"
        album_date_string: string = re.findall(year_pattern, title_name)
        if album_date_string:
            year = re.search(r"\d{4}", album_date_string[0]).group()
            album_object.release_year = year
            if len(album_date_string) > 1:
                print(f"INFO: Multiple years found in title, using first year: {year}")
                album_object.title_name = title_name
            else:
                album_object.title_name = re.sub(year_pattern, "", title_name)
                album_object.title_name = album_object.title_name.replace("-", "")
            print(f"INFO: Extracted release year: {year}")
        else:
            print(f"INFO: No release year found in file name: {file_path}")

        # Capitalization handling
        capital_latters_pattern: string = "[A-Z]{4,}"
        capital_latters_stings = re.findall(capital_latters_pattern, title_name)
        if capital_latters_stings:
            if len(capital_latters_stings) > 1:
                original_title = album_object.title_name
                album_object.title_name = album_object.title_name.title()
                print(f"INFO: Adjusted title capitalization")
                print(f"  Original: {original_title}")
                print(f"  Adjusted: {album_object.title_name}")

        print(f"INFO: Final title: {album_object.title_name}")

        # Genre ---------
        album_object.genre = folder_path.name
        print(f"INFO: Extracted genre from folder name: {album_object.genre}")

        # Create clean file name
        album_object.clean_file_name = (artist_name + " " + clean_file_separator + " "
                                      + album_object.title_name).strip() + album_object.file_ending

        destination_path: string = str(folder_path.absolute()) + "/" + album_object.clean_file_name

        # Rename file using clean file name
        try:
            if album_object.complete_file_path != destination_path:
                os.rename(album_object.complete_file_path, destination_path)
                print(f"INFO: Renamed file:")
                print(f"  From: {album_object.complete_file_path}")
                print(f"  To: {destination_path}")
                album_object.complete_file_path = destination_path
        except FileNotFoundError as ex:
            print(f"ERROR: File not found during rename")
            print(f"  From: {album_object.complete_file_path}")
            print(f"  To: {destination_path}")
            print(f"  Error: {str(ex)}")
            return None
        except FileExistsError as ex:
            print(f"ERROR: Destination file already exists")
            print(f"  From: {album_object.complete_file_path}")
            print(f"  To: {destination_path}")
            print(f"  Error: {str(ex)}")
            return None
        except Exception as ex:
            print(f"ERROR: Failed to rename file")
            print(f"  From: {album_object.complete_file_path}")
            print(f"  To: {destination_path}")
            print(f"  Error: {str(ex)}")
            return None

        return album_object
        
    except Exception as ex:
        print(f"ERROR: Unexpected error in get_album_from_file_path")
        print(f"  File: {file_path}")
        print(f"  Error type: {type(ex).__name__}")
        print(f"  Error message: {str(ex)}")
        return None


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
        print("WARN: No seperator in album file path! " + file_path)
        return None
    return separator
