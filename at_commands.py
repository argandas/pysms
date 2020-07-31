import re


AT_PREFFIX = "AT"
AT_TEST = "=?"
AT_READ = "?"
AT_WRITE = "="
AT_EOL = "\r\n"
CTRL_Z = "\x1A"


class AT_BASIC_SYNTAX:
    def __init__(self, command, regexp=None, fmt=None):
        self.command = AT_PREFFIX + command
        self.cmd_execute = self.command + AT_EOL
        self.cmd_write = (self.command + fmt + AT_EOL) if fmt else None
        self.cmd_regexp = re.compile(regexp) if regexp else None

    def execute(self):
        return self.cmd_execute

    def write(self, data):
        return self.cmd_write.format(**data)

    def regexp(self):
        return self.cmd_regexp


class AT_S_PARAMETER_SYNTAX:
    pass


class AT_EXTENDED_SYNTAX:
    def __init__(self, command, regexp=None, fmt=None):
        self.cmd = AT_PREFFIX + command
        self.cmd_test = self.cmd + AT_TEST + AT_EOL
        self.cmd_read = self.cmd + AT_READ + AT_EOL
        self.cmd_execute = self.cmd + AT_EOL
        self.cmd_write = (self.cmd + AT_WRITE + fmt + AT_EOL) if fmt else None
        self.cmd_regexp = re.compile(regexp) if regexp else None

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

CREG = AT_EXTENDED_SYNTAX(
    "+CREG",
    regexp="(^[+]CREG[:] [0-9]+,[0-9]+$)",
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

CMGS = AT_EXTENDED_SYNTAX(
    "+CMGS",
    regexp="(^[+]CMGS[:] [0-9]+$)",
    fmt="{address}"
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
