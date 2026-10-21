from dataclasses import dataclass
from typing import List, Optional, Any

from application.ports import UserRepository
from application.dto.requests import UpdateUserRequest



class UserNotFoundError(Exception):
    """Пользователь не найден."""
    pass

@dataclass
class GetAllUsersUseCase:
    """Получить всех активных пользователей."""

    user_repo: UserRepository

    def execute(self) -> List[dict]:
        users = self.user_repo.get_all_active()
        return [
            self._format_user(u)
            for u in users
        ]

    @staticmethod
    def _format_user(user) -> dict:
        """Форматирует пользователя"""
        return {
            "id": user.id,
            "email": user.email,
            "name": user.name,
            "age": user.age,
            "gender": user.gender,
            "looking_for": user.looking_for,
            "city": user.city,
            "bio": user.bio,
            "avatar": user.avatar,
            "income": user.income,
            "appearance": user.appearance,
            "education": user.education,
            "religion": user.religion,
            "kindness": user.kindness,
            "interests": user.interests,
        }


@dataclass
class GetUserByIdUseCase:
    user_repo: UserRepository
    photo_storage: Any  

    def execute(self, user_id: int) -> dict:
        user = self.user_repo.get_by_id(user_id)
        if not user:
            raise UserNotFoundError(f"Пользователь с ID {user_id} не найден")
        user_dict = GetAllUsersUseCase._format_user(user)
        
        photos = self.photo_storage.get_user_photos(user_id)
        avatar_url = None
        for photo in photos:
            if photo.get("is_avatar"):
                avatar_url = photo.get("photo_id") 
                break
        user_dict["avatar_url"] = avatar_url
        return user_dict



@dataclass
class UpdateUserUseCase:

    user_repo: UserRepository
    def execute(self, user_id: int, request: UpdateUserRequest) -> dict:
        user = self.user_repo.get_by_id(user_id)
        if not user:
            raise UserNotFoundError(f"Пользователь с ID {user_id} не найден")

        fields = {
            k: v for k, v in request.model_dump().items()
            if v is not None
        }

        if fields:
            self.user_repo.update(user_id, fields)

        return {"message": "Данные обновлены", "updated_fields": list(fields.keys())}


@dataclass
class DeleteUserUseCase:
    """Удалить профиль"""

    user_repo: UserRepository

    def execute(self, user_id: int) -> dict:
        user = self.user_repo.get_by_id(user_id)
        if not user:
            raise UserNotFoundError(f"Пользователь с ID {user_id} не найден")

        self.user_repo.deactivate(user_id)
        return {"message": "Профиль удалён"}



@dataclass
class GetUserProfileWithPhotosUseCase:
    user_repo: UserRepository
    photo_storage: Any

    def execute(self, user_id: int) -> dict:
        user = self.user_repo.get_by_id(user_id)
        if not user:
            raise UserNotFoundError(f"Пользователь {user_id} не найден")
        user_dict = GetAllUsersUseCase._format_user(user)
        photos = self.photo_storage.get_user_photos(user_id)
        avatar_url = None
        for photo in photos:
            if photo.get("is_avatar"):
                avatar_url = photo.get("photo_id")
                break
        user_dict["avatar_url"] = avatar_url
        user_dict["photos"] = photos
        return user_dict
