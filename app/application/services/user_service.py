"""Servicio 1: Usuarios."""
from typing import List

from app.application.ports.inbound import UserServicePort
from app.application.ports.outbound import IdGenerator, UserRepository
from app.domain.entities import User
from app.domain.exceptions import ConflictError, NotFoundError


class UserService(UserServicePort):
    def __init__(self, repository: UserRepository, ids: IdGenerator):
        self._repo = repository
        self._ids = ids

    def register(self, name: str, email: str) -> User:
        user = User(id=self._ids.new_id(), name=name, email=email)
        if self._repo.get_by_email(user.email):
            raise ConflictError(f"Ya existe un usuario con el email {user.email}")
        return self._repo.save(user)

    def get(self, user_id: str) -> User:
        user = self._repo.get(user_id)
        if user is None:
            raise NotFoundError(f"Usuario {user_id} no encontrado")
        return user

    def list(self) -> List[User]:
        return self._repo.list()
