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


def test_sim900_send():
    stub_serial = Mock(serial.Serial)
    stub_serial.write = lambda x: len(x)
    stub_serial.is_open = True
    sim = pysms.SERIAL_GSM_MODEM(stub_serial)
    res = sim.send("Joe")
    assert 3 == res


def test_sim900_write():
    stub_serial = Mock(serial.Serial)
    stub_serial.write = lambda x: len(x)
    stub_serial.is_open = True
    sim = pysms.SERIAL_GSM_MODEM(stub_serial)
    res = sim.write([bytes(x, 'utf-8') for x in "1234567890"])
    assert 10 == res


def test_sim900_write_port_not_open():
    stub_serial = Mock(serial.Serial)
    stub_serial.write = lambda x: len(x)
    stub_serial.is_open = False
    sim = pysms.SERIAL_GSM_MODEM(stub_serial)
    with pytest.raises(Exception) as excinfo:
        sim.write([bytes(x, 'utf-8') for x in "1234567890"])
    assert "ERROR" in str(excinfo.value)


def test_sim900_ping():
    stub_serial = Mock(serial.Serial)
    data_to_read = "OK\r\n"
    stub_serial.write = lambda x: len(x)
    stub_serial.is_open = True
    stub_serial.read.side_effect = [bytes(x, 'utf-8') for x in data_to_read]
    sim = pysms.SIMXXX(stub_serial)
    res = sim.ping()
    assert "OK" in res
    assert sim.serial.write("hello") == 5


"""
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

"""