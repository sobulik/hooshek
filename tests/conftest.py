import pathlib
import pytest

def dir_fixtures():
    p = pathlib.Path(__file__).parents[1] / "test" / "resources"
    return filter(lambda d: d.is_dir(), p.iterdir())

@pytest.fixture(params=dir_fixtures(), scope="session")
def dir_fixture(request):
    return request.param

@pytest.fixture(scope="session")
def dir_script():
    return pathlib.Path(__file__).parents[1]
