from dataclasses import dataclass
from typing import List, Optional

from application.ports import UserRepository, WeightRepository
from application.dto.requests import CompatibilityRequest
from domain.services.compatibility_services import CompatibilityEvaluator
from domain.services.ahp_services import AHPService




class NoCandidatesError(Exception):
    """Нет подходящих кандидатов."""
    pass




@dataclass
class CalculateCompatibilityUseCase:
    """
    Рассчитать совместимость пользователя с кандидатами.
    """

    user_repo: UserRepository
    weight_repo: WeightRepository
    compatibility_evaluator: CompatibilityEvaluator

    def execute(self, request: CompatibilityRequest) -> dict:
        
        user = self.user_repo.get_by_id(request.user_id)
        if not user:
            from application.use_cases.user_case import UserNotFoundError
            raise UserNotFoundError(f"Пользователь с ID {request.user_id} не найден")

        if request.use_saved_weights:
            normalized = self.weight_repo.get_normalized(request.user_id)
            if normalized is None:
                normalized = AHPService.default_weights()
        else:
            normalized = AHPService.default_weights()

        if request.candidate_ids:
            candidates = []
            for cid in request.candidate_ids:
                c = self.user_repo.get_by_id(cid)
                if c:
                    candidates.append(c)
        else:
            all_users = self.user_repo.get_all_active()
            candidates = [
                u for u in all_users
                if u.id != request.user_id and u.gender == user.looking_for
            ]

        if not candidates:
            raise NoCandidatesError("Нет подходящих кандидатов")

        user_profile = self.user_repo.to_profile_dict(user)
        candidate_profiles = [self.user_repo.to_profile_dict(c) for c in candidates]

        results = self.compatibility_evaluator.evaluate_batch(
            user_profile=user_profile,
            candidates=candidate_profiles,
            weights=normalized,
        )

        formatted = []
        for i, result in enumerate(results[:20]):
            candidate = candidates[i]
            formatted.append({
                "candidate_id": candidate.id,
                "candidate_name": candidate.name,
                "candidate_age": candidate.age,
                "candidate_city": candidate.city,
                "candidate_avatar": candidate.avatar,
                "compatibility_score": result.score,
                "best_criterion": result.breakdown.best_criterion.criterion_name if result.breakdown.best_criterion else None,
                "worst_criterion": result.breakdown.worst_criterion.criterion_name if result.breakdown.worst_criterion else None,
                "average_similarity": round(result.breakdown.average_similarity * 100, 2),
            })

        top_match = formatted[0] if formatted else None

        return {
            "user_id": request.user_id,
            "user_name": user.name,
            "weights_used": normalized,
            "weights_consistent": True,
            "candidates": formatted,
            "top_match": top_match,
        }


@dataclass
class GetRecommendationsUseCase:
    user_repo: UserRepository
    weight_repo: WeightRepository
    compatibility_evaluator: CompatibilityEvaluator

    def execute(self, user_id: int, limit: int = 10) -> dict:
        from application.use_cases.user_case import UserNotFoundError

        user = self.user_repo.get_by_id(user_id)
        if not user:
            raise UserNotFoundError(f"Пользователь с ID {user_id} не найден")

        
        normalized = self.weight_repo.get_normalized(user_id)
        if normalized is None:
            normalized = AHPService.default_weights()

        # Кандидаты
        all_users = self.user_repo.get_all_active()
        candidates = [
            u for u in all_users
            if u.id != user_id and u.gender == user.looking_for

        ]

        if not candidates:
            raise NoCandidatesError("Нет подходящих кандидатов")

        # Совместимость
        user_profile = self.user_repo.to_profile_dict(user)
        candidate_profiles = [self.user_repo.to_profile_dict(c) for c in candidates]

        results = self.compatibility_evaluator.evaluate_batch(
            user_profile=user_profile,
            candidates=candidate_profiles,
            weights=normalized,
        )

        formatted = []
        for i, result in enumerate(results[:limit]):
            candidate = candidates[i]
            formatted.append({
                "candidate_id": candidate.id,
                "candidate_name": candidate.name,
                "candidate_age": candidate.age,
                "candidate_city": candidate.city,
                "candidate_avatar": candidate.avatar,
                "compatibility_score": result.score,
                "best_criterion": result.breakdown.best_criterion.criterion_name if result.breakdown.best_criterion else None,
                "average_similarity": round(result.breakdown.average_similarity * 100, 2),
            })

        return {
            "user_id": user_id,
            "recommendations": formatted,
            "total_candidates": len(results),
        }
