from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import Response

from application.dto.requests import UploadPhotoRequest, SetAvatarRequest
from application.use_cases.photo_case import (
    UploadPhotoUseCase,
    GetUserPhotosUseCase,
    SetAvatarUseCase,
    DeletePhotoUseCase,
    GetPhotoBytesUseCase,
    PhotoNotFoundError,
)
from application.use_cases.user_case import UserNotFoundError
from presentation.api.dependencies import (
    get_upload_photo_use_case,
    get_user_photos_use_case,
    get_set_avatar_use_case,
    get_delete_photo_use_case,
    get_photo_bytes_use_case,
)

router = APIRouter(prefix="/api/photos", tags=["Фотографии"])


@router.post("/upload/{user_id}")
def upload_photo(
        user_id: int,
        request: UploadPhotoRequest,
        use_case: UploadPhotoUseCase = Depends(get_upload_photo_use_case),
):
    """Загрузить фото пользователя"""
    try:
        return use_case.execute(user_id, request)
    except UserNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/user/{user_id}")
def get_user_photos(
        user_id: int,
        use_case: GetUserPhotosUseCase = Depends(get_user_photos_use_case),
):
    """Получить все фото пользователя"""
    try:
        photos = use_case.execute(user_id)
        return {"photos": photos, "count": len(photos)}
    except UserNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.put("/avatar/{user_id}")
def set_avatar(
        user_id: int,
        request: SetAvatarRequest,
        use_case: SetAvatarUseCase = Depends(get_set_avatar_use_case),
):
    """Установить фото как основной аватар"""
    try:
        return use_case.execute(user_id, request)
    except UserNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except PhotoNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.delete("/{user_id}/{photo_id}")
def delete_photo(
        user_id: int,
        photo_id: str,
        use_case: DeletePhotoUseCase = Depends(get_delete_photo_use_case),
):
    """Удалить фото"""
    try:
        return use_case.execute(user_id, photo_id)
    except UserNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except PhotoNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/{photo_id}")
def get_photo(
    photo_id: str,
    use_case: GetPhotoBytesUseCase = Depends(get_photo_bytes_use_case),
):
    photo_bytes, content_type = use_case.execute(photo_id)
    if photo_bytes is None:
        raise HTTPException(status_code=404, detail="Фото не найдено")
    return Response(content=photo_bytes, media_type=content_type or "image/jpeg")

