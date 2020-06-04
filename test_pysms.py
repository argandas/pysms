import pytest
from pysms import SIM900


@pytest.fixture
def sim():
    sim = SIM900()
    sim.open("COM4")
    yield sim
    sim.close()


def test_sim900_write(sim):
    res = sim.send("Joe")
    assert 3 == res


@pytest.mark.skip(reason="HW is required to test this function")
def test_sim900_ping(sim):
    res = sim.Ping()
    assert "OK" in res
