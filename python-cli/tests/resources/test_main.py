import pytest


def add(x, y):
    return x + y


def test_add():
    assert add(1, 2) == 3


@pytest.mark.parametrize("blah", [(42), (39)])
def test_add2(blah):
    assert add(1, 2) == 3
