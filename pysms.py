import at_commands.at_commands as AT
import sys
import getopt
from simxxx.simxxx import SIMXXX


class PYSMS:
    def __init__(self, sim=None, port="COM1", baud=9600, debug=False):
        self.sim = sim or SIMXXX(port=port, baud=baud, debug=debug)
        if self.sim.ping():
            self.sim.set_echo(False)
            self.sim.set_error_verbose(2)
        else:
            raise Exception("Failed to ping the SIM Module")

    def __del__(self):
        self.sim.close()

    def send_sms(self, addr, msg):
        if self.sim.is_registered():
            # Set text mode
            self.sim.set_sms_format(1)
            # Request to send SMS.
            return self.sim.sms_send(addr, msg)
        else:
            raise Exception("The SIM module is not registered in the network")

    def passthrough(self):
        while 1:
            data = input()
            if data == "CTRL+Z":
                self.sim.send(AT.CTRL_Z)
            elif data == "exit":
                break
            elif data != "":
                self.sim.send(data + AT.AT_EOL)
                self.sim.wait_for_ok()


def main(argv):
    addr = ''
    port = ''
    msg = ''
    debug = False

    def print_usage():
        print('Usage:')
        print('\t-p, --port\t: Serial port to use')
        print('\t-a, --addr\t: Destination address of the SMS')
        print('\t-m, --msg \t: Message to send')
        print('\t-d        \t: Enable AT commands debug')
        print('\r\nExamples:')
        print('\tsend_sms.py -a <addr> -m <msg>')
        print('\tsend_sms.py --addr=<addr> --msg=<msg>')
        print('\tsend_sms.py -d -a <addr> -m <msg>')

    try:
        opts, _ = getopt.getopt(
            argv,
            "hda:m:p:",
            ["addr=", "msg=", "port="]
        )
    except getopt.GetoptError:
        print('ERROR: Invalid syntax')
        print_usage()
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print_usage()
            sys.exit()
        elif opt in ("-d"):
            debug = True
        elif opt in ("-a", "--addr"):
            addr = arg
        elif opt in ("-m", "--msg"):
            msg = arg
        elif opt in ("-p", "--port"):
            port = arg

    sms_handler = PYSMS(port=port, baud=115200, debug=debug)
    try:
        print(f"Send SMS: addr=\"{addr}\", msg=\"{msg}\"")
        if sms_handler.send_sms(addr, msg):
            print("OK")
        else:
            print("ERROR")
        # sms_handler.passthrough()

    except Exception as e:
        print(f"Exception found: {e}")
    finally:
        del sms_handler


if __name__ == "__main__":
    main(sys.argv[1:])
