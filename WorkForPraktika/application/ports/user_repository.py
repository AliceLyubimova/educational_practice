from abc import ABC, abstractmethod
from typing import List, Optional, Dict, Any


class UserRepository(ABC):
    

    @abstractmethod
    def get_all_active(self) -> List[Any]:
        
        raise NotImplementedError

    @abstractmethod
    def get_by_id(self, user_id: int) -> Optional[Any]:
        """Найти пользователя по ID."""
        raise NotImplementedError

    @abstractmethod
    def get_by_email(self, email: str) -> Optional[Any]:
        """Найти пользователя по email."""
        raise NotImplementedError

    @abstractmethod
    def create(self, user_data: Dict[str, Any]) -> int:
        """Создать пользователя"""
        raise NotImplementedError

    @abstractmethod
    def update(self, user_id: int, fields: Dict[str, Any]) -> bool:
        """Обновить поля """
        raise NotImplementedError

    @abstractmethod
    def deactivate(self, user_id: int) -> bool:
        """удаление пользователя."""
        raise NotImplementedError

    @abstractmethod
    def to_profile_dict(self, user: Any) -> Dict[str, Any]:
        raise NotImplementedError
