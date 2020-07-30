import pytest
import pysms
from unittest.mock import Mock
import serial


@pytest.fixture
def sim():
    sim = pysms.SERIAL_GSM_MODEM()
    sim.open("COM4")
    yield sim
    sim.close()


def test_sim900_write():
    stub_serial = Mock(serial.Serial)
    stub_serial.write.return_value = 3
    sim = pysms.SERIAL_GSM_MODEM(stub_serial)
    sim.open("COM4")
    res = sim.send("Joe")
    assert 3 == res


def test_sim900_ping():
    stub_serial = Mock(serial.Serial)
    stub_serial.write.return_value = 4
    stub_serial.readline.return_value = b"OK\r\n"
    sim = pysms.SIMXXX(stub_serial)
    res = sim.ping()
    assert "OK" in res


def test_cme_error_exception():
    with pytest.raises(Exception) as excinfo:
        stub_serial = Mock(serial.Serial)
        stub_serial.write.return_value = 4
        stub_serial.readline.return_value = b"+CME ERROR: Unexpected error\r\n"
        sim = pysms.SIMXXX(stub_serial)
        sim.ping()
    assert "+CME ERROR" in str(excinfo.value)


def test_cms_error_exception():
    with pytest.raises(Exception) as excinfo:
        stub_serial = Mock(serial.Serial)
        stub_serial.write.return_value = 4
        stub_serial.readline.return_value = b"+CMS ERROR: Unexpected error\r\n"
        sim = pysms.SIMXXX(stub_serial)
        sim.ping()
    assert "+CMS ERROR" in str(excinfo.value)


def test_generic_error_exception():
    with pytest.raises(Exception) as excinfo:
        stub_serial = Mock(serial.Serial)
        stub_serial.write.return_value = 4
        stub_serial.readline.return_value = b"ERROR\r\n"
        sim = pysms.SIMXXX(stub_serial)
        sim.ping()
    assert "ERROR" in str(excinfo.value)
