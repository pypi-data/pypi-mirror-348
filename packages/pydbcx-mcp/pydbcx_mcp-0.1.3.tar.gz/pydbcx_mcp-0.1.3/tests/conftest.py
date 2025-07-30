import httpx
import pytest

from testcontainers.generic import ServerContainer
from testcontainers.core.waiting_utils import wait_for_logs
from testcontainers.core.image import DockerImage


@pytest.fixture(scope="session", autouse=True)
def print_beginning_of_session():
    with ServerContainer(port=8080, image="jdbcx/jdbcx") as srv:
        url = srv._create_connection_url()
        response = httpx.get(f"{url}/ping", timeout=5)
        assert response.status_code == 200, "Response status code is not 200"
        delay = wait_for_logs(srv, "GET / HTTP/1.1")
        yield
