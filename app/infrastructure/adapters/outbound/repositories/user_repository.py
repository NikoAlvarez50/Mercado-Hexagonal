from typing import List, Optional

from app.application.ports.outbound import UserRepository
from app.domain.entities import User
from app.infrastructure.adapters.outbound.repositories.base import InMemoryStore


class InMemoryUserRepository(InMemoryStore[User], UserRepository):
    def save(self, user: User) -> User:
        return self._put(user.id, user)

    def get(self, user_id: str) -> Optional[User]:
        return self._find(user_id)

    def get_by_email(self, email: str) -> Optional[User]:
        email = email.strip().lower()
        return next((u for u in self._all() if u.email == email), None)

    def list(self) -> List[User]:
        return self._all()
