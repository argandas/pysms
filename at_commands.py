import re


# AT commands
CMD_CMGF_RX = "+CMGF: "
CMD_CMGR_RX = "+CMGR: "
CMD_CMTI_RX = "+CMTI: \"SM\","

# Special commands
CMD_CTRL_Z = "\x1A"
CMD_EOL = "\r\n"

# AT Write/Set Commands
AT_PING = "AT"
AT_ECHO = "ATE {value}"
AT_CMGF = "AT+CMGF={mode}"
AT_CMGS = "AT+CMGS=\"{address}\""
AT_CMGR = "AT+CMGR={index}"
AT_CMGD = "AT+CMGD={index}"
AT_CMEE = "AT+CMEE={n}"

# Queries
QUERY_CMGF = "AT+CMGF?"

# Regular Expressions
RE_OK = re.compile("(^OK$)")
RE_ERROR = re.compile("(^ERROR$)|(^[+]CM[E,S] ERROR:.*$)")
RE_CMGF = re.compile("(^[+]CMGF[:] [0-9]+$)")
RE_CMTI = re.compile("(^[+]CMTI[:] \"SM\",[0-9]+$)")
RE_CMGR = re.compile("(^[+]CMGR[:] .*)")
RE_CMGS = re.compile("(^[+]CMGS[:] [0-9]+$)")

# SMS Message Format
SMS_MODE_PDU = 0
SMS_MODE_TEXT = 1
