from dataclasses import dataclass
from enum import Enum

from ...esc import color, style, Style

@dataclass
class TimestampModeInfo:
  pad: int
  
class TimestampMode(Enum):
  """
  Timestamp Modes
  """
  #: Disables timestamps
  OFF         = 0
  #: Shows time since start
  SINCE_START = 1
  #: Shows time since epoch (unix time)
  EPOCH       = 2

TIMESTAMP_MODES = {
  # 10 ** 8 == ~1157 days before padding is messed up
  TimestampMode.SINCE_START : TimestampModeInfo(pad = 8), 
  TimestampMode.EPOCH       : TimestampModeInfo(pad = 10)
}

class StackMode(Enum):
  #: Disables stacks
  OFF = 0
  #: Enables stacks
  ON  = 1
  #: Only show on `Level.WARN` or above
  ONLY_BAD = 2
  
class LevelLabelMode(Enum):
  #: Disables log level label
  OFF = 0
  #: Enables log level label
  ON  = 1
  
class EmptyMessageMode(Enum):
  #: Print just a newline (i.e. `print()`)
  NEWLINE_ONLY = 0
  #: Print log output as normal just with a blank message.
  NORMAL = 1

class Level:
  """
  Log severity levels
  """
  #: Debug
  DEBUG = 0
  #: Info
  INFO  = 1
  #: Log
  LOG   = 2
  #: Warn
  WARN  = 3
  #: Error
  ERROR = MAX = 4
    
@dataclass
class LogLevel:
  name: str
  severity: int
  style: Style

levels: dict[Level, LogLevel] = {
  Level.DEBUG : LogLevel(name='debug', severity=Level.DEBUG, style=color.normal + style.dim),
  Level.INFO  : LogLevel(name='info',  severity=Level.INFO,  style=color.cyan),
  Level.LOG   : LogLevel(name='log',   severity=Level.LOG,   style=color.normal),
  Level.WARN  : LogLevel(name='warn',  severity=Level.WARN,  style=color.yellow),
  Level.ERROR : LogLevel(name='error', severity=Level.ERROR, style=color.brred)
}

# To avoid recalculating on every _format_stack call
#: List of all level names
level_names   : list[str] = list(map(lambda level: level.name, levels.values()))

#: Longest level name length
LOG_LEVEL_PAD : int = max(map(len, level_names))