from abc import ABC, abstractmethod
from typing import List, Any


class CommentRepository(ABC):
    @abstractmethod
    def add(self, user_id: int, target_user_id: int, text: str) -> int:
        raise NotImplementedError

    @abstractmethod
    def get_by_target(self, target_user_id: int) -> List[Any]:
        raise NotImplementedError
