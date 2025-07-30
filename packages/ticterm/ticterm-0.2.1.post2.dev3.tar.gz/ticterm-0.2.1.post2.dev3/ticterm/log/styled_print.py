from ..esc import color, Style

from . import styling

_print = print
def styled_print(*message, normal: Style = None, highlight: bool = True):
  if highlight:
    message = map(styling.style_object, message)
  else:
    message = map(str, message)
  
  if normal:
    message = normal.wrap_many(message)
    message = normal.replace_normal_many(message)
  else:
    normal = color.normal
        
  # message = [ part + str(color.normal) for part in message ]
  message = ' '.join(message)
    
  _print(color.normal + message)