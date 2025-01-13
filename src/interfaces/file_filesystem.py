from abc import ABC, abstractmethod

class IFileSystem(ABC):
    @abstractmethod
    def copy_file(self, source: str, destination: str) -> None:
        pass
    
    @abstractmethod
    def move_file(self, source: str, destination: str) -> None:
        pass
    
    @abstractmethod
    def delete_file(self, path: str) -> None:
        pass
    
    @abstractmethod
    def delete_directory(self, path: str) -> None:
        pass
    
    @abstractmethod
    def file_exists(self, path: str) -> bool:
        pass
    
    @abstractmethod
    def is_file(self, path: str) -> bool:
        pass
    
    @abstractmethod
    def is_directory(self, path: str) -> bool:
        pass