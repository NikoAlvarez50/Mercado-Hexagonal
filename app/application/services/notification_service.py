"""Servicio 5: Notificaciones."""
from typing import List

from app.application.ports.inbound import NotificationServicePort, UserServicePort
from app.application.ports.outbound import IdGenerator, NotificationRepository, NotificationSender
from app.domain.entities import Notification
from app.domain.exceptions import ValidationError


class NotificationService(NotificationServicePort):
    def __init__(
        self,
        repository: NotificationRepository,
        sender: NotificationSender,
        users: UserServicePort,
        ids: IdGenerator,
    ):
        self._repo = repository
        self._sender = sender
        self._users = users
        self._ids = ids

    def notify(self, user_id: str, message: str) -> Notification:
        if not isinstance(message, str) or not message.strip():
            raise ValidationError("El mensaje es obligatorio")
        user = self._users.get(user_id)
        notification = self._repo.save(
            Notification(id=self._ids.new_id(), user_id=user_id, message=message.strip())
        )
        self._sender.send(user, notification.message)
        return notification

    def list_for_user(self, user_id: str) -> List[Notification]:
        self._users.get(user_id)
        return self._repo.list_for_user(user_id)
