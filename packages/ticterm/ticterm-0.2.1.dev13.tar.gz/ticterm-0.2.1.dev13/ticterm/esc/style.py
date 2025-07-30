
from .Style import Style

bold      = Style('\033[1m', '\033[22m')
dim       = Style('\033[2m', '\033[22m')
italic    = Style('\033[3m', '\033[23m')
underline = Style('\033[4m', '\033[24m')
blinking  = Style('\033[5m', '\033[25m')
inverse   = Style('\033[7m', '\033[27m')