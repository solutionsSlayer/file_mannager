# Python File Explorer

A command-line file management application that allows users to explore directories and perform operations like copying, moving, and deleting files.

## Features

- 📁 Directory navigation and exploration
- ✅ Multiple file selection
- 📋 File operations:
  - Copy files/folders
  - Move files/folders
  - Delete files/folders
- 🔍 Interactive menu interface
- 🛡️ Error handling and user feedback
- 🎯 Interface-driven architecture

## Requirements

- Python >= 3.7
- pytest >= 7.0.0
- typing >= 3.7.4

## Installation

1. Clone the repository
2. Install dependencies:

```bash
pip install -r requirements.txt
```

## Usage

To run the application, use the following command:

```bash
python main.py
```

### Available Commands

- `1`: Display the current directory
- `2`: Navigate to a subdirectory
- `3`: Go back to the parent directory
- `4`: Select files/folders
- `5`: Copy selected files/folders
- `6`: Move selected files/folders
- `7`: Delete selected files/folders
- `8`: Show help
- `9`: Quit

### Typical Workflow

1. Use "Display Directory" to view files
2. Select files using their indices (comma-separated)
3. Perform desired operation (copy/move/delete)

## Project Structure

src/
├── core/
│ ├── command_handler.py - Command processing and menu interface
│ ├── file_explorer.py - Directory navigation and display
│ ├── file_manager.py - File operations implementation
│ └── file_system.py - Filesystem operations wrapper
├── interfaces/
│ ├── file_explorer.py - Explorer interface definition
│ ├── file_filesystem.py - Filesystem interface definition
│ └── file_selector.py - File selection interface definition
└── main.py - Application entry point

## Testing

The project includes unit tests using pytest. Run tests with:

```bash
pytest
```

## Architecture

The application follows interface-driven development with clear separation of concerns:

- **IFileExplorer**: Handles directory navigation and content display
- **IFileSystem**: Abstracts filesystem operations
- **IFileSelector**: Manages file selection functionality
- **FileManager**: Coordinates file operations using the interfaces
- **CommandHandler**: Processes user input and manages the application flow

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is open source and available under the MIT License.
