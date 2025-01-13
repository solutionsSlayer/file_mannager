""" System modules """
import os
import shutil

""" Interfaces """
from interfaces.file_filesystem import IFileSystem

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