from dataclasses import dataclass
from enum import Enum
import traceback
import time
import math
import os

from ...esc import color, style, Style

from ..styled_print import styled_print
from .lib import (
  LOG_LEVEL_PAD,
  
  TimestampMode,
  TIMESTAMP_MODES,
  StackMode,
  EmptyMessageMode,
  Level,
  levels,
  level_names
)
from .Config import Config

# PROGRESS_CHARS = ["▖", "▌", "▛", "█"]
PROGRESS_CHARS   = list(map(lambda offset: chr(0x2581 + offset), range(0, 8)))
PROGRESS_ENDCAP  = chr(0x2595)
PROGRESS_CHARS_N = len(PROGRESS_CHARS)

@dataclass
class LoggerState:
  """
  State object for :class:`Logger` instances.
  """
  
  #: Current progress bar value
  progress: float|None      = None
  
  #: Current progress bar target value
  progress_target: float|int|None  = None
      
class Logger:
  #: Instance Configuration
  config: Config
  
  #: Instance state
  state: LoggerState
  
  #: Instance progress context for `with` statements
  progress_context: "ProgressContext"
  
  def __init__(self, *, config: Config|None = None):
    if config is None:
      self.config = Config()
    elif isinstance(config, Config):
      self.config = config
    else:
      raise TypeError('config kwarg must be an instance of log.Config.Config or None')
    
    self.state = LoggerState()
    
    self.progress_context = ProgressContext(self)
  
  def _format_stack(self, limit: int|None = None, ascend: int = 0) -> str:
    stack = list(reversed(traceback.extract_stack()))
    formatted = []
    
    if limit is None:
      limit = self.config.stack_limit
    
    for frame in stack:
      if frame.__module__ == __package__:
        continue
      
      if (frame.filename == __file__ and frame.name in ('func', '_format_stack', 'log', *level_names)):
        continue
      
      path = frame.filename
      if self.config.project_root and path.startswith(self.config.project_root):
        path = os.path.relpath(path, self.config.project_root)
        
      formatted.append(f'{path}:{frame.name}<{frame.lineno}>')
      
    return ' -> '.join(reversed(formatted[ascend:ascend+limit]))
  
  def log(self, *message, level: int = Level.LOG, stack_ascend: int = 0) -> None:  
    """
    Write log message to console
    
    :param level: Log message severity
    :type  level: int
    
    :param stack_ascend: Number of stack frames to ignore. e.g. If this is
                         called from a custom log function, `stack_ascend = 1`
                         would prevent every message saying it originated in
                         your custom log function.
    """
    
    config = self.config
    
    if levels[level].severity < levels[config.verbosity].severity:
      return
    
    level_style = levels[level].style
    
    if not message and self.config.empty_message_mode == EmptyMessageMode.NEWLINE_ONLY:
      print(level_style)
      return
    
    parts = []
    
    if config.timestamp_mode != TimestampMode.OFF:
      timestamp_format = f'{TIMESTAMP_MODES[config.timestamp_mode].pad + 1 + config.timestamp_precision}.{config.timestamp_precision}f'
      
      if config.timestamp_mode == TimestampMode.SINCE_START:
        since_start = time.time() - config.start_time
        parts.append(f'[{since_start:{config.pad_char}>{timestamp_format}}]')
      elif config.timestamp_mode == TimestampMode.EPOCH:
        parts.append(f'[{time.time():{config.pad_char}>{timestamp_format}}]')
      
    if (config.stack_mode == StackMode.ON 
        or (config.stack_mode == StackMode.ONLY_BAD 
            and levels[level].severity >= levels[Level.WARN].severity)):
      stack_result = self._format_stack(ascend=stack_ascend)
      if stack_result:
        parts.append(f'[{stack_result}]')

    parts.append(f'[{levels[level].name.upper():{config.pad_char}>{LOG_LEVEL_PAD}}]')
    
    if self.config.tags:
      parts.append(f'[{':'.join(self.config.tags)}]')

    parts = color.normal + ' '.join(parts)
    
    if self.state.progress is not None:
      parts = '\033[2K' + parts # clearline
    
    if level == Level.LOG:    
      styled_print(parts, *message)
    else:
      styled_print(parts, *message, normal=level_style)
      
    if self.state.progress is not None:
      self._print_progress_()
    
  def debug(self, *message, stack_ascend: int = 0) -> None:
    """
    Alias for :meth:`~Logger.log` with `level` kwarg set to :attr:`Level.DEBUG`
    """
    return self.log(*message, level=Level.DEBUG, stack_ascend=stack_ascend)

  def  info(self, *message, stack_ascend: int = 0) -> None:
    """
    Alias for :meth:`~Logger.log` with `level` kwarg set to :attr:`Level.INFO`
    """
    return self.log(*message, level=Level.INFO, stack_ascend=stack_ascend)

  def  warn(self, *message, stack_ascend: int = 0) -> None:
    """
    Alias for :meth:`~Logger.log` with `level` kwarg set to :attr:`Level.WARN`
    """
    return self.log(*message, level=Level.WARN, stack_ascend=stack_ascend)

  def error(self, *message, stack_ascend: int = 0) -> None:
    """
    Alias for :meth:`~Logger.log` with `level` kwarg set to :attr:`Level.ERROR`
    """
    return self.log(*message, level=Level.ERROR, stack_ascend=stack_ascend)

  def set_progress(self, value: float|int|bool|None = None, target: float|int|None = None) -> "ProgressContext":
    """
    Updates current logger progress.
    
    :param value: Can be a `float` or `int` above 0,
                  `True` to finalize progress bar and prevent it from being overwritten then disable it,
                  or `None` to disable progress bar.
                  Defaults to `None`
    :type  value: float, int, bool, None, optional
    
    :param target: Can be a `float` or `int` above 0 or `None` to not change.
    :type  target: float, int, optional
    
    :rtype: ProgressContext
    """
    if target is not None:
      self.state.progress_target = target
      
    if value is True:
      self._print_progress_(finalize=True)
      self.state.progress = None
    else:
      if value is not None and self.state.progress_target is None:
        raise ValueError('progress value was set without a progress target set.')
      
      self.state.progress = value
      self._print_progress_()
    
    return self.progress_context
  
  def _print_progress_(self, *, finalize: bool = False):
    if self.state.progress is None:
      return
    
    ratio   = max(0, min(1, self.state.progress / self.state.progress_target))
    space   = max(1, self.config.progress_width - 2)
    steps   = space * PROGRESS_CHARS_N
    parts   = ratio * steps
    whole   = int(parts // PROGRESS_CHARS_N)
    partial = math.floor(parts % PROGRESS_CHARS_N)
    empty   = space - whole - (1 if partial != 0 else 0)
    
    # print(f'[   {parts}/{steps} = {whole} + ({partial}/{PROGRESS_CHARS_N})   ]\r', end='')
    print(
      '  '
      + f'{PROGRESS_CHARS[-1] * whole}'
      + f'{'' if not partial else PROGRESS_CHARS[partial]}'
      + f'{(' ' * (empty - 1)) if empty > 1 else ''}'
      + f'{PROGRESS_ENDCAP if empty != 0 else ''}'
      + '\r', 
      end=''
    )
    
    if finalize:
      print()
    
Logger.log.debug = Logger.debug
Logger.log.info = Logger.info
Logger.log.warn = Logger.warn
Logger.log.error = Logger.error

class ProgressContext:
  """
  Context object for :class:`Logger` progress bars for use in `with` statements.
  
  Calls `logger.set_progress(True)` to finalize progress bar on exit.
  
  Usage: 
  
  .. highlight:: python
  .. code-block:: python
  
    logger = Logger()
    
    with logger.set_progress(0, 100) as update:
      for value in range(0, 100, 5):
        update(value)
        # or
        logger.set_progress(value)
  """
  logger: Logger
  
  def __init__(self, logger):
    self.logger = logger
    
  def __call__(self, ratio: float|bool|None = None):
    """
    Wrapper for `self.logger.set_progress`
    """
    return self.logger.set_progress(ratio)
    
  def __enter__(self):
    return self
  
  def __exit__(self, exc_type, exc_value, traceback):
    self.logger.set_progress(True)