import pytest

from app.infrastructure.container import build_container
from app.main import create_app


@pytest.fixture
def container():
    return build_container()


@pytest.fixture
def client(container):
    app = create_app(container)
    app.config.update(TESTING=True)
    return app.test_client()
