import at_commands.at_commands as AT
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

    def write(self, data_bytes):
        if self.serial.is_open:
            if self.debug:
                print(f"   [TX] {data_bytes}")
            return self.serial.write(data_bytes)
        else:
            raise Exception("ERROR: Serial port is not open")

    def send(self, data: str):
        self.serial.flush()
        return self.write(data.encode('utf-8'))

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
                if self.debug and len(decoded_line) > 0:
                    print(f"   [RX] Line ignored = {decoded_line}\r\n")
                if line_found:
                    line = b""
                time.sleep(0.1)
                retry += 1

        return (pattern_found, result)

    def wait_for_ok(self, timeout=100):
        result, response = self.wait_for(AT.RE_OK, timeout=timeout)
        return result and "OK" in response

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
        self.send(AT.PING.execute())
        return self.wait_for_ok()

    def is_registered(self):
        stat = 0
        self.send(AT.ETSI_GSM.CREG.read())
        found, creg_rsp = self.wait_for(AT.ETSI_GSM.CREG.regexp())
        if found and self.wait_for_ok():
            data = AT.ETSI_GSM.CREG.parse(creg_rsp)
            stat = data["stat"]
        return True if found and stat == 1 else False

    def set_echo(self, echo=True):
        self.send(AT.HAYES.E.write({"value": 1 if echo else 0}))
        return self.wait_for_ok()

    def set_sms_format(self, sms_mode):
        self.send(AT.ETSI_GSM.CMGF.write({"mode": sms_mode}))
        return self.wait_for_ok()

    def set_error_verbose(self, level):
        self.send(AT.ETSI_GSM.CMEE.write({"n": level}))
        return self.wait_for_ok()

    def get_signal_quality(self):
        rssi = 99
        ber = 99
        self.send(AT.ETSI_GSM.CSQ.execute())
        found, csq_rsp = self.wait_for(AT.ETSI_GSM.CREG.regexp())
        if found and self.wait_for_ok():
            data = AT.ETSI_GSM.CSQ.parse(csq_rsp)
            rssi = data["rssi"]
            ber = data["ber"]
        return (rssi, ber)

    def sms_send(self, address, text):
        # Send CMGS
        self.send(AT.ETSI_GSM.CMGS.write({"address": f"\"{address}\""}))
        # Wait for indicator
        indicator_found, _ = self.wait_for(re.compile("(^>.*)"))
        if indicator_found:
            # Send message and terminate with CTRL+Z
            self.send(text + AT.CTRL_Z)
            # Wait for CMGS confirmation
            cmgs_found, _ = self.wait_for(AT.ETSI_GSM.CMGS.regexp())
            if cmgs_found:
                return self.wait_for_ok()
        return False
