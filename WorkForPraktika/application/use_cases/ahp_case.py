from dataclasses import dataclass
from typing import List, Dict

from application.ports import WeightRepository
from application.dto.requests import (
    CalculateWeightsRequest,
    SaveWeightsRequest,

)
from domain.services.ahp_services import (
    AHPService,
    Comparison,
)


@dataclass
class CalculateWeightsUseCase:
    ahp_service: AHPService

    def execute(self, request: CalculateWeightsRequest) -> dict:
        comparisons = [
            Comparison(
                criterion_a=comp.criterion_a,
                criterion_b=comp.criterion_b,
                value=comp.value,
            )
            for comp in request.comparisons
        ]

        # Строим матрицу
        matrix = self.ahp_service.build_matrix(
            criteria=request.criteria,
            comparisons=comparisons,
        )

        # Вычисляем веса
        result = self.ahp_service.calculate_weights(matrix)

        # ответ
        weights_dict = result.to_dict(request.criteria)

        return {
            "weights": weights_dict,
            "lambda_max": result.lambda_max,
            "ci": result.ci,
            "cr": result.cr,
            "is_consistent": result.is_consistent,
            "criteria_list": request.criteria,
        }


@dataclass
class SaveWeightsUseCase:
    """Сохранить веса критериев для пользователя."""

    weight_repo: WeightRepository

    def execute(self, user_id: int, request: SaveWeightsRequest) -> dict:
        self.weight_repo.save(user_id, request.weights)

        return {
            "message": "Веса сохранены",
            "weights": request.weights,
        }


@dataclass
class GetWeightsUseCase:
    weight_repo: WeightRepository

    def execute(self, user_id: int) -> dict:
        raw = self.weight_repo.get_raw(user_id)
        if not raw:
            # Значения по умолчанию 5
            criteria = AHPService.default_criteria()
            raw = {c: 5 for c in criteria}
        return {
            "user_id": user_id,
            "raw_weights": raw,
            "criteria_list": list(raw.keys()),
        }

@dataclass
class SaveWeightsSimpleUseCase:
    weight_repo: WeightRepository

    def execute(self, user_id: int, raw_weights: Dict[str, float]) -> dict:
        self.weight_repo.save(user_id, raw_weights)
        return {
            "message": "Веса успешно сохранены",
            "raw_weights": raw_weights
        }
