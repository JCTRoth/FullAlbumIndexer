import unittest
import os
from pathlib import Path
from logic.main import run
from logic.tests.tests import create_test_files, delete_all_files_in_folder


class TestMain(unittest.TestCase):
    def setUp(self):
        """Set up test environment before each test"""
        self.test_folder_path = './logic/tests/test_folder'
        if not Path(self.test_folder_path).exists():
            os.mkdir(self.test_folder_path)
        self.test_folder = Path(self.test_folder_path).absolute()
        create_test_files(self.test_folder)

    def tearDown(self):
        """Clean up test environment after each test"""
        delete_all_files_in_folder(self.test_folder)

    def test_run_with_test_files(self):
        """Test the main run function with test files"""
        try:
            run(self.test_folder)
            # If we reach this point without exceptions, consider the test passed
            self.assertTrue(True)
        except Exception as e:
            self.fail(f"run() raised an exception: {str(e)}")


if __name__ == '__main__':
    unittest.main() 