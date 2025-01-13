""" Interfaces """
from interfaces.file_selector import IFileSelector
from interfaces.file_filesystem import IFileSystem

""" Classes """
from core.file_explorer import FileExplorer
from core.file_manager import FileManager

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