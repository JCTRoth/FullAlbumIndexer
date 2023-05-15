import string
import time
import objects
import tests
from album_logic import list_files, get_album_from_file_path, set_music_information


# Press the green button in the gutter to run the script.
def run(folderpath: string):
    file_list = list_files(folderpath)
    for i in file_list:
        print(i)
        album_data: objects.AlbumObject = get_album_from_file_path(i)
        set_music_information(album_data)
        print("---------------------------")


if __name__ == '__main__':

    folderPath: string = '/home/jonas/Musik/Album_Project/Test/Tests/'
    tests.create_test_files(folderPath)
    run(folderPath)

    # run('/home/jonas/Musik/A13/Music/Album/Test')

    # example_path = "/home/jonas/Musik/Album/ElectronicMusic/Gorillaz - Cracker Island (Full Album) 2023.opus"
    # get_file_ending(example_path)
    # album = get_album_from_file_path(example_path)
    # if album != None:
    #    set_music_information(album)

    # TODO RETURN LIST OF MUSIC FILES WITH NOT CORRECT FORMATION

    # TODO ADD TESTS - add attrappen files

    # TODO ADD MODE FOR SINGLE TRACKS

    # TODO ADD MODE FOR ALBUMS WITH SEPARATED FILES IN ONE FOLDER
