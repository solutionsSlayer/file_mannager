import pytest
from unittest.mock import Mock, call
from typing import List
import os.path
from src.main import FileManager

class MockFileSelector:
    def __init__(self, selected_files: List[str]):
        self.selected_files = selected_files
        
    def get_selected_files(self) -> List[str]:
        return self.selected_files
        
    def clear_selection(self) -> None:
        self.selected_files = []

class MockFileSystem:
    def __init__(self):
        self.copied_files = []
        self.moved_files = []
        self.deleted_files = []
        
    def copy_file(self, source: str, destination: str) -> None:
        self.copied_files.append((source, destination))
        
    def move_file(self, source: str, destination: str) -> None:
        self.moved_files.append((source, destination))
        
    def delete_file(self, path: str) -> None:
        self.deleted_files.append(path)
        
    def file_exists(self, path: str) -> bool:
        return True
        
    def is_file(self, path: str) -> bool:
        return True
        
    def is_directory(self, path: str) -> bool:
        return False

    def delete_directory(self, path: str) -> None:
        self.deleted_files.append(path)

class TestFileManager:
    @pytest.fixture
    def setup(self):
        self.selected_files = [
            os.path.normpath("/path/file1.txt"),
            os.path.normpath("/path/file2.txt")
        ]
        self.file_selector = MockFileSelector(self.selected_files)
        self.file_system = MockFileSystem()
        self.file_manager = FileManager(self.file_selector, self.file_system)
        
    def test_copy_files(self, setup):
        # Arrange
        destination = os.path.normpath("/dest")
        
        # Act
        self.file_manager.copy_files(destination)
        
        # Assert
        expected_copies = [
            (os.path.normpath("/path/file1.txt"), os.path.join(destination, "file1.txt")),
            (os.path.normpath("/path/file2.txt"), os.path.join(destination, "file2.txt"))
        ]
        assert self.file_system.copied_files == expected_copies
        assert len(self.file_selector.selected_files) == 0  # Selection cleared
        
    def test_move_files(self, setup):
        # Arrange
        destination = os.path.normpath("/dest")
        
        # Act
        self.file_manager.move_files(destination)
        
        # Assert
        expected_moves = [
            (os.path.normpath("/path/file1.txt"), destination),
            (os.path.normpath("/path/file2.txt"), destination)
        ]
        assert self.file_system.moved_files == expected_moves
        assert len(self.file_selector.selected_files) == 0
        
    def test_delete_files(self, setup):
        # Act
        self.file_manager.delete_files()
        
        # Assert
        assert self.file_system.deleted_files == self.selected_files
        assert len(self.file_selector.selected_files) == 0
        
    def test_copy_files_no_selection(self, setup):
        # Arrange
        self.file_selector.clear_selection()
        destination = os.path.normpath("/dest")
        
        # Act
        self.file_manager.copy_files(destination)
        
        # Assert
        assert len(self.file_system.copied_files) == 0