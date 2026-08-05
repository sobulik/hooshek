import pathlib
import pytest


@pytest.fixture(scope="session")
def project_path():
    return pathlib.Path(__file__).parents[1]


def fixtures_path():
    p = pathlib.Path(__file__).parent / "data"
    return filter(lambda d: d.is_dir(), p.iterdir())


@pytest.fixture(params=fixtures_path(), scope="session")
def fixture_path(request):
    return request.param
