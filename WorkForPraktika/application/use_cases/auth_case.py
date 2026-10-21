from domain.services.ahp_services import AHPService
from dataclasses import dataclass

from application.ports import (
    UserRepository,
    WeightRepository,
    HashService,
)
from application.dto.requests import RegisterRequest, LoginRequest

class EmailAlreadyExistsError(Exception):
    """Email уже зарегистрирован."""
    pass


class InvalidCredentialsError(Exception):
    """Неверный email или пароль."""
    pass


@dataclass
class RegisterUseCase:
    """
    Регистрация нового пользователя.
    """

    user_repo: UserRepository
    weight_repo: WeightRepository
    hash_service: HashService

    def execute(self, request: RegisterRequest) -> dict:
       
        # Проверяем email
        existing = self.user_repo.get_by_email(request.email)
        if existing:
            raise EmailAlreadyExistsError(
                f"Email '{request.email}' уже зарегистрирован"
            )

        # Хэшируем пароль
        password_hash = self.hash_service.hash(request.password)

        # Создаём пользователя
        user_id = self.user_repo.create({
            "email": request.email,
            "password_hash": password_hash,
            "name": request.name,
            "age": request.age,
            "gender": request.gender,
            "looking_for": request.looking_for,
            "city": request.city,
            "bio": request.bio,
        })

        # Инициализируем стандартные веса
        criteria = AHPService.default_criteria()
        default_raw = {c: 5 for c in criteria}  # все по 5
        self.weight_repo.save(user_id, default_raw)

        return {
            "user_id": user_id,
            "email": request.email,
            "name": request.name,
            "message": "Регистрация успешна",
        }


@dataclass
class LoginUseCase:
    """
    Вход в систему.
    """

    user_repo: UserRepository
    hash_service: HashService

    def execute(self, request: LoginRequest) -> dict:
        # Ищем пользователя
        user = self.user_repo.get_by_email(request.email)
        if not user:
            raise InvalidCredentialsError("Неверный email или пароль")
        # Проверяем пароль
        if not self.hash_service.verify(request.password, user.password_hash):
            raise InvalidCredentialsError("Неверный email или пароль")

        return {
            "user_id": user.id,
            "email": user.email,
            "name": user.name,
            "message": "Вход выполнен успешно",
        }
