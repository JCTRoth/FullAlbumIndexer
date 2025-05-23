#!/usr/bin/env python3

import unittest
import os
import shutil
from pathlib import Path
from unittest.mock import patch, MagicMock

from main import run
from logic.album_logic import get_album_from_file_path, set_music_information
from logic.objects import AlbumObject


class TestAlbumIndexer(unittest.TestCase):
    def setUp(self):
        """Set up test environment before each test"""
        self.test_folder_path = Path('./logic/tests/test_folder')
        if not self.test_folder_path.exists():
            os.makedirs(self.test_folder_path)
        print(f"\nSetting up test environment in {self.test_folder_path}")

    def tearDown(self):
        """Clean up test environment after each test"""
        if self.test_folder_path.exists():
            shutil.rmtree(self.test_folder_path)
        print("Cleaned up test environment")

    def create_test_file(self, file_name: str) -> bool:
        """Create a test file with given name"""
        try:
            file_path = self.test_folder_path / file_name
            # Get the directory where this test file is located
            current_dir = Path(__file__).parent
            empty_opus_path = current_dir / "emptyOpusFile.opus"
            shutil.copy(str(empty_opus_path), str(file_path))
            return True
        except Exception as ex:
            print(f"ERROR: Create empty file: {str(ex)}")
            return False

    def test_file_name_parsing(self):
        """Test parsing of different file name formats"""
        print("\nTesting file name parsing...")
        test_cases = [
            {
                "filename": "Test - Normal Path 2023.opus",
                "expected": {
                    "artist": "Test",
                    "title": "Normal Path",
                    "year": "2023"
                }
            },
            {
                "filename": "T.e.s.t - N.o.r.m.a.l P.a.t.h 2.0.2.3.opus",
                "expected": {
                    "artist": "T.e.s.t",
                    "title": "N.o.r.m.a.l P.a.t.h 2.0.2.3"
                }
            },
            {
                "filename": "Test - 1999 2023.opus",
                "expected": {
                    "artist": "Test",
                    "title": "1999 2023",
                    "year": "1999"
                }
            },
            {
                "filename": "Test - 1999-2016 2023.opus",
                "expected": {
                    "artist": "Test",
                    "title": "1999-2016 2023",
                    "year": "1999"
                }
            },
            {
                "filename": "R̲o̲b̲b̲i̲e̲ W̲i̲l̲l̲i̲a̲m̲s̲ - L̲i̲f̲e̲ T̲h̲r̲u̲ A̲ L̲e̲n̲s̲.opus",
                "expected": {
                    "artist": "Robbie Williams",
                    "title": "Life Thru A Lens"
                }
            },
            {
                "filename": "Th̲e Cur̲e̲ – Thre̲e̲ Imagi̲n̲ary B̲oys.opus",
                "expected": {
                    "artist": "The Cure",
                    "title": "Three Imaginary Boys"
                }
            },
            {
                "filename": "B̤ṳf̤f̤a̤l̤o̤ ̤V̤o̤l̤c̤a̤n̤i̤c̤ ̤- R̤o̤c̤k̤ 1973.opus",
                "expected": {
                    "artist": "Buffalo Volcanic",
                    "title": "Rock",
                    "year": "1973"
                }
            },
            {
                "filename": "The Beatles - Magical Mystery Tour [Full Album] (1967).opus",
                "expected": {
                    "artist": "The Beatles",
                    "title": "Magical Mystery Tour",
                    "year": "1967"
                }
            },
            {
                "filename": "Tschaikowsky - Nocturne d-Moll ∙ hr-Sinfonieorchester ∙ Mischa Maisky ∙ Paavo Järvi.opus",
                "expected": {
                    "artist": "Tschaikowsky",
                    "title": "Nocturne d-Moll hr-Sinfonieorchester Mischa Maisky Paavo Järvi"
                }
            }
        ]

        for test_case in test_cases:
            print(f"\nTesting filename: {test_case['filename']}")
            self.create_test_file(test_case["filename"])
            file_path = str(self.test_folder_path / test_case["filename"])
            result = get_album_from_file_path(file_path)
            self.assertIsNotNone(result)
            self.assertEqual(result.artist_name, test_case["expected"]["artist"])
            self.assertEqual(result.title_name.strip(), test_case["expected"]["title"])
            if "year" in test_case["expected"]:
                self.assertEqual(result.release_year, test_case["expected"]["year"])

    def test_special_characters_handling(self):
        """Test handling of special characters in filenames"""
        print("\nTesting special character handling...")
        test_files = [
            ("Th̲e Cur̲e̲ – Thre̲e̲ Imagi̲n̲ary B̲oys.opus", "The Cure - Three Imaginary Boys.opus"),
            ("B̤ṳf̤f̤a̤l̤o̤ ̤V̤o̤l̤c̤a̤n̤i̤c̤ ̤- R̤o̤c̤k̤ 1973.opus", "Buffalo Volcanic - Rock.opus"),
            ("Tschaikowsky - Nocturne d-Moll ∙ hr-Sinfonieorchester ∙ Mischa Maisky ∙ Paavo Järvi.opus",
             "Tschaikowsky - Nocturne d-Moll hr-Sinfonieorchester Mischa Maisky Paavo Järvi.opus")
        ]

        for original, expected in test_files:
            print(f"\nTesting filename: {original}")
            self.create_test_file(original)
            file_path = str(self.test_folder_path / original)
            result = get_album_from_file_path(file_path)
            self.assertIsNotNone(result)
            self.assertEqual(result.clean_file_name, expected)
            # Verify special characters are removed
            self.assertNotIn("̲", result.clean_file_name)
            self.assertNotIn("̤", result.clean_file_name)
            self.assertNotIn("∙", result.clean_file_name)

    def test_full_album_tag_removal(self):
        """Test removal of [Full Album] and similar tags"""
        print("\nTesting full album tag removal...")
        test_cases = [
            {
                "filename": "Artist - Album [Full Album].opus",
                "expected_title": "Album"
            },
            {
                "filename": "Artist - Album (Full Album).opus",
                "expected_title": "Album"
            },
            {
                "filename": "Artist - Album [Complete Album].opus",
                "expected_title": "Album"
            },
            {
                "filename": "Artist - Album [HQ].opus",
                "expected_title": "Album"
            },
            {
                "filename": "Artist - Album (High Quality).opus",
                "expected_title": "Album"
            },
                        {
                "filename": "Artist - Album.mp3",
                "expected_title": "Album"
            }
        ]

        for test_case in test_cases:
            print(f"\nTesting filename: {test_case['filename']}")
            self.create_test_file(test_case["filename"])
            file_path = str(self.test_folder_path / test_case["filename"])
            result = get_album_from_file_path(file_path)
            self.assertIsNotNone(result)
            self.assertEqual(result.title_name.strip(), test_case["expected_title"])

    def test_capitalization_handling(self):
        """Test handling of different capitalization patterns"""
        print("\nTesting capitalization handling...")
        test_cases = [
            {
                "filename": "THE BAND - THE ALBUM NAME.opus",
                "expected": {
                    "artist": "THE BAND",
                    "title": "The Album Name"
                }
            },
            {
                "filename": "CAPITALS BAND - ALL CAPS ALBUM NAME.opus",
                "expected": {
                    "artist": "CAPITALS BAND",
                    "title": "All Caps Album Name"
                }
            }
        ]

        for test_case in test_cases:
            print(f"\nTesting filename: {test_case['filename']}")
            self.create_test_file(test_case["filename"])
            file_path = str(self.test_folder_path / test_case["filename"])
            result = get_album_from_file_path(file_path)
            self.assertIsNotNone(result)
            self.assertEqual(result.artist_name, test_case["expected"]["artist"])
            self.assertEqual(result.title_name.strip(), test_case["expected"]["title"])


def run_tests():
    """Run all tests with detailed output"""
    print("Starting Album Indexer Tests...")
    print("=" * 50)
    
    # Create a test suite
    suite = unittest.TestLoader().loadTestsFromTestCase(TestAlbumIndexer)
    
    # Run the tests with verbosity
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    print("\nTest Summary:")
    print("=" * 50)
    print(f"Tests Run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print(f"Skipped: {len(result.skipped)}")
    
    return result.wasSuccessful()


if __name__ == '__main__':
    success = run_tests()
    # Exit with appropriate status code
    exit(0 if success else 1) 