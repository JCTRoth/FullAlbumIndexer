#!/usr/bin/env python3

import argparse
import sys
import os
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
    Process music files in the specified folder.
    
    Args:
        folder_path: Path to the folder containing music files
        recursive: Whether to process subfolders
        dry_run: If True, only show what would be done without making changes
        verbose: If True, show detailed processing information
    """
    summary = ProcessingSummary()
    
    # Get list of files to process
    try:
        files = list_files(folder_path) if recursive else [
            os.path.join(folder_path, f) for f in os.listdir(folder_path)
            if os.path.isfile(os.path.join(folder_path, f))
        ]
        summary.total_files = len(files)
        if verbose:
            print(f"\nFound {len(files)} files to process in {folder_path}")
            if recursive:
                print("Processing recursively through subfolders")
    except Exception as e:
        print(f"ERROR: Failed to list files in {folder_path}: {str(e)}")
        return

    for file_path in files:
        if verbose:
            print(f"\n{'='*50}")
            print(f"Processing file: {file_path}")

        try:
            # Get album information from file name
            album_obj = get_album_from_file_path(file_path)
            
            if album_obj is None:
                if verbose:
                    print(f"SKIP: Could not parse file name. Possible issues:")
                    print(f"  - No valid separator found (-, –, or —)")
                    print(f"  - File name does not match expected format: Artist - Title")
                    print(f"  - Special characters could not be processed")
                    print(f"Original file: {os.path.basename(file_path)}")
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
                    if verbose:
                        print(f"ERROR: Failed to set metadata for {file_path}")
                        print("  - Check if file is write-protected")
                        print("  - Verify file is a valid audio format")
                        print("  - Ensure sufficient disk space")
                    summary.error_files += 1
                else:
                    if verbose:
                        print(f"SUCCESS: Updated metadata and renamed file")
                        print(f"  From: {os.path.basename(file_path)}")
                        print(f"  To: {album_obj.clean_file_name}")
                    summary.processed_files += 1

        except Exception as e:
            if verbose:
                print(f"ERROR: Unexpected error processing {file_path}")
                print(f"  Error type: {type(e).__name__}")
                print(f"  Error message: {str(e)}")
                print("  Stack trace:")
                import traceback
                print('    ' + '\n    '.join(traceback.format_exc().split('\n')))
            summary.error_files += 1

    if verbose:
        print(f"\n{'='*50}")
        print("Processing complete")
    
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