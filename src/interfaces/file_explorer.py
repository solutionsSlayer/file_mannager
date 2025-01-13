from abc import ABC, abstractmethod

""" Interfaces """
from interfaces.file_selector import IFileSelector

class IFileExplorer(ABC):
    @abstractmethod
    def display_directory_contents(self, file_selector: IFileSelector) -> None:
        pass
    
    @abstractmethod
    def navigate(self, index: int, file_selector: IFileSelector) -> None:
        pass
    
    @abstractmethod
    def go_to_parent_directory(self, file_selector: IFileSelector) -> None:
        pass

    @abstractmethod
    def get_current_path(self) -> str:
        pass