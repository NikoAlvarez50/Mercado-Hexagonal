"""Adaptadores de salida: generador de IDs y canal de notificación por log."""
import logging
import uuid

from app.application.ports.outbound import IdGenerator, NotificationSender
from app.domain.entities import User

logger = logging.getLogger("notifications")


class UuidGenerator(IdGenerator):
    def new_id(self) -> str:
        return uuid.uuid4().hex[:12]


class LogNotificationSender(NotificationSender):
    """Simula el envío escribiendo en el log. Sustituible por SMTP, SMS, etc."""

    def send(self, user: User, message: str) -> None:
        logger.info("Notificación para %s <%s>: %s", user.name, user.email, message)
