import re


AT_PREFFIX = "AT"
AT_TEST = "=?"
AT_READ = "?"
AT_WRITE = "="
AT_EOL = "\r\n"
CTRL_Z = "\x1A"


class AT_BASE:
    def __init__(self, command):
        self.command = command
        self.cmd_test = None
        self.cmd_read = None
        self.cmd_execute = None
        self.cmd_write = None
        self.cmd_regexp = None
        self.cmd_parser = None

    def test(self):
        return self.cmd_test

    def read(self):
        return self.cmd_read

    def execute(self):
        return self.cmd_execute

    def write(self, data):
        return self.cmd_write.format(**data)

    def regexp(self):
        return self.cmd_regexp

    def parse(self, data):
        if self.cmd_parser:
            return self.cmd_parser(data)


class AT_BASIC_SYNTAX(AT_BASE):
    def __init__(self, command, regexp=None, fmt=None):
        super().__init__(command)
        cmd = AT_PREFFIX + self.command
        self.cmd_execute = cmd + AT_EOL
        self.cmd_write = (cmd + fmt + AT_EOL) if fmt else None
        self.cmd_regexp = re.compile(regexp) if regexp else None


class AT_S_PARAMETER_SYNTAX(AT_BASE):
    pass


class AT_EXTENDED_SYNTAX(AT_BASE):
    def __init__(self, command, regexp=None, fmt=None, parser=None):
        super().__init__(command)
        cmd = AT_PREFFIX + self.command
        self.cmd_test = cmd + AT_TEST + AT_EOL
        self.cmd_read = cmd + AT_READ + AT_EOL
        self.cmd_execute = cmd + AT_EOL
        self.cmd_write = (cmd + AT_WRITE + fmt + AT_EOL) if fmt else None
        self.cmd_regexp = re.compile(regexp) if regexp else None
        self.cmd_parser = parser


# AT Write/Set Commands
PING = AT_BASIC_SYNTAX("")
ECHO = AT_BASIC_SYNTAX("E", fmt="{value}")

CSQ = AT_EXTENDED_SYNTAX(
    "+CSQ",
    regexp="(^[+]CSQ[:] [0-9]+,[0-9]+$)",
)

CCID = AT_EXTENDED_SYNTAX(
    "+CCID",
    regexp="(^[0-9a-z]+$)",
)


def parse_CREG(data):
    cmd, rsp = tuple(data.split(" "))
    assert(cmd[:-1] == CREG.command)
    args = rsp.split(",")
    ans = {"n": int(args[0]), "stat": int(args[1])}
    return ans


CREG = AT_EXTENDED_SYNTAX(
    "+CREG",
    regexp="(^[+]CREG[:] [0-9]+,[0-9]+$)",
    parser=parse_CREG
)

COPS = AT_EXTENDED_SYNTAX(
    "+COPS",
    regexp="(^[+]COPS[:] .*$)",
)

CMGF = AT_EXTENDED_SYNTAX(
    "+CMGF",
    regexp="(^[+]CMGF[:] [0-9]+$)",
    fmt="{mode}"
)


def parse_CMGS(data):
    cmd, rsp = tuple(data.split(" "))
    assert(cmd[:-1] == CMGS.command)
    args = rsp.split(",")
    ans = {"mr": int(args[0])}
    return ans


CMGS = AT_EXTENDED_SYNTAX(
    "+CMGS",
    regexp="(^[+]CMGS[:] [0-9]+$)",
    fmt="{address}",
    parser=parse_CMGS
)


CMGR = AT_EXTENDED_SYNTAX(
    "+CMGR",
    regexp="(^[+]CMGR[:] .*)"
)

CMGD = AT_EXTENDED_SYNTAX(
    "+CMGD",
    fmt="{index}"
)

CMEE = AT_EXTENDED_SYNTAX(
    "+CMEE",
    fmt="{n}"
)

CFUN = AT_EXTENDED_SYNTAX(
    "+CFUN",
    fmt="{fun}"
)

GMM = AT_EXTENDED_SYNTAX("+GMM", regexp="(.+)")
GSN = AT_EXTENDED_SYNTAX("+GSN", regexp="(.+)")

# Regular Expressions
RE_OK = re.compile("(^OK$)")
RE_ERROR = re.compile("(^ERROR.*$)|(^[+]CM[E,S] ERROR:.*$)")
