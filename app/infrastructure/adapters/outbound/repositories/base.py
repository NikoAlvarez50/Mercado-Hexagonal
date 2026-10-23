"""Almacén genérico en memoria compartido por todos los repositorios."""
import copy
from threading import RLock
from typing import Dict, Generic, List, Optional, TypeVar

T = TypeVar("T")


class InMemoryStore(Generic[T]):
    """Almacén por clave. Guarda y devuelve copias para que nadie modifique el
    estado interno desde fuera. Evita repetir el mismo código en cada repositorio."""

    def __init__(self):
        self._data: Dict[str, T] = {}
        self._lock = RLock()

    def _put(self, key: str, entity: T) -> T:
        with self._lock:
            self._data[key] = copy.deepcopy(entity)
        return entity

    def _find(self, key: str) -> Optional[T]:
        entity = self._data.get(key)
        return copy.deepcopy(entity) if entity is not None else None

    def _all(self) -> List[T]:
        return [copy.deepcopy(entity) for entity in self._data.values()]
