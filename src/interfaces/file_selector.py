from abc import ABC, abstractmethod
from typing import List

class IFileSelector(ABC):
    @abstractmethod
    def load_directory_contents(self, directory_path: str) -> List[str]:
        pass
    
    @abstractmethod
    def select_files_by_indices(self, indices: str, directory_path: str) -> List[str]:
        pass
    
    @abstractmethod
    def get_selected_files(self) -> List[str]:
        pass
    
    @abstractmethod
    def clear_selection(self) -> None:
        pass 