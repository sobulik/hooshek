import pathlib
import pytest
import shutil

def dir_fixtures():
    p = pathlib.Path(__file__).parents[1] / "test" / "resources"
    return filter(lambda d: d.is_dir(), p.iterdir())

@pytest.fixture(params=dir_fixtures(), scope="session")
def dir_fixture(request):
    return request.param

@pytest.fixture(scope="session")
def dir_script():
    return pathlib.Path(__file__).parents[1]

@pytest.fixture
def prepare(dir_fixture, tmp_path):
    for f in ("event.yaml", "clubs.yaml", "athletes.yaml"):
        shutil.copy(dir_fixture / f, tmp_path)
