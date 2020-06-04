import at_commands as at
import serial


class SIM900:
    def __init__(self, serial_handler=None):
        self.serial = serial_handler or serial.Serial()

    def __del__(self):
        if self.serial is not None:
            self.serial.close()

    def open(self, port, baud=9600, timeout=100):
        self.serial.port = port
        self.serial.baudrate = baud
        self.serial.timeout = timeout
        self.serial.open()

    def send(self, data):
        encoded_data = data.encode('utf-8')
        # print("\r\n\t[TX] bytes = ", encoded_data, "len = ", len(encoded_data))
        return self.serial.write(encoded_data)

    def close(self):
        self.serial.close()

    def Ping(self):
        return self.__sendCommand(at.CMD_AT, at.CMD_OK, 1000)

    def __sendCommand(self, command, regexp_response, timeout):
        decoded_data = ""
        if len(command) <= self.send(command + "\r\n"):
            regexp = regexp_response + "|" + at.CMD_ERROR
            data = self.__waitfor(regexp, timeout)
            decoded_data = data.decode("utf-8")
        return decoded_data

    def __waitfor(self, regexp, timeout):
        data = b""
        data = self.serial.readline()
        # print("\r\n\t[RX] bytes = ", data, "len = ", len(data))
        return data
