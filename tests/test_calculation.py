import utilities
from utilities import user, calculation
import pytest

@pytest.fixture
def setup_mock(mocker):
    calculation.clear()
    calculation.create_table()

def test_add_calculation_passed(setup_mock):
    assert calculation.add_calculation(1, 5689, 10) == 1

def test_add_calculation_not_passed(setup_mock):
    assert calculation.add_calculation(1, 5689,  None) == None


def test_get_user_history(setup_mock):
    result1 = [('5689', 10), ('5689', 10), ('5689', 10), ('5689', 10), ('5689', 10), ('5689', 10), ('5689', 10), ('5689', 10), ('5689', 10), ('5689', 10)]
    result2 = [('56', 20)] * 10
    for i in range(0, 20):
       calculation.add_calculation(1, 5689, 10)
    for i in range(0, 20):
       calculation.add_calculation(2, 56, 20)
    assert calculation.get_user_history(1) == result1
    assert calculation.get_user_history(2) == result2
    assert calculation.get_user_history(3) == []
