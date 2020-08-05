import at_commands as AT
import serial
import time
import re


class SERIAL_GSM_MODEM:

    def __init__(self, serial_handler=None, debug=False):
        self.serial = serial_handler or serial.Serial()
        self.serial.timeout = 1
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

    def send(self, data: str):
        return self.write(data.encode('utf-8'))

    def send_command(self, command, pattern=None, timeout=100):
        response = None
        self.send(command)
        if pattern:
            response = self.wait_for(pattern, timeout=timeout)
        if not self.wait_for(AT.RE_OK, timeout=timeout):
            raise Exception(f"Missing closure for command: {command}")
        return response

    def write(self, data_bytes):
        if self.debug:
            print(f"   [TX] {data_bytes}")
        return self.serial.write(data_bytes)

    def wait_for(self, pattern, timeout=100):
        pattern_found = False
        result = None
        line_found = False
        retry = 0
        line = b""
        while retry < timeout:
            line_found, line = self.readline(line)

            # Decode byte string
            decoded_line = line.decode("utf-8")

            if pattern.match(decoded_line):
                ''' Search for pattern '''
                if self.debug:
                    print(f"   [RE] Pattern match = {decoded_line}\r\n")
                pattern_found = True
                result = decoded_line
                break
            elif AT.RE_ERROR.match(decoded_line):
                """ Search for errors """
                raise Exception(decoded_line)
            # Retry
            else:
                if line_found:
                    line = b""
                time.sleep(0.1)
                retry += 1

        return (pattern_found, result)

    def readline(self, line, timeout=100):
        line_found = False
        while self.serial.in_waiting:
            c = self.serial.read()
            if c == b'\r':
                continue
            if c == b'\n':
                line_found = True
                break
            line += c

        if self.debug and len(line) > 0:
            print(f"   [RX] {line}")

        return (line_found, line)


class SIMXXX(SERIAL_GSM_MODEM):
    def __init__(self, com_handler=None, port="COM1", baud=9600, debug=False):
        super().__init__(serial_handler=com_handler, debug=debug)
        self.open(port=port, baud=baud)

    def ping(self):
        return self.send_command(AT.PING.execute())

    def set_echo(self, echo=True):
        return self.send_command(AT.ECHO.write({"value": 1 if echo else 0}))

    def set_sms_format(self, sms_mode):
        return self.send_command(AT.CMGF.write({"mode": sms_mode}))

    def set_error_verbose(self, level):
        return self.send_command(AT.CMEE.write({"n": level}))

    def get_signal_quality(self):
        return self.send_command(AT.CSQ.execute(), pattern=AT.CSQ.regexp())

    def is_registered(self):
        stat = 0

        found, creg_rsp = self.send_command(
            AT.CREG.read(),
            pattern=AT.CREG.regexp()
        )

        if found:
            data = AT.CREG.parse(creg_rsp)
            stat = data["stat"]

        return True if found and stat == 1 else False


class PYSMS:
    def __init__(self, sim=None, port="COM1", baud=9600, debug=False):
        self.sim = sim or SIMXXX(port=port, baud=baud, debug=debug)
        self.sim.ping()
        self.sim.set_echo(False)
        self.sim.set_error_verbose(2)
        self.sim.send_command(AT.CCID.execute(), pattern=AT.CCID.regexp())
        self.sim.send_command(AT.COPS.read(), pattern=AT.COPS.regexp())
        self.sim.get_signal_quality()

    def __del__(self):
        self.sim.close()

    def send_sms(self, addr, msg):
        sent = False
        if self.sim.is_registered():
            # Set text mode
            self.sim.set_sms_format(1)
            # Request to send SMS.
            self.sim.send(AT.CMGS.write({"address": f"\"{addr}\""}))
            # Wait for indicator
            if self.sim.wait_for(re.compile("(^>.*)")):
                # Send message and terminate with CTRL+Z
                found, _ = self.sim.send_command(
                    msg + AT.CTRL_Z,
                    pattern=AT.CMGS.regexp()
                )

                sent = found
        return sent

    def passtrough(self):
        while 1:
            data = input()
            if data == "CTRL+Z":
                self.sim.send(AT.CTRL_Z)
            elif data == "exit":
                break
            elif data != "":
                self.sim.send_command(data + AT.AT_EOL)
