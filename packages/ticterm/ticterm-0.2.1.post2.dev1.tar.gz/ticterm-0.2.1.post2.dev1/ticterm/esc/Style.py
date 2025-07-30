import typing

class Style:
  """
  Terminal escape code style
  
  :param value: Escape sequence to enable style
  :param value_off: Escape sequence to disable style
  """
  
  #: 
  value     : str
  
  #: 
  value_off : str
  
  def __init__(self, value: str, value_off: str = '\033[m'):
    self.value     = str(value)
    self.value_off = str(value_off)
  
  def __str__(self):
    return str(self.value)
  
  def __repr__(self):
    return f'Style(value={repr(self.value)}, value_off={repr(self.value_off)})'
  
  def wrap(self, item: str|typing.Any) -> str:
    """
    Wraps `str(item)` with :attr:`value` and :attr:`value_off` (if available)
    
    :param item:
    """
    return f'{self.value}{item}{self.value_off or ""}'
  
  def wrap_many(self, items: iter) -> map:
    """
    Maps :meth:`Style.wrap` to `items` iterable
    
    :param items:
    """
    return map(self.wrap, items)
  
  def replace_normal(self, item) -> str:
    """
    Replaces all instances of :attr:`ticterm.esc.color.normal` in `items`.
    
    :param style:
    :param items:
    """
    return str(item).replace('\033[39m', str(self.value))

  def replace_normal_many(self, items: iter) -> map:
    """
    Maps :meth:`Style.replace_normal` to `items` iterable
    
    :param items:
    """
    return map(self.replace_normal, items)
    
  @staticmethod
  def combine(*styles: typing.Self) -> typing.Self:
    """
    Combines multiple :class:`Style` objects into one.
    """
    values     = []
    values_off = []
    
    for style in styles:
      if not style.value:
        continue
      values.append(style.value)
      
      if not style.value_off:
        continue
      values_off.append(style.value_off)
    
    return Style(
      ''.join(values),
      ''.join(values_off)
    )
    
  def add(self, *styles: typing.Self) -> typing.Self:
    """
    Combines self with all `styles`
    """
    return Style.combine(self, *styles)
  
  def __add__(self, target) -> typing.Self|str:
    if isinstance(target, Style):
      return Style.combine(self, target)
    else:
      return self.__str__() + target
  
  def __iadd__(self, target) -> typing.Self|str:
    # self = Style.combine(self, target)
    self = self.__add__(target)
    return self