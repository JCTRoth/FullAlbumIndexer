# This is a sample Python script.
from logic import list_files, get_album_from_file_path, get_file_ending, set_music_information

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    file_list = list_files('/home/jonas/Musik/Album')
    for i in file_list:
        print(i)

    example_path = "/home/jonas/Musik/Album/ElectronicMusic/Gorillaz - Cracker Island (Full Album) 2023.opus"
    # get_file_ending(example_path)
    album = get_album_from_file_path(example_path)
    set_music_information(album)

    example_path = "/home/jonas/Musik/Album/ElectronicMusic/DieselBoy - Future Sound of Hardcore (A Side) (1994).opus"
    # get_file_ending(example_path)
    album = get_album_from_file_path(example_path)
    set_music_information(album)

    # TODO RETURN LIST OF MUSIC FILES WITH NOT CORRECT FORMATION

    # TODO ADD TESTS
