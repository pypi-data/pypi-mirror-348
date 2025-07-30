from dataclasses import dataclass

from .Logger.lib import (
  LOG_LEVEL_PAD,
  
  TimestampModeInfo,
  TimestampMode,
  TIMESTAMP_MODES,
  StackMode,
  LevelLabelMode,
  EmptyMessageMode,
  Level,
  LogLevel,
  levels,
  level_names,
)

from .Logger.Config import (
  Config,
  UpdateFlag
)
from .Logger.Logger import (
  Logger, 
  LoggerState, 
  ProgressContext
)

#: Default :class:`Logger` instance for convenience.
default_logger = Logger()

#: Alias for :attr:`default_logger.config` (:attr:`Logger.config`)
config = default_logger.config

#: Alias for :meth:`default_logger.debug` (:meth:`Logger.debug`)
debug = default_logger.debug
# debug = _log_factory(level=Level.DEBUG)

#: Alias for :meth:`default_logger.info` (:meth:`Logger.info`)
info = default_logger.info
# info  = _log_factory(level=Level.INFO)

#: Alias for :meth:`default_logger.log` (:meth:`Logger.log`)
log = default_logger.log
# log   = _log_factory(level=Level.LOG)

#: Alias for :meth:`default_logger.warn` (:meth:`Logger.warn`)
warn = default_logger.warn
# warn  = _log_factory(level=Level.WARN)

#: Alias for :meth:`default_logger.error` (:meth:`Logger.error`)
error = default_logger.error
# error = _log_factory(level=Level.ERROR)

#: Alias for :meth:`default_logger.set_progress` (:meth:`Logger.set_progress`)
set_progress = default_logger.set_progress