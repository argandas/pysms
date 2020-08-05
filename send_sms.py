from pysms import PYSMS
import sys
import getopt


def sendsms(address, message, debug):
    pysms = PYSMS(port="COM9", baud=115200, debug=debug)
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
    msg = ''
    debug = False
    try:
        opts, _ = getopt.getopt(
            argv,
            "hda:m:",
            ["addr=", "msg="]
        )
    except getopt.GetoptError:
        print('example.py -a <addr> -m <msg> -d')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('example.py -a <addr> -m <msg> -d')
            sys.exit()
        elif opt in ("-d"):
            debug = True
        elif opt in ("-a", "--addr"):
            addr = arg
        elif opt in ("-m", "--msg"):
            msg = arg

    sendsms(addr, msg, debug)


if __name__ == "__main__":
    main(sys.argv[1:])
