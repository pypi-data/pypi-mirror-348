from .Style import Style

#: List of color names.
color_names: list[str] = [
  'black',
  'red',
  'green',
  'yellow',
  'blue',
  'magenta',
  'cyan',
  'white'
]

# color_names_bright = [
#   f'br{name}' for name in color_names
# ]

#: List of color names prepended with `'br'` mapped to their non-bright
#: counterparts.
color_bright_map: dict[str, str] = {
  f'br{name}': name for name in color_names
}

#: Map of color names to their ansi escape code ids.
color_map: dict[str, int] = {
  name: 30 + i for i, name in enumerate(color_names)
}

# color_map.update({
#   name: 90 + i for i,name in enumerate(color_names_bright)
# })

#: Normal color and style
normal = Style('\033[39m', '')

def get(color: Style|int|str, *, bg: bool=False) -> Style:
  """
  Get color or style from input. Accepts :class:`Style` objects, ansi color ids, or names.
  
  :param color:
  
  :param bg: Should background color escape code be returned instead of foreground?
  """
  
  if isinstance(color, Style) or str(color).startswith('\033'):
    return color
  
  elif color =='normal':
    return normal
  
  elif color in color_map or color in color_bright_map:
    if color in color_map:
      color_code = color_map[color]
    else:
      color_code = color_map[color_bright_map[color]] + 60
    
    if bg:
      color_code += 10
      
    return Style(f'\033[{color_code}m', normal)

def replace_normal(style: Style|int|str, *items: str) -> list[str]|str:
  """
  Replaces all instances of :attr:`normal` in `items`.
  
  :param style:
  :param items:
  """
  if not isinstance(items, (list, tuple)):
    items = [items]
  
  style = get(style)
  
  output = []
  for item in items:
    output.append(str(item).replace('\033[39m', str(style.value)))
  
  if len(items) == 1:
    return output[0]
  
  return output
  
black   = get('black') #:
red     = get('red') #:
green   = get('green') #:
yellow  = get('yellow') #:
blue    = get('blue') #:
magenta = get('magenta') #:
cyan    = get('cyan') #:
white   = get('white') #:

brblack   = get('brblack') #:
brred     = get('brred') #:
brgreen   = get('brgreen') #:
bryellow  = get('bryellow') #:
brblue    = get('brblue') #:
brmagenta = get('brmagenta') #:
brcyan    = get('brcyan') #:
brwhite   = get('brwhite') #:
