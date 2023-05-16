import os
import string
import time
from pathlib import Path

import objects
import tests
from album_logic import list_files, get_album_from_file_path, set_music_information


# Press the green button in the gutter to run the script.
def run(folder_path: string):
    file_list = list_files(folder_path)
    for i in file_list:
        print(i)
        album_data: objects.AlbumObject = get_album_from_file_path(i)
        set_music_information(album_data)
        print("---------------------------")


if __name__ == '__main__':

    testFolderPathString: string = './test_folder'

    # Run Test
    # Tests on real opus/music files if it is possible to set the tags.
    # Deletes test files after test again, so test runs can be done without any future action.
    if not Path(testFolderPathString).exists():
        os.mkdir(testFolderPathString)
    testFolderPath: Path = Path(testFolderPathString).absolute()
    tests.create_test_files(testFolderPath)
    run(testFolderPath)
    tests.delete_all_files_in_folder(testFolderPath)

    # run('/home/jonas/Musik/A13/Music/Album/Test')








#TODO RETURN LIST OF MUSIC FILES WITH NOT CORRECT FORMATION

#TODO ADD MODE FOR SINGLE TRACKS

#TODO ADD MODE FOR ALBUMS WITH SEPARATED FILES IN ONE FOLDER