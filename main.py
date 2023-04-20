import objects
from logic import list_files, get_album_from_file_path, set_music_information

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    file_list = list_files('/home/jonas/Musik/A13/Music/Album')
    for i in file_list:
        print(i)
        album_data: objects.AlbumObject = get_album_from_file_path(i)
        set_music_information(album_data)
        print("---------------------------")

    # example_path = "/home/jonas/Musik/Album/ElectronicMusic/Gorillaz - Cracker Island (Full Album) 2023.opus"
    # get_file_ending(example_path)
    # album = get_album_from_file_path(example_path)
    # if album != None:
    #    set_music_information(album)

    # TODO RETURN LIST OF MUSIC FILES WITH NOT CORRECT FORMATION

    # TODO ADD TESTS - add attrappen files

    # TODO ADD MODE FOR SINGLE TRACKS

    # TODO ADD MODE FOR ALBUMS WITH SEPARATED FILES IN ONE FOLDER
