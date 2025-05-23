#!/usr/bin/env python3

import argparse
import sys
from dataclasses import dataclass
from logic.album_logic import list_files, get_album_from_file_path, set_music_information


@dataclass
class ProcessingSummary:
    """Class to track file processing statistics"""
    total_files: int = 0
    processed_files: int = 0
    skipped_files: int = 0
    error_files: int = 0

    def display(self):
        """Display the processing summary in a formatted way"""
        print("\n" + "=" * 50)
        print("Processing Summary")
        print("=" * 50)
        print(f"Total files found:      {self.total_files}")
        print(f"Successfully processed: {self.processed_files}")
        print(f"Skipped:               {self.skipped_files}")
        print(f"Errors:                {self.error_files}")
        print("=" * 50)


def run(folder_path: str, recursive: bool = False, dry_run: bool = False, verbose: bool = False) -> None:
    """
    Main function to process music files in a folder.
    
    Args:
        folder_path (str): Path to the folder containing music files
        recursive (bool): Whether to process subfolders recursively
        dry_run (bool): If True, show what would be done without making changes
        verbose (bool): If True, show detailed processing information
    """
    if verbose:
        print(f"Processing folder: {folder_path}")
        if dry_run:
            print("Dry run mode - no changes will be made")
        if recursive:
            print("Processing recursively")

    # Initialize summary tracking
    summary = ProcessingSummary()

    # Get list of files to process
    files = list_files(folder_path)
    summary.total_files = len(files)
    
    if verbose:
        print(f"Found {len(files)} files to process")

    for file_path in files:
        if verbose:
            print(f"\nProcessing file: {file_path}")

        try:
            # Get album information from file name
            album_obj = get_album_from_file_path(file_path)
            
            if album_obj is None:
                if verbose:
                    print(f"Skipping {file_path} - could not parse file name")
                summary.skipped_files += 1
                continue

            if dry_run:
                print("\nWould set the following metadata:")
                print(f"  Artist: {album_obj.artist_name}")
                print(f"  Title: {album_obj.title_name}")
                print(f"  Year: {album_obj.release_year}")
                print(f"  Genre: {album_obj.genre}")
                print(f"  Clean filename: {album_obj.clean_file_name}")
                summary.processed_files += 1
            else:
                # Set music information in the file
                result = set_music_information(album_obj)
                if result is None:
                    summary.error_files += 1
                else:
                    summary.processed_files += 1

        except Exception as e:
            if verbose:
                print(f"Error processing {file_path}: {str(e)}")
            summary.error_files += 1

    if verbose:
        print("\nProcessing complete")
    
    # Display the summary
    summary.display()


def main():
    """
    Command line interface for the Full Album Indexer.
    Run this script directly to process music files.
    
    Example usage:
        ./main.py /path/to/music/folder -rv
        python main.py --dry-run /path/to/music/folder
    """
    parser = argparse.ArgumentParser(
        description='Index and organize full album music files, setting proper metadata tags.'
    )
    parser.add_argument(
        'folder_path',
        help='Path to the folder containing music files to process'
    )
    parser.add_argument(
        '--recursive', '-r',
        action='store_true',
        help='Process folders recursively'
    )
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Show what would be done without making any changes'
    )
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Show detailed processing information'
    )

    args = parser.parse_args()

    try:
        run(
            folder_path=args.folder_path,
            recursive=args.recursive,
            dry_run=args.dry_run,
            verbose=args.verbose
        )
    except Exception as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()