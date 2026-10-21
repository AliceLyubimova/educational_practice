import hashlib

from application.ports.hash_services import HashService


class Sha256HashService(HashService):
    """Хеширование SHA-256."""

    def hash(self, password: str) -> str:
        return hashlib.sha256(password.encode()).hexdigest()

    def verify(self, password: str, password_hash: str) -> bool:
        """Проверить соответствия"""
        return self.hash(password) == password_hash
