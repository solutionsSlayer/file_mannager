""" System modules """
import os

""" Interfaces """
from interfaces.file_selector import IFileSelector
from interfaces.file_filesystem import IFileSystem

class FileManager:
    def __init__(self, file_selector: IFileSelector, file_system: IFileSystem):
        self.file_selector = file_selector
        self.file_system = file_system

    def copy_files(self, destination):
        """Copy selected files"""
        try:
            selected_files = self.file_selector.get_selected_files()
            if not selected_files:
                print("No files selected. Please select files first.")
                return
                
            if not os.path.exists(destination):
                print(f"Creating destination directory: {destination}")
                os.makedirs(destination)
                
            copied_count = 0
            for file in selected_files:
                if self.file_system.file_exists(file):
                    dest_path = os.path.join(destination, os.path.basename(file))
                    self.file_system.copy_file(file, dest_path)
                    copied_count += 1
                else:
                    print(f"Warning: Source file not found - {file}")
                    
            print(f"{copied_count} file(s) copied successfully")
            self.file_selector.clear_selection()
        except Exception as e:
            print(f"Copy error: {e}")

    def move_files(self, destination):
        """Move selected files"""
        try:
            selected_files = self.file_selector.get_selected_files()
            for file in selected_files:
                if self.file_system.file_exists(file):
                    self.file_system.move_file(file, destination)
            print(f"{len(selected_files)} file(s) moved")
            self.file_selector.clear_selection()
        except Exception as e:
            print(f"Move error: {e}")

    def delete_files(self):
        """Delete selected files"""
        try:
            selected_files = self.file_selector.get_selected_files()
            for file in selected_files:
                if self.file_system.is_file(file):
                    self.file_system.delete_file(file)
                elif self.file_system.is_directory(file):
                    self.file_system.delete_directory(file)
            print(f"{len(selected_files)} file(s)/folder(s) deleted")
            self.file_selector.clear_selection()
        except Exception as e:
            print(f"Delete error: {e}")