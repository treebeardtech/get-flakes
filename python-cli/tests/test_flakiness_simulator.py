import random

import pytest

random.uniform(0, 1)

N_TESTS = 10000
BUG_THRESHOLD = 1.0 / 10000
FLAKY_TESTS = [130, 3000, 8400, 9900]
FLAKE_THRESHOLD = 1.0 / 6


def get_tests():
    return [ii for ii in range(N_TESTS)]


@pytest.mark.flakysim
@pytest.mark.parametrize("ii", get_tests())
def test_eval(ii: int):
    change_quality = random.uniform(0, 1)
    assert change_quality > BUG_THRESHOLD, "real bug"

    if ii in FLAKY_TESTS:
        test_exec_quality = random.uniform(0, 1)
        assert test_exec_quality > FLAKE_THRESHOLD, "flaky test"
