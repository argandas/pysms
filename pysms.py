import at_commands as at
import serial
import time
import multiprocessing


class SERIAL_GSM_MODEM:

    def __init__(self, serial_handler=None, debug=False):
        self.serial = serial_handler or serial.Serial()
        self.debug = debug

    def __del__(self):
        if self.serial is not None:
            self.close()

    def open(self, port, baud=9600, timeout=100):
        self.serial.port = port
        self.serial.baudrate = baud
        self.serial.timeout = timeout
        self.serial.open()

    def close(self):
        self.serial.close()

    def send(self, data):
        return self.write(data.encode('utf-8'))

    def send_and_wait(self, command, pattern):
        data = ""
        if self.debug:
            print(f"[CMD] {command}")
        if len(command) <= self.send(command + at.CMD_EOL):
            time.sleep(0.1)
            data = self.wait_for_pattern(pattern)
        return data

    def write(self, data_bytes):
        if self.debug:
            print(f"\t[TX] bytes = {data_bytes} len = {len(data_bytes)}")
        return self.serial.write(data_bytes)

    def wait_for_pattern(self, pattern):
        while self.serial.in_waiting:
            data = self.serial.readline()

            decoded = data.decode("utf-8")
            if len(decoded) >= 2:
                decoded = decoded[:len(decoded)-2]

            if self.debug:
                print(f"\t[RX] bytes = {data}, len = {len(data)}")

            if pattern.match(decoded):
                if self.debug:
                    print(f"\t[RE] Pattern match = {decoded}")
                return decoded
            elif at.RE_ERROR.match(decoded):
                raise Exception(decoded)

        return ""


class SIMXXX(SERIAL_GSM_MODEM):
    def __init__(self, com_handler=None, port="COM1", baud=9600, debug=False):
        super().__init__(serial_handler=com_handler, debug=debug)
        self.open(port=port, baud=baud)

    def ping(self):
        return self.send_and_wait(
            at.AT_PING,
            at.RE_OK
        )

    def echo(self, echo=True):
        return self.send_and_wait(
            at.AT_ECHO.format(value=1 if echo else 0),
            at.RE_OK
        )

    def set_sms_format(self, sms_mode=at.SMS_MODE_TEXT):
        return self.send_and_wait(
            at.AT_CMGF.format(mode=sms_mode),
            at.RE_OK
        )

    def set_error_verbose(self, level):
        return self.send_and_wait(
            at.AT_CMEE.format(n=level),
            at.RE_OK
        )


class PYSMS:
    def __init__(self, sim=None, port="COM1", baud=9600):
        self.sim = sim or SIMXXX(port=port, baud=baud, debug=True)
        self.sim.echo(False)
        self.sim.set_error_verbose(2)

    def __del__(self):
        self.sim.close()

    def send_sms(self, addr, message):
        self.sim.set_sms_format(at.SMS_MODE_TEXT)
        self.sim.send(at.AT_CMGS.format(address=addr) + at.CMD_EOL)
        self.sim.send_and_wait(message + at.CMD_CTRL_Z, at.RE_CMGS)


pysms = PYSMS(port="COM9")
try:
    pysms.send_sms("3323436739", "Hello world SMS!")
except Exception as e:
    print(f"Exception found: {e}")
finally:
    del pysms
