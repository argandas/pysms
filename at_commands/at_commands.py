import re
import at_commands.at_parsers as parsers


AT_PREFFIX = "AT"
AT_TEST = "=?"
AT_READ = "?"
AT_WRITE = "="
AT_EOL = "\r\n"
CTRL_Z = "\x1A"


AT_COMMANDS = {
    "": {
        'cmd': "",
    },
    # Hayes AT Commands - Generic Modem Control
    "GMM": {
        'cmd': "+GMM",
        'rex': "(.+)"
    },
    "GSN": {
        'cmd': "+GSN",
        'rex': "(.+)"
    },
    # Hayes AT Commands - DTE-Modem Interface Control
    "E": {
        'cmd': "E",
        'fmt': "{value}"
    },
    # ETSI GSM 07.07 - Network Service Handling
    "CREG": {
        'cmd': "+CREG",
        'rex': "(^[+]CREG[:] [0-9]+,[0-9]+$)",
        'fmt': "{n}"
    },
    "COPS": {
        'cmd': "+COPS",
        'rex': "(^[+]COPS[:] [0-4]$)",
        'fmt': "{mode}"
    },
    "CMGF": {
        'cmd': "+CMGF",
        'rex': "(^[+]CMGF[:] [0-9]+$)",
        'fmt': "{mode}"
    },
    "CMGS": {
        'cmd': "+CMGS",
        'rex': "(^[+]CMGS[:] [0-9]+$)",
        'fmt': "{address}"
    },
    "CMGR": {
        'cmd': "+CMGR",
        'rex': "(^[+]CMGR[:] .*)",
        'fmt': "{index}"
    },
    "CMGD": {
        'cmd': "+CMGD",
        'fmt': "{index}"
    },
    # ETSI GSM 07.07 - Mobile Equipment Errors
    "CMEE": {
        'cmd': "+CMEE",
        'fmt': "{n}"
    },
    # ETSI GSM 07.07 - Mobile Equipment Control
    "CFUN": {
        'cmd': "+CFUN",
        'fmt': "{fun}"
    },
    "CSQ": {
        'cmd': "+CSQ",
        'rex': "(^[+]CSQ[:] [0-9]+,[0-9]+$)"
    },
    "CCID": {
        'cmd': "+CCID",
        'rex': "(^[0-9a-z]+$)"
    }
}


class AT_BASE:
    def __init__(self, command):
        self.command = command
        self.cmd_test = None
        self.cmd_read = None
        self.cmd_execute = None
        self.cmd_write = None
        self.cmd_regexp = None

    def attach_parser(self, fn_parser):
        self.cmd_parser = fn_parser

    def test(self) -> str:
        return self.cmd_test

    def read(self) -> str:
        return self.cmd_read

    def execute(self) -> str:
        return self.cmd_execute

    def write(self, data: dict) -> str:
        """ AT Write format """
        return self.cmd_write.format(**data)

    def regexp(self) -> str:
        """ AT command response regular expression """
        return self.cmd_regexp

    def parse(self, data: str) -> dict:
        """ AT command response parser """
        if self.cmd_parser:
            return self.cmd_parser(data)


class AT_BASIC_SYNTAX(AT_BASE):
    def __init__(self, command):
        data = AT_COMMANDS[command]
        super().__init__(data['cmd'])
        cmd = AT_PREFFIX + self.command
        self.cmd_execute = cmd + AT_EOL
        if 'fmt' in data:
            self.cmd_write = (cmd + data['fmt'] + AT_EOL)
        else:
            self.cmd_write = None
        if 'rex' in data:
            self.cmd_regexp = re.compile(data['rex'])
        else:
            self.cmd_regexp = None


class AT_S_PARAMETER_SYNTAX(AT_BASE):
    pass


class AT_EXTENDED_SYNTAX(AT_BASE):
    def __init__(self, command):
        data = AT_COMMANDS[command]
        super().__init__(data['cmd'])
        cmd = AT_PREFFIX + self.command
        self.cmd_test = cmd + AT_TEST + AT_EOL
        self.cmd_read = cmd + AT_READ + AT_EOL
        self.cmd_execute = cmd + AT_EOL
        if 'fmt' in data:
            self.cmd_write = (cmd + AT_WRITE + data['fmt'] + AT_EOL)
        else:
            self.cmd_write = None
        if 'rex' in data:
            self.cmd_regexp = re.compile(data['rex'])
        else:
            self.cmd_regexp = None


class __HAYES_AT_COMMANDS():
    E = AT_BASIC_SYNTAX("E")
    GMM = AT_EXTENDED_SYNTAX('GMM')
    GSN = AT_EXTENDED_SYNTAX("GSN")

    def __init__(self):
        pass


class __ETSI_GSM_COMMANDS():
    CREG = AT_EXTENDED_SYNTAX("CREG")
    COPS = AT_EXTENDED_SYNTAX("COPS")
    CMGF = AT_EXTENDED_SYNTAX("CMGF")
    CMGS = AT_EXTENDED_SYNTAX("CMGS")
    CMGR = AT_EXTENDED_SYNTAX("CMGR")
    CMGD = AT_EXTENDED_SYNTAX("CMGD")
    CMEE = AT_EXTENDED_SYNTAX("CMEE")
    CSQ = AT_EXTENDED_SYNTAX("CSQ")
    CCID = AT_EXTENDED_SYNTAX("CCID")
    CFUN = AT_EXTENDED_SYNTAX("CFUN")

    def __init__(self):
        self.CREG.attach_parser(parsers.parse_CREG)
        self.CMGS.attach_parser(parsers.parse_CMGS)
        self.CSQ.attach_parser(parsers.parse_CSQ)


# AT Ping Command
PING = AT_BASIC_SYNTAX("")

# Hayes AT Commands
HAYES = __HAYES_AT_COMMANDS()

# ETSI GSM 07.07 AT Commands
ETSI_GSM = __ETSI_GSM_COMMANDS()

# Regular Expressions
RE_OK = re.compile("(^OK$)")
RE_ERROR = re.compile("(^ERROR.*$)|(^[+]CM[E,S] ERROR:.*$)")
