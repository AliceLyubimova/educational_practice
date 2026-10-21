from dataclasses import dataclass
from typing import List

from application.ports.user_repository import UserRepository
from application.ports.comment_repository import CommentRepository
from application.use_cases.user_case import UserNotFoundError


class SelfCommentError(Exception):
    pass


@dataclass
class AddCommentUseCase:
    user_repo: UserRepository
    comment_repo: CommentRepository

    def execute(self, user_id: int, target_user_id: int, text: str) -> dict:
        if user_id == target_user_id:
            raise SelfCommentError("Нельзя оставлять отзыв о себе")

        if not self.user_repo.get_by_id(target_user_id):
            raise UserNotFoundError(f"Пользователь {target_user_id} не найден")

        if not text or not text.strip():
            raise ValueError("Текст отзыва не может быть пустым")

        comment_id = self.comment_repo.add(user_id, target_user_id, text.strip())
        return {"id": comment_id, "message": "Отзыв добавлен"}


@dataclass
class GetCommentsUseCase:
    comment_repo: CommentRepository

    def execute(self, target_user_id: int) -> List[dict]:
        comments = self.comment_repo.get_by_target(target_user_id)
        return [
            {
                "id": c.id,
                "user_id": c.user_id,
                "user_name": c.user_name,
                "text": c.text,
                "created_at": c.created_at,
            }
            for c in comments
        ]
