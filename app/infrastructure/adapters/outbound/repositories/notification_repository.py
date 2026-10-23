from typing import List

from app.application.ports.outbound import NotificationRepository
from app.domain.entities import Notification
from app.infrastructure.adapters.outbound.repositories.base import InMemoryStore


class InMemoryNotificationRepository(InMemoryStore[Notification], NotificationRepository):
    def save(self, notification: Notification) -> Notification:
        return self._put(notification.id, notification)

    def list_for_user(self, user_id: str) -> List[Notification]:
        return [n for n in self._all() if n.user_id == user_id]
