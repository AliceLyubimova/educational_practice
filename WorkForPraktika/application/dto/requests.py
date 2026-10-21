from pydantic import BaseModel, EmailStr, field_validator
from typing import List, Optional
from typing import Dict

# АВТОРИЗАЦИЯ

class RegisterRequest(BaseModel):
    email: EmailStr
    password: str
    name: str
    age: int
    gender: str
    looking_for: str
    city: str
    bio: Optional[str] = None

    @field_validator("age")
    @classmethod
    def age_must_be_adult(cls, v: int) -> int:
        if v < 18:
            raise ValueError("Возраст должен быть не менее 18 лет")
        if v > 120:
            raise ValueError("Некорректный возраст")
        return v

    @field_validator("gender", "looking_for")
    @classmethod
    def must_be_valid_gender(cls, v: str) -> str:
        if v not in ("male", "female"):
            raise ValueError("Пол должен быть 'male' или 'female'")
        return v

    @field_validator("password")
    @classmethod
    def password_min_length(cls, v: str) -> str:
        if len(v) < 3:
            raise ValueError("Пароль должен быть не менее 3 символов")
        return v


class LoginRequest(BaseModel):
    """Запрос на вход."""
    email: EmailStr
    password: str


# ПОЛЬЗОВАТЕЛИ 

class UpdateUserRequest(BaseModel):
    """обновление профиля"""
    name: Optional[str] = None
    age: Optional[int] = None
    gender: Optional[str] = None
    looking_for: Optional[str] = None
    city: Optional[str] = None
    bio: Optional[str] = None
    income: Optional[int] = None
    appearance: Optional[int] = None
    education: Optional[str] = None
    religion: Optional[str] = None
    kindness: Optional[int] = None
    interests: Optional[List[str]] = None


# МАИ 

class CriteriaComparison(BaseModel):
    criterion_a: str
    criterion_b: str
    value: float 


class CalculateWeightsRequest(BaseModel):
    criteria: List[str]
    comparisons: List[CriteriaComparison]


class SaveWeightsRequest(BaseModel):
    user_id: int
    weights: dict[str, float]
    comparisons: List[CriteriaComparison]


# СОВМЕСТИМОСТЬ 

class CompatibilityRequest(BaseModel):
    user_id: int
    candidate_ids: Optional[List[int]] = None  
    use_saved_weights: bool = True  


#  ЛАЙКИ 

class LikeRequest(BaseModel):
    """Запрос на лайк."""
    from_user_id: int
    to_user_id: int


# ФОТО

class UploadPhotoRequest(BaseModel):
    photo_base64: str  
    filename: Optional[str] = None


class SetAvatarRequest(BaseModel):
    photo_id: str

class SaveWeightsSimpleRequest(BaseModel):
    weights: Dict[str, float]
