import at_commands.at_commands as AT


def parse_CMGS(data):
    cmd, rsp = tuple(data.split(" "))
    assert(cmd[:-1] == AT.ETSI_GSM.CMGS.command)
    args = rsp.split(",")
    ans = {"mr": int(args[0])}
    return ans


def parse_CREG(data):
    cmd, rsp = tuple(data.split(" "))
    assert(cmd[:-1] == AT.ETSI_GSM.CREG.command)
    args = rsp.split(",")
    ans = {"n": int(args[0]), "stat": int(args[1])}
    return ans


def parse_CSQ(data):
    cmd, rsp = tuple(data.split(" "))
    assert(cmd[:-1] == AT.ETSI_GSM.CSQ.command)
    args = rsp.split(",")
    ans = {"rssi": int(args[0]), "ber": int(args[1])}
    return ans
