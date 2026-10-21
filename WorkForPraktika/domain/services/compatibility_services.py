from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Dict, List, Any, Optional, Union
from enum import Enum

#Типы критериев
class CriterionType(Enum):
    """
    Тип критерия определяет, как вычислять сходство.

    Это БИЗНЕС-КЛАССИФИКАЦИЯ: она диктует правила,
    а не технические детали.
    """
    NUMERIC = "numeric"  # возраст, доход, внешность (шкала 1-10)
    CATEGORICAL = "categorical"  # пол, город, образование, религия (точное совпадение)
    MULTISET = "multiset"  # интересы, хобби (пересечение множеств)
    UNKNOWN = "unknown" 


@dataclass(frozen=True)
class CriterionValue:
    raw_value: Any

    @property
    def is_empty(self) -> bool:
        """Значение отсутствует или пустое"""
        if self.raw_value is None:
            return True
        if isinstance(self.raw_value, list) and len(self.raw_value) == 0:
            return True
        if isinstance(self.raw_value, str) and not self.raw_value.strip():
            return True
        return False

    def infer_type(self) -> CriterionType:
        if self.is_empty:
            return CriterionType.UNKNOWN
        if isinstance(self.raw_value, (int, float)):
            return CriterionType.NUMERIC
        if isinstance(self.raw_value, list):
            return CriterionType.MULTISET
        return CriterionType.CATEGORICAL


@dataclass(frozen=True)
class SimilarityScore:
    """
    - 1.0 = полное совпадение
    - 0.0 = полное несовпадение
    """
    value: float

    def __post_init__(self):
        if not (0.0 <= self.value <= 1.0):
            raise ValueError(
                f"Сходство должно быть в диапазоне [0, 1], получено {self.value}"
            )

    @property
    def as_percent(self) -> float:
        """Сходство в процентах 0-100"""
        return round(self.value * 100, 2)

    def __mul__(self, weight: float) -> float:
        
        return self.value * weight

    def __lt__(self, other: 'SimilarityScore') -> bool:
        return self.value < other.value

    def __gt__(self, other: 'SimilarityScore') -> bool:
        return self.value > other.value


@dataclass(frozen=True)
class CriterionContribution:
    """
    Вклад одного критерия в итоговую совместимость.
    """
    criterion_name: str
    criterion_type: CriterionType
    weight: float
    similarity: SimilarityScore
    value_a: Optional[Any] = None
    value_b: Optional[Any] = None

    @property
    def contribution(self) -> float:
        """Итоговый вклад этого критерия (вес × сходство)."""
        return round(self.weight * self.similarity.value, 4)

    @property
    def contribution_percent(self) -> float:
        return round(self.contribution * 100, 2)


@dataclass(frozen=True)
class CompatibilityBreakdown:
    items: List[CriterionContribution]

    @property
    def best_criterion(self) -> Optional[CriterionContribution]:
        """Критерий с наилучшим сходством"""
        if not self.items:
            return None
        return max(self.items, key=lambda x: x.similarity.value)

    @property
    def worst_criterion(self) -> Optional[CriterionContribution]:
        """Критерий с наихудшим сходством"""
        if not self.items:
            return None
        return min(self.items, key=lambda x: x.similarity.value)

    @property
    def average_similarity(self) -> float:
        """Среднее сходство по всем критериям"""
        if not self.items:
            return 0.0
        return sum(item.similarity.value for item in self.items) / len(self.items)

    def to_dict_list(self) -> List[Dict[str, Any]]:
        return [
            {
                "criterion": item.criterion_name,
                "criterion_type": item.criterion_type.value,
                "weight": item.weight,
                "similarity": item.similarity.value,
                "contribution": item.contribution,
                "contribution_percent": item.contribution_percent,
                "value_a": item.value_a,
                "value_b": item.value_b,
            }
            for item in self.items
        ]


@dataclass(frozen=True)
class CompatibilityResult:
    #Результат
    score: float  # 0-100
    breakdown: CompatibilityBreakdown

    def __post_init__(self):
        if not (0.0 <= self.score <= 100.0):
            raise ValueError(
                f"Балл совместимости должен быть в диапазоне [0, 100], получено {self.score}"
            )

    @property
    def score_normalized(self) -> float:
        
        return self.score / 100.0

    @property
    def is_good_match(self) -> bool:
        
        """хорошая совместимость > 70%. """
        return self.score >= 70.0

    @property
    def is_excellent_match(self) -> bool:
        """Отличная совместимость > 85%."""
        return self.score >= 85.0

    def summary_dict(self) -> Dict[str, Any]:
        return {
            "compatibility_score": self.score,
            "best_criterion": self.breakdown.best_criterion.criterion_name if self.breakdown.best_criterion else None,
            "best_similarity": self.breakdown.best_criterion.similarity.as_percent if self.breakdown.best_criterion else 0,
            "worst_criterion": self.breakdown.worst_criterion.criterion_name if self.breakdown.worst_criterion else None,
            "worst_similarity": self.breakdown.worst_criterion.similarity.as_percent if self.breakdown.worst_criterion else 0,
            "average_similarity": round(self.breakdown.average_similarity * 100, 2),
        }

class SimilarityFunction(ABC):

    @abstractmethod
    def compute(self, value_a: Any, value_b: Any) -> SimilarityScore:
        
        """ Вычислить сходство двух значений."""
        raise NotImplementedError


class ProfileReader(ABC):
   

    @abstractmethod
    def get_criterion_value(self, user_id: int, criterion_name: str) -> Any:
        """Получить значение критерия для пользователя."""
        raise NotImplementedError




class CompatibilityEvaluator:
    
    def __init__(self, similarity_functions: Dict[CriterionType, SimilarityFunction]):
        self._functions = similarity_functions

    def evaluate(
            self,
            profile_a: Dict[str, Any],
            profile_b: Dict[str, Any],
            weights: Dict[str, float]
    ) -> CompatibilityResult:
        """
        Оценить совместимость двух профилей.
        1. Для каждого критерия из weights:
            Получить значения из профилей
            Определить тип критерия
            Выбрать функцию сходства
            Вычислить сходство
            Посчитать вклад = вес * сходство
        2. Суммировать вклады - итоговый балл (0-100)"""
        contributions = []
        total_score = 0.0

        for criterion_name, weight in weights.items():
            # Получаем значения
            value_a = profile_a.get(criterion_name)
            value_b = profile_b.get(criterion_name)

            # Определяем тип критерия
            val_a = CriterionValue(value_a)
            val_b = CriterionValue(value_b)

            
            if val_a.is_empty or val_b.is_empty:
                similarity = SimilarityScore(0.0)
                criterion_type = CriterionType.UNKNOWN
            else:
                criterion_type = val_a.infer_type()
                func = self._functions.get(criterion_type)
                if func is None:
                    similarity = SimilarityScore(0.0)
                else:
                    similarity = func.compute(value_a, value_b)

            contribution = CriterionContribution(
                criterion_name=criterion_name,
                criterion_type=criterion_type,
                weight=weight,
                similarity=similarity,
                value_a=value_a,
                value_b=value_b,
            )

            contributions.append(contribution)
            total_score += contribution.contribution

        
        final_score = round(total_score * 100, 2)

        return CompatibilityResult(
            score=final_score,
            breakdown=CompatibilityBreakdown(items=contributions),
        )

    def evaluate_batch(
            self,
            user_profile: Dict[str, Any],
            candidates: List[Dict[str, Any]],
            weights: Dict[str, float]
    ) -> List[CompatibilityResult]:
        
        results = [
            self.evaluate(user_profile, candidate, weights)
            for candidate in candidates
        ]

        # Сортировка по убыванию совместимости
        results.sort(key=lambda r: r.score, reverse=True)
        return results

    def get_top_matches(
            self,
            user_profile: Dict[str, Any],
            candidates: List[Dict[str, Any]],
            weights: Dict[str, float],
            limit: int = 20
    ) -> List[CompatibilityResult]:
    
        all_results = self.evaluate_batch(user_profile, candidates, weights)
        return all_results[:limit]

    def validate_weights(self, weights: Dict[str, float]) -> List[str]:
        """
        Проверить корректность весов перед вычислением совместимости.
        """
        warnings = []

        total = sum(weights.values())
        if abs(total - 1.0) > 0.01:
            warnings.append(
                f"Сумма весов должна быть 1.0, текущая сумма: {total:.3f}"
            )

        for name, weight in weights.items():
            if weight < 0:
                warnings.append(f"Вес критерия '{name}' отрицательный: {weight}")
            if weight > 1:
                warnings.append(f"Вес критерия '{name}' больше 1: {weight}")

        return warnings
