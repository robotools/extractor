import pytest


@pytest.fixture(scope="session", params=["defcon", "ufoLib2"])
def ufo_module(request):
    return pytest.importorskip(request.param)


@pytest.fixture(scope="session")
def FontClass(ufo_module):
    if hasattr(ufo_module.Font, "open"):

        def ctor(path=None):
            if path is None:
                return ufo_module.Font()
            else:
                return ufo_module.Font.open(path)

        return ctor
    return ufo_module.Font
