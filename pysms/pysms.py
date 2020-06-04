from pysms import at_commands as at
import serial


class SIM900:
    def __init__(self):
        self.port = None
        self.serial = None

    def __del__(self):
        if self.serial is not None:
            if self.serial.is_open:
                self.serial.close()

    def open(self, port=None, baud=9600, timeout=100):
        if port is not None:
            self.port = port
            self.serial = serial.Serial(self.port, baud, timeout=timeout)

    def send(self, data):
        encoded_data = data.encode('utf-8')
        print("\r\n\t[TX] bytes = ", encoded_data, "len = ", len(encoded_data))
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
        print("\r\n\t[RX] bytes = ", data, "len = ", len(data))
        return data
