import os
import json
import shutil
import base64
from pathlib import Path
from typing import List, Optional, Dict, Any
from datetime import datetime
from dataclasses import dataclass, asdict


PHOTOS_DIR = Path(__file__).parent.parent.parent / "storage" / "photos"
PHOTOS_DIR.mkdir(parents=True, exist_ok=True)


METADATA_FILE = PHOTOS_DIR / "photos_metadata.json"


@dataclass
class PhotoMetadata:
    photo_id: str  
    user_id: int
    filename: str  
    file_path: str  
    file_size: int
    content_type: str
    uploaded_at: str
    is_avatar: bool = False 


class PhotoStorage:

    def __init__(self):
        self._ensure_metadata()

    def _ensure_metadata(self):
        if not METADATA_FILE.exists():
            self._save_metadata({})

    def _load_metadata(self) -> Dict[str, PhotoMetadata]:
        if not METADATA_FILE.exists():
            return {}
        with open(METADATA_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return {
                photo_id: PhotoMetadata(**meta)
                for photo_id, meta in data.items()
            }

    def _save_metadata(self, metadata: Dict[str, PhotoMetadata]):
        
        data = {photo_id: asdict(meta) for photo_id, meta in metadata.items()}
        with open(METADATA_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def _generate_photo_id(self) -> str:
        """Сгенерировать ID фото"""
        import uuid
        return str(uuid.uuid4())

    def _get_user_photos_dir(self, user_id: int) -> Path:
        
        user_dir = PHOTOS_DIR / str(user_id)
        user_dir.mkdir(parents=True, exist_ok=True)
        return user_dir

    def save_photo(self, user_id: int, base64_data: str, filename: str = None) -> PhotoMetadata:
        if ',' in base64_data and base64_data.startswith('data:'):
            header, data = base64_data.split(',', 1)
            
            content_type = header.split(':')[1].split(';')[0]
        else:
            data = base64_data
            content_type = "image/jpeg"  # default

        
        photo_bytes = base64.b64decode(data)

        
        ext_map = {
            "image/jpeg": ".jpg",
            "image/jpg": ".jpg",
            "image/png": ".png",
            "image/webp": ".webp",
            "image/gif": ".gif"
        }
        ext = ext_map.get(content_type, ".jpg")

        
        photo_id = self._generate_photo_id()
        if not filename:
            filename = f"{photo_id}{ext}"
        elif not filename.endswith(ext):
            filename = f"{filename}{ext}"

        # Сохраняем
        user_dir = self._get_user_photos_dir(user_id)
        file_path = user_dir / filename
        file_path.write_bytes(photo_bytes)

        
        metadata = PhotoMetadata(
            photo_id=photo_id,
            user_id=user_id,
            filename=filename,
            file_path=str(file_path.relative_to(PHOTOS_DIR)),
            file_size=len(photo_bytes),
            content_type=content_type,
            uploaded_at=datetime.now().isoformat(),
            is_avatar=False,
        )

        all_metadata = self._load_metadata()
        all_metadata[photo_id] = metadata
        self._save_metadata(all_metadata)

        return metadata

    def set_avatar(self, user_id: int, photo_id: str) -> bool:
        """Установить фото как аватар"""
        all_metadata = self._load_metadata()

        # Снимаем со всех фото пользователя
        for pid, meta in all_metadata.items():
            if meta.user_id == user_id:
                meta.is_avatar = False
                all_metadata[pid] = meta

        # Устанавливаем новому фото
        if photo_id in all_metadata:
            meta = all_metadata[photo_id]
            meta.is_avatar = True
            all_metadata[photo_id] = meta
            self._save_metadata(all_metadata)
            return True

        return False

    def get_user_photos(self, user_id: int) -> List[Dict[str, Any]]:
        """все фото пользователя"""
        all_metadata = self._load_metadata()
        user_photos = [
            meta for meta in all_metadata.values()
            if meta.user_id == user_id
        ]

        result = []
        for meta in user_photos:
            result.append({
                "photo_id": meta.photo_id,
                "filename": meta.filename,
                "file_size": meta.file_size,
                "content_type": meta.content_type,
                "uploaded_at": meta.uploaded_at,
                "is_avatar": meta.is_avatar,
                "url": f"/api/photos/{meta.photo_id}"
            })

        return result

    def get_photo_path(self, photo_id: str) -> Optional[Path]:
        
        all_metadata = self._load_metadata()
        if photo_id not in all_metadata:
            return None

        meta = all_metadata[photo_id]
        return PHOTOS_DIR / meta.file_path

    def get_photo_base64(self, photo_id: str) -> Optional[str]:
        
        path = self.get_photo_path(photo_id)
        if not path or not path.exists():
            return None

        import base64
        photo_bytes = path.read_bytes()
        return base64.b64encode(photo_bytes).decode('utf-8')

    def get_photo_bytes(self, photo_id: str) -> Optional[bytes]:
        """байты фото"""
        path = self.get_photo_path(photo_id)
        if not path or not path.exists():
            return None
        return path.read_bytes()

    def delete_photo(self, user_id: int, photo_id: str) -> bool:
        """Удалить фото"""
        all_metadata = self._load_metadata()
        if photo_id not in all_metadata:
            return False

        meta = all_metadata[photo_id]
        if meta.user_id != user_id:
            return False  # чужое фото

        # Удаляем файл
        file_path = PHOTOS_DIR / meta.file_path
        if file_path.exists():
            file_path.unlink()

        # Удаляем метаданные
        del all_metadata[photo_id]
        self._save_metadata(all_metadata)
        return True

    def delete_all_user_photos(self, user_id: int) -> int:
        """Удалить все фото пользователя"""
        all_metadata = self._load_metadata()
        to_delete = [
            photo_id for photo_id, meta in all_metadata.items()
            if meta.user_id == user_id
        ]

        for photo_id in to_delete:
            meta = all_metadata[photo_id]
            file_path = PHOTOS_DIR / meta.file_path
            if file_path.exists():
                file_path.unlink()
            del all_metadata[photo_id]

        
        user_dir = self._get_user_photos_dir(user_id)
        if user_dir.exists():
            shutil.rmtree(user_dir)

        self._save_metadata(all_metadata)
        return len(to_delete)

    def get_photo_bytes(self, photo_id: str) -> Optional[bytes]:
        
        path = self.get_photo_path(photo_id)
        if not path or not path.exists():
            print(f"[DEBUG] Photo not found: {path}")
            return None
        return path.read_bytes()



_photo_storage = None


def get_photo_storage() -> PhotoStorage:
    global _photo_storage
    if _photo_storage is None:
        _photo_storage = PhotoStorage()
    return _photo_storage
