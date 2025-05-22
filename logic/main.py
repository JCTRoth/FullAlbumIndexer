import string
from logic.album_logic import list_files, get_album_from_file_path, set_music_information


def run(folder_path: string):
    """
    Process all music files in the given folder path.
    Updates metadata and cleans filenames for each music file found.
    
    Args:
        folder_path: Path to the folder containing music files
    """
    file_list = list_files(folder_path)
    for i in file_list:
        print(i)
        album_data = get_album_from_file_path(i)
        set_music_information(album_data)
        print("---------------------------")


if __name__ == '__main__':
    # Example usage:
    run('/path/to/your/music/folder')
    pass