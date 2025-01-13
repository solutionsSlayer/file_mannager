""" System modules """
import os
import shutil

""" Interfaces """
from interfaces.file_selector import IFileSelector
from interfaces.file_filesystem import IFileSystem

""" File Manager Console Application 
    Generated with Claude 3.5 Haiku
    With 2 prompts : 
        Génère un programme console python qui permet d'explorer les fichiers, 
        en sélectionner pour copier, déplacer et supprimer les fichiers sélectionnés. 
        Une classe "métier" regroupe les fonctions de sélection, copie, déplacement 
        et suppression.

        Deux rectifications : il faudrait passer le code et l'interface en anglais 
        et sortir la sélection de la classe "métier"
"""


class FileSelector(IFileSelector):
    def __init__(self):
        self.selected_files = []
        self.current_directory_contents = []

    def load_directory_contents(self, directory_path):
        """Load the contents of a directory"""
        try:
            self.current_directory_contents = os.listdir(directory_path)
            return self.current_directory_contents
        except Exception as e:
            print(f"Error loading directory contents: {e}")
            return []

    def select_files_by_indices(self, indices, directory_path):
        """Select files based on indices"""
        try:
            # Convert input string to list of indices
            selected_indices = [int(i.strip()) for i in indices.split(',')]
            
            # Reset previous selection
            self.selected_files.clear()
            
            # Select files
            for index in selected_indices:
                if 0 <= index < len(self.current_directory_contents):
                    full_path = os.path.join(directory_path, self.current_directory_contents[index])
                    self.selected_files.append(full_path)
            
            print("Selected files:")
            for file in self.selected_files:
                print(f" - {os.path.basename(file)}")
            
            return self.selected_files
        except ValueError:
            print("Invalid input. Please enter valid indices.")
            return []
        except Exception as e:
            print(f"Error selecting files: {e}")
            return []

    def get_selected_files(self):
        """Return the list of currently selected files"""
        return self.selected_files

    def clear_selection(self):
        """Clear the current file selection"""
        self.selected_files.clear()


class FileExplorer:
    def __init__(self):
        self.current_path = os.path.expanduser('~')

    def display_directory_contents(self, file_selector):
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

    def navigate(self, index, file_selector):
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

    def go_to_parent_directory(self, file_selector):
        """Move to the parent directory"""
        self.current_path = os.path.dirname(self.current_path)
        self.display_directory_contents(file_selector)

    def get_current_path(self):
        """Return the current directory path"""
        return self.current_path


class DefaultFileSystem(IFileSystem):
    def copy_file(self, source: str, destination: str) -> None:
        shutil.copy2(source, destination)
    
    def move_file(self, source: str, destination: str) -> None:
        shutil.move(source, destination)
    
    def delete_file(self, path: str) -> None:
        os.remove(path)
    
    def delete_directory(self, path: str) -> None:
        shutil.rmtree(path)
    
    def file_exists(self, path: str) -> bool:
        return os.path.exists(path)
    
    def is_file(self, path: str) -> bool:
        return os.path.isfile(path)
    
    def is_directory(self, path: str) -> bool:
        return os.path.isdir(path)


class FileManager:
    def __init__(self, file_selector: FileSelector, file_system: IFileSystem):
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


class CommandHandler:
    def __init__(self):
        self.file_selector = FileSelector()
        self.file_explorer = FileExplorer()
        self.file_system = DefaultFileSystem()
        self.file_manager = FileManager(self.file_selector, self.file_system)
        self.commands = {
            '1': self.display_directory,
            '2': self.navigate,
            '3': self.go_to_parent,
            '4': self.select_files,
            '5': self.copy_files,
            '6': self.move_files,
            '7': self.delete_files,
            '8': self.show_help,
            '9': self.quit
        }
        self.running = True

    def display_directory(self):
        self.file_explorer.display_directory_contents(self.file_selector)

    def navigate(self):
        index = int(input("Enter navigation index: "))
        self.file_explorer.navigate(index, self.file_selector)

    def go_to_parent(self):
        self.file_explorer.go_to_parent_directory(self.file_selector)

    def select_files(self):
        self.file_explorer.display_directory_contents(self.file_selector)
        indices = input("Enter file indices to select (comma-separated): ")
        self.file_selector.select_files_by_indices(indices, self.file_explorer.get_current_path())

    def copy_files(self):
        dest = input("Enter destination path for copying: ")
        self.file_manager.copy_files(dest)

    def move_files(self):
        dest = input("Enter destination path for moving: ")
        self.file_manager.move_files(dest)

    def delete_files(self):
        self.file_manager.delete_files()

    def show_help(self):
        """Display help information about commands"""
        print("\n=== File Explorer Help ===")
        print("Available commands:")
        print("1. Display Directory - Shows the contents of current directory")
        print("2. Navigate - Enter an index to open a folder")
        print("3. Go to Parent Directory - Move up one level in directory tree")
        print("4. Select Files - Choose files for operations:")
        print("   - Enter indices separated by commas (e.g., 0,1,3)")
        print("   - Selected files will be used for copy/move/delete operations")
        print("5. Copy - Copy selected files to a destination path")
        print("6. Move - Move selected files to a destination path")
        print("7. Delete - Remove selected files/folders permanently")
        print("8. Help - Display this help message")
        print("9. Quit - Exit the application")
        print("\nTypical workflow:")
        print("1. Use Display Directory to see files")
        print("2. Select files using their indices")
        print("3. Perform an operation (copy/move/delete)")
        print("\nNote: You must select files before copying, moving, or deleting")

    def quit(self):
        print("Goodbye!")
        self.running = False

    def display_menu(self):
        print("\n--- File Explorer ---")
        print("1. Display Directory")
        print("2. Navigate")
        print("3. Go to Parent Directory")
        print("4. Select Files")
        print("5. Copy")
        print("6. Move")
        print("7. Delete")
        print("8. Help")
        print("9. Quit")

    def execute_command(self, choice):
        if choice in self.commands:
            try:
                self.commands[choice]()
            except Exception as e:
                print(f"An error occurred: {e}")
        else:
            print("Invalid choice")

    def run(self):
        while self.running:
            self.display_menu()
            choice = input("Your choice: ")
            self.execute_command(choice)


def main_menu():
    command_handler = CommandHandler()
    command_handler.run()

if __name__ == "__main__":
    main_menu()