from dataclasses import dataclass
from typing import List, Optional

from application.ports import UserRepository
from application.dto.requests import UploadPhotoRequest, SetAvatarRequest
from application.dto.responses import PhotoResponse


class PhotoStorageInterface:

    def save_photo(self, user_id: int, base64_data: str, filename: str = None):
        raise NotImplementedError

    def get_user_photos(self, user_id: int) -> List[dict]:
        raise NotImplementedError

    def set_avatar(self, user_id: int, photo_id: str) -> bool:
        raise NotImplementedError

    def delete_photo(self, user_id: int, photo_id: str) -> bool:
        raise NotImplementedError

    def delete_all_user_photos(self, user_id: int) -> int:
        raise NotImplementedError

    def get_photo_bytes(self, photo_id: str) -> Optional[bytes]:
        raise NotImplementedError


class PhotoNotFoundError(Exception):
    """Фото не найдено"""
    pass


@dataclass
class UploadPhotoUseCase:
    """Загрузить фото пользователя"""

    user_repo: UserRepository
    photo_storage: PhotoStorageInterface

    def execute(self, user_id: int, request: UploadPhotoRequest) -> dict:
        user = self.user_repo.get_by_id(user_id)
        if not user:
            from application.use_cases.user_case import UserNotFoundError
            raise UserNotFoundError(f"Пользователь {user_id} не найден")

        metadata = self.photo_storage.save_photo(
            user_id=user_id,
            base64_data=request.photo_base64,
            filename=request.filename,
        )

        return {
            "photo_id": metadata.photo_id,
            "message": "Фото загружено",
            "url": f"/api/photos/{metadata.photo_id}"
        }


@dataclass
class GetUserPhotosUseCase:

    user_repo: UserRepository
    photo_storage: PhotoStorageInterface

    def execute(self, user_id: int) -> List[dict]:
        user = self.user_repo.get_by_id(user_id)
        if not user:
            from application.use_cases.user_case import UserNotFoundError
            raise UserNotFoundError(f"Пользователь {user_id} не найден")

        return self.photo_storage.get_user_photos(user_id)


@dataclass
class SetAvatarUseCase:
    """Установить аватар"""

    user_repo: UserRepository
    photo_storage: PhotoStorageInterface

    def execute(self, user_id: int, request: SetAvatarRequest) -> dict:
        user = self.user_repo.get_by_id(user_id)
        if not user:
            from application.use_cases.user_case import UserNotFoundError
            raise UserNotFoundError(f"Пользователь {user_id} не найден")

        success = self.photo_storage.set_avatar(user_id, request.photo_id)
        if not success:
            raise PhotoNotFoundError(f"Фото {request.photo_id} не найдено")

        self.user_repo.update(user_id, {"avatar": request.photo_id})

        return {"message": "Аватар установлен", "photo_id": request.photo_id}


@dataclass
class DeletePhotoUseCase:
    """Удалить фото"""

    user_repo: UserRepository
    photo_storage: PhotoStorageInterface

    def execute(self, user_id: int, photo_id: str) -> dict:
        user = self.user_repo.get_by_id(user_id)
        if not user:
            from application.use_cases.user_case import UserNotFoundError
            raise UserNotFoundError(f"Пользователь {user_id} не найден")

        success = self.photo_storage.delete_photo(user_id, photo_id)
        if not success:
            raise PhotoNotFoundError(f"Фото {photo_id} не найдено")

        return {"message": "Фото удалено"}


@dataclass
class GetPhotoBytesUseCase:

    photo_storage: PhotoStorageInterface
    def execute(self, photo_id: str) -> tuple[Optional[bytes], Optional[str]]:
        from infrastructure.storage.photo import get_photo_storage
        storage = get_photo_storage()

        path = storage.get_photo_path(photo_id)
        if not path:
            return None, None

        all_metadata = storage._load_metadata()
        if photo_id not in all_metadata:
            return None, None

        meta = all_metadata[photo_id]
        return path.read_bytes(), meta.content_type
