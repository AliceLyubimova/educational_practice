from abc import ABC, abstractmethod
from typing import Optional, Dict


class WeightRepository(ABC):

    @abstractmethod
    def save(self, user_id: int, weights: Dict[str, float]) -> None:
        """Сохранить веса критериев."""
        raise NotImplementedError

    @abstractmethod
    def get(self, user_id: int) -> Optional[Dict[str, float]]:
        """Получить веса пользователя."""
        raise NotImplementedError

    @abstractmethod
    def get_or_default(self, user_id: int, defaults: Dict[str, float]) -> Dict[str, float]:
        """Получить веса или стандартные"""
        raise NotImplementedError
