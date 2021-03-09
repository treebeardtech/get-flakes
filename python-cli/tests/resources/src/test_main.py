import pytest


def divide(x, y):
    if y < 0:
        raise Exception()
    return x / y


def test_add():
    assert divide(1.0, 2) == 0.5


@pytest.mark.parametrize("denom", [(3.0), (0)])
def test_add2(denom: float):
    assert divide(1.0, denom) == 1 / 3
