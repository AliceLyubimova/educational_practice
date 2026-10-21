from abc import ABC, abstractmethod
from typing import List, Any


class LikeRepository(ABC):

    @abstractmethod
    def add(self, from_user_id: int, to_user_id: int) -> bool:
        """Добавить лайк."""
        raise NotImplementedError

    @abstractmethod
    def get_received(self, user_id: int) -> List[Any]:
        """Кто лайкнул этого пользователя."""
        raise NotImplementedError

    @abstractmethod
    def get_given(self, user_id: int) -> List[Any]:
        """Кого лайкнул этот пользователь."""
        raise NotImplementedError

    @abstractmethod
    def is_match(self, user1_id: int, user2_id: int) -> bool:
        """Проверить взаимный лайк."""
        raise NotImplementedError

    @abstractmethod
    def get_matches(self, user_id: int) -> List[Any]:
        """Получить все мэтчи."""
        raise NotImplementedError
