"""Excepciones del dominio. No dependen de ningún framework."""


class DomainError(Exception):
    """Error base del dominio."""


class ValidationError(DomainError):
    """Datos inválidos."""


class NotFoundError(DomainError):
    """Recurso inexistente."""


class ConflictError(DomainError):
    """Conflicto con el estado actual (p. ej. email duplicado)."""


class InsufficientStockError(DomainError):
    """No hay existencias suficientes."""
