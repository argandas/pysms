from pysms import PYSMS
import sys
import getopt


def sendsms(port, address, message, debug):
    pysms = PYSMS(port=port, baud=115200, debug=debug)
    try:
        print(f"Send SMS: addr=\"{address}\", msg=\"{message}\"")
        if pysms.send_sms(address, message):
            print("OK")
        else:
            print("ERROR")

    except Exception as e:
        print(f"Exception found: {e}")
    finally:
        del pysms


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

    sendsms(port, addr, msg, debug)


if __name__ == "__main__":
    main(sys.argv[1:])
