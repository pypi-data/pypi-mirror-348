from dataclasses import dataclass
import re

from ..esc import color, style, Style

@dataclass
class HighlightingRule:
  regexp: re.Pattern
  repl: callable
  
@dataclass
class StyleRule:
  check: callable
  repl: callable

highlighting_rules = {
  'numbers': HighlightingRule(
    regexp = re.compile(
      r'(?:(?<=^)|(?<=[\s=\(]))' # can either be lead by any characters in the positive lookbehind
      + r'(?:'
      + r'(0x[0-9a-f]+)'
      + r'|(0b[01]+)'
      + r'|(\d+(?:(\.)(\d+))?)'
      + r')'
      + r'(?:(?=$)|(?=[\s,\)]))' # can be followed by any of the characters in the positive lookahead
    ),
    repl = lambda match: (color.brblue).wrap(match.group(0))
  ),
  'literals': HighlightingRule(
    regexp = re.compile(r'(None|True|False)'),
    repl   = lambda match: color.brmagenta.wrap(match.group(0))
  ),
  'strings_double': HighlightingRule(
    regexp = re.compile(r'"((?:\\"|[^"])*)"'),
    repl   = lambda match: f'{color.bryellow}"{color.bryellow.replace_normal(match.group(1))}{color.bryellow}"{color.normal}'
  ),
  'strings_single': HighlightingRule(
    regexp = re.compile(r"'((?:\\'|[^'])*)'"),
    repl   = lambda match: f'{color.bryellow}\'{color.bryellow.replace_normal(match.group(1))}{color.bryellow}\'{color.normal}'
  ),
}

def highlighter(part: str) -> str:
  """
  Styles individual parts of strings based on regular expressions.
  """
  part = str(part)
  
  for highlighter in highlighting_rules.values():
    part = highlighter.regexp.sub(
      highlighter.repl,
      part
    )
  
  return part

style_rules = []
def insert_style_rule(*, index: int|None = None, check: callable, repl: callable):
  rule = StyleRule(
    check = check,
    repl = repl
  )
  if index is None:
    style_rules.append(rule)
  else:
    style_rules.insert(index, rule)
    
def append_style_rule(*args, **kwargs):
  """
  Wrapper for :func:insert_style_rules but :param:`index` is always `None`
  """
  
  kwargs = {
    **kwargs,
    'index': None
  }
  
  return insert_style_rule(
    *args,
    **kwargs
  )
    
insert_style_rule(
  check = lambda value: isinstance(value, (int, float)),
  repl  = lambda value: (color.brblue).wrap(value)
)
insert_style_rule(
  check = lambda value: value in (None, True, False),
  repl  = lambda value: color.brmagenta.wrap(value)
)
# insert_style_rule(
#   check = lambda value: isinstance(value, str),
#   repl  = lambda value: f'{color.bryellow}"{color.bryellow.replace_normal(value)}{color.bryellow}"{color.normal}'
# )
# insert_style_rule(
#   check = lambda value: isinstance(value, str),
#   repl  = highlighter
# )
insert_style_rule(
  check = lambda value: isinstance(value, (list, tuple)),
  repl  = lambda value: f'[{', '.join(map(lambda item: style_object(item, highlight_string=False), value))}]'
)

#: Style rule for strings when :func:`style_object` is called with `highlight_string` = `False`
#: Check is not used.
string_style_rule = StyleRule(
  check = lambda value: isinstance(value, str),
  repl  = lambda value: (
    f'{color.bryellow}"'
    + f'{color.bryellow.replace_normal(value)}'
    + f'{color.bryellow}"{color.normal}'
  )
)

def style_object(target, *, highlight_string=True) -> str:
  """
  Styles entire objects passed to :func:`log` based on check functions.
  See `style_rules`
  
  :param highlight_string: Should run target through :func:highlight if it's a string?
                           If not, uses `string_style_rule`
                           Defaults to `True`
  :type  highlight_string: bool
  """
  for rule in style_rules:
    if not rule.check(target):
      continue
    
    return rule.repl(target)
  
  if highlight_string:
    return highlighter(target)
  else:
    return string_style_rule.repl(str(target))