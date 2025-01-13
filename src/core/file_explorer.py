""" System modules """
import os

""" Interfaces """
from interfaces.file_explorer import IFileExplorer
from interfaces.file_selector import IFileSelector

class FileExplorer(IFileExplorer):
    def __init__(self):
        self.current_path = os.path.expanduser('~')

    def display_directory_contents(self, file_selector: IFileSelector):
        """Display contents of the current directory"""
        try:
            contents = file_selector.load_directory_contents(self.current_path)
            print(f"\nCurrent Directory: {self.current_path}")
            print("-" * 50)
            for index, element in enumerate(contents):
                full_path = os.path.join(self.current_path, element)
                element_type = "📁 Folder" if os.path.isdir(full_path) else "📄 File"
                print(f"{index}. {element_type}: {element}")
        except PermissionError:
            print("Access denied to this directory.")
        except Exception as e:
            print(f"Error: {e}")

    def navigate(self, index: int, file_selector: IFileSelector):
        """Navigate to a subdirectory"""
        try:
            contents = os.listdir(self.current_path)
            selected_element = contents[index]
            full_path = os.path.join(self.current_path, selected_element)
            
            if os.path.isdir(full_path):
                self.current_path = full_path
                self.display_directory_contents(file_selector)
            else:
                print(f"Cannot open file {selected_element}")
        except Exception as e:
            print(f"Navigation error: {e}")

    def go_to_parent_directory(self, file_selector: IFileSelector):
        """Move to the parent directory"""
        self.current_path = os.path.dirname(self.current_path)
        self.display_directory_contents(file_selector)

    def get_current_path(self):
        """Return the current directory path"""
        return self.current_path