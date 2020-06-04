import pytest
from pysms import SIM900
from unittest.mock import Mock
import serial


@pytest.fixture
def sim():
    sim = SIM900()
    sim.open("COM4")
    yield sim
    sim.close()


def test_sim900_write():
    stub_serial = Mock(serial.Serial)
    stub_serial.write.return_value = 3
    sim = SIM900(stub_serial)
    sim.open("COM4")
    res = sim.send("Joe")
    assert 3 == res


def test_sim900_ping():
    stub_serial = Mock(serial.Serial)
    stub_serial.write.return_value = 4
    stub_serial.readline.return_value = b"OK\r\n"
    sim = SIM900(stub_serial)
    sim.open("COM4")
    res = sim.Ping()
    assert "OK" in res
