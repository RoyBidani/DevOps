from datetime import datetime, timedelta
import pytest
from Machine import Machine


@pytest.fixture
def machine():
    return Machine(1)

def test_init(machine):
    assert machine.type == 1
    assert machine.start is not None
    assert machine.end is None
    assert machine.cost == 2

def test_start_machine(machine):
    machine.start_machine()
    assert machine.start is not None

def test_stop_machine(machine):
    machine.stop_machine()
    assert machine.end is not None

def test_calculate_cost(machine):
    # Assuming the machine runs for 5 minutes
    machine.start = datetime.now() - timedelta(minutes=5)
    machine.end = datetime.now()
    expected_cost = machine.cost * 5  # minutes
    calculated_cost = machine.calculate_cost()
    print("\nCalculated cost:", calculated_cost)
    print("Expected cost:", expected_cost)
    assert int(machine.calculate_cost()) == expected_cost



if __name__ == '__main__':
    pytest.main()