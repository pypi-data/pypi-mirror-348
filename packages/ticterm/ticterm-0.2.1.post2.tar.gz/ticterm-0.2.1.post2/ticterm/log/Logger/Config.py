from dataclasses import dataclass
import inspect
import typing
import time
import os

from .lib import (
  TimestampMode,
  StackMode,
  LevelLabelMode,
  EmptyMessageMode,
  Level
)

@dataclass
class UpdateFlag:
  """
  Special flags recognized by :meth:`Config.update`
  """
  name: str
  
class Config:
  #: Flag that indicates value should reset to default
  FLAG_DEFAULT : UpdateFlag = UpdateFlag('DEFAULT')
  # FLAG_UNSET   : StateFlag = StateFlag('UNSET')
  
  DEFAULT_VERBOSITY           : int              = Level.LOG #:
  DEFAULT_TAGS                : list[str]        = [] #:
  DEFAULT_PAD_CHAR            : str              = ' ' #:
  DEFAULT_TIMESTAMP_MODE      : TimestampMode    = TimestampMode.OFF #:
  DEFAULT_TIMESTAMP_PRECISION : int              = 4 #:
  DEFAULT_STACK_MODE          : StackMode        = StackMode.OFF #:
  DEFAULT_STACK_LIMIT         : int              = 1 #:
  DEFAULT_EMPTY_MESSAGE_MODE  : EmptyMessageMode = EmptyMessageMode.NEWLINE_ONLY #:
  DEFAULT_LEVEL_LABEL_MODE    : LevelLabelMode   = LevelLabelMode.ON #:
  DEFAULT_PROGRESS_WIDTH      : int              = 40 #:
  
  #: All configuration flags that vary between instances
  MEMBERS : list[str] = [
    'verbosity',
    'tags',
    'pad_char',
    'timestamp_mode',
    'timestamp_precision',
    'stack_mode',
    'stack_limit',
    'empty_message_mode',
    'level_label_mode',
    'progress_width',
    'project_root',
    'start_time'
  ]

  #: Defaults to :attr:`Config.DEFAULT_VERBOSITY`
  verbosity: int
  
  #: A list of tags to prepend to log messages.
  #: Defaults to an empty list
  tags: list[str]
  
  #: Character to use when padding strings
  #: Defaults to :attr:`Config.DEFAULT_PAD_CHAR`
  pad_char: str
  
  #: Defaults to :attr:`Config.DEFAULT_TIMESTAMP_MODE`
  timestamp_mode: TimestampMode

  #: Number of decimal points to be displayed for timestamps.
  #: Defaults to :attr:`Config.DEFAULT_TIMESTAMP_PRECISION`
  timestamp_precision: int
  
  #: Defaults to :attr:`Config.DEFAULT_STACK_MODE`
  stack_mode: StackMode
  
  #: Defaults to :attr:`Config.DEFAULT_STACK_LIMIT`
  stack_limit: StackMode
  
  #: Should generally be ON for accessiblity or readability in non-interactive
  #: (i.e. black-and-white) terminals.
  #: Defaults to :attr:`Config.DEFAULT_LEVEL_LABEL_MODE`
  level_label_mode: LevelLabelMode
  
  #: `Logger.log` behavior when passed an empty message.
  #: Defaults to :attr:`Config.DEFAULT_EMPTY_MESSAGE_MODE`
  empty_message_mode: EmptyMessageMode
  
  #: Progress bar width in characters
  #: Defaults to :attr:`Config.DEFAULT_PROGRESS_WIDTH`
  progress_width: int
  
  #: Path root for stack frames
  project_root : str
  
  #: Logging time start for :attr:`TimestampMode.SINCE_START`
  start_time   : float
  
  def __init__(self):
    self.reset()
    
  def __dict__(self):
    return {
      member: getattr(self, member) for member in self.MEMBERS
    }
  def __str__(self):
    return str(self.__dict__())
    
  def reset(self, **kwargs):
    """
    Calls :meth:`Config.update` with all kwargs set to :attr:`Config.FLAG_DEFAULT`. 
    Any kwargs passed to this function will override the former kwargs.
    e.g. `Config.reset(start_time=None)` will reset everything but `start_time`
    """
    
    update_kwargs = {
      **{kwarg: self.FLAG_DEFAULT for kwarg in self.MEMBERS},
      **kwargs
    }
    
    self.update(**update_kwargs)
  
  def update(self, *, 
             verbosity           : int|None              = None,
             tags                : list[str]|None        = None,
             pad_char            : str|None              = None,
             timestamp_mode      : TimestampMode|None    = None,
             timestamp_precision : int|None              = None,
             stack_mode          : StackMode|None        = None,
             stack_limit         : int|None              = None,
             level_label_mode    : LevelLabelMode|None   = None,
             empty_message_mode  : EmptyMessageMode|None = None,
             progress_width      : int|None              = None,
             project_root        : str|typing.Any|None   = None,
             start_time          : bool|int|None         = None):
    """
    All parameters will accept :attr:`Config.FLAG_DEFAULT` to reset to default value or `None` to keep current value.
    
    :param verbosity: Should be a level/severity int
    :param tags: A list of tags to prepend to log messages
    :param pad_char: Character to use when padding strings.
    :param timestamp_mode: Should be a `TimestampMode` enum.
    :param timestamp_precision: Number of decimal points to be displayed for timestamps.
    :param stack_mode: Should be a `StackMode` enum.
    :param stack_limit: Stack levels to show.
    :param level_label_mode: Should be a `LevelLabelMode` enum.
    :param empty_message_mode: Should be an `EmptyMessageMode` enum.
    :param progress_width: Progress bar width in characters.
    :param project_root: can be truthy to get from top-level module (default), a str (path), or falsey to unset.
    
    :param start_time: `None` will reset start_time if it hasn't already been set (default), truthy will reset it to `time.time()`, 
    any `int` will set it to that `int`.
    """
    
    if verbosity is None:
      pass
    elif verbosity == self.FLAG_DEFAULT:
      self.verbosity = self.DEFAULT_VERBOSITY
    elif isinstance(verbosity, int) and 0 <= verbosity and verbosity <= Level.MAX:
      self.verbosity = verbosity
    else:
      raise TypeError('verbosity kwarg must be an int <= Level.MAX and >= 0')
    
    if tags is None:
      pass
    elif tags == self.FLAG_DEFAULT:
      self.tags = [*self.DEFAULT_TAGS]
    elif hasattr(tags, '__iter__'):
      self.tags = list(tags)
    else:
      raise TypeError('tags kwarg must be iterable')
    
    if pad_char is None:
      pass
    elif pad_char == self.FLAG_DEFAULT:
      self.pad_char = self.DEFAULT_PAD_CHAR
    elif isinstance(pad_char, int) and pad_char >= 0:
      self.pad_char = pad_char
    else:
      raise ValueError('pad_char kwarg must an int >= 0')
    
    if timestamp_mode is None:
      pass
    elif timestamp_mode == self.FLAG_DEFAULT:
      self.timestamp_mode = self.DEFAULT_TIMESTAMP_MODE
    elif timestamp_mode in TimestampMode:
      self.timestamp_mode = timestamp_mode
    else:
      raise ValueError('timestamp_mode kwarg must be member of TimestampMode enum')
    
    if timestamp_precision is None:
      pass
    elif timestamp_precision == self.FLAG_DEFAULT:
      self.timestamp_precision = self.DEFAULT_TIMESTAMP_PRECISION
    elif isinstance(timestamp_precision, int) and timestamp_precision >= 0:
      self.timestamp_precision = timestamp_precision
    else:
      raise ValueError('timestamp_precision kwarg must an int >= 0')
    
    if stack_mode is None:
      pass
    elif stack_mode == self.FLAG_DEFAULT:
      self.stack_mode = self.DEFAULT_STACK_MODE
    elif stack_mode in StackMode:
      self.stack_mode = stack_mode
    else:
      raise ValueError('stack_mode kwarg must be member of StackMode enum')
    
    if stack_limit is None:
      pass
    elif stack_limit == self.FLAG_DEFAULT:
      self.stack_limit = self.DEFAULT_STACK_LIMIT
    elif isinstance(stack_limit, int) and stack_limit >= 0:
      self.stack_limit = stack_limit
    else:
      raise ValueError('stack_limit kwarg must an int >= 0')
    
    if level_label_mode is None:
      pass
    elif level_label_mode == self.FLAG_DEFAULT:
      self.level_label_mode = self.DEFAULT_LEVEL_LABEL_MODE
    elif level_label_mode in LevelLabelMode:
      self.level_label_mode = level_label_mode
    else:
      raise ValueError('level_label_mode kwarg must be member of LevelLabelMode enum')

    if empty_message_mode is None:
      pass
    elif empty_message_mode == self.FLAG_DEFAULT:
      self.empty_message_mode = self.DEFAULT_EMPTY_MESSAGE_MODE
    elif empty_message_mode in EmptyMessageMode:
      self.empty_message_mode = empty_message_mode
    else:
      raise ValueError('empty_message_mode kwarg must be member of EmptyMessageMode enum')
    
    if progress_width is None:
      pass
    elif progress_width == self.FLAG_DEFAULT:
      self.progress_width = self.DEFAULT_PROGRESS_WIDTH
    elif isinstance(progress_width, int) and progress_width > 0:
      self.progress_width = progress_width
    else:
      raise ValueError('progress_width kwarg must be an int larger than 1')
    
    if project_root is None:
      pass
    elif not project_root:
      self.project_root = None
    elif isinstance(project_root, str):
      self.project_root = os.path.abspath(project_root)
    else: # including FLAG_DEFAULT
      frames = []
      frames.append(inspect.currentframe())
      while frames[-1].f_back:
        frames.append(frames[-1].f_back)
          
      if not frames:
        self.project_root = None
      else:
        if module := inspect.getmodule(frames[-1]):
          root = module.__file__
        elif file := inspect.getfile(frames[-1]):
          root = file
        else:
          root = os.getcwd()
          
        self.project_root = os.path.abspath(os.path.dirname(root))
    
    if start_time is None and self.start_time:
      pass
    elif isinstance(start_time, (int, float)):
      self.start_time = start_time
    else:
      self.start_time = time.time()