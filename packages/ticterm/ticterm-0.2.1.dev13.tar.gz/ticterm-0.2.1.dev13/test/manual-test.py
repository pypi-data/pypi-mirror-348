import subprocess
import time
import sys
import os

def main():
  sys.path.append(
    os.path.realpath("../")
  )
  import ticterm
  from ticterm import log
  
  log.config.DEFAULT_VERBOSITY = log.Level.DEBUG
  log.config.update(
    verbosity=0
  )
  
  ticterm_version = subprocess.check_output(
    ['hatch', 'version'],
    cwd = '../'
  ).strip().decode()
  
  log.info(f'ticterm version {ticterm_version}')
    
  print()
  for level in log.levels:
    log.log(
      f"This is a level {level} ({log.levels[level].name}) message",
      level=level
    )
    
  list_test = (
    "This is a list with at least 2 elements:", 
    [10, 20, 30, "hello world", "0xfffff"]
  )

  print()
  log.log(*list_test)
  log.info(*list_test)
  
  log.info('Dict:', {'x': 32, 'y': '64', '10': 'a'})
  
  print()
  # log.log('Only numbers at the beginning or end, or surrounded by whitespace should be highlighted')
  log.log('Numbers in the middle of of words shouldn\'t be highlighted.')
  log.log('123 Hello W047d cool okay. 0b1101 0x456 789')
  
  print()
  log.config.reset(start_time=None)
  log.config.update(stack_mode=log.StackMode.ON)
  log.config.update(project_root=False)
  log.info('This is with project_root=False')
  
  log.config.update(project_root=os.environ.get('HOME'))
  log.info('This is with project_root=$HOME')
  
  log.config.update(project_root=True)
  log.info('This is with project_root=True (auto)')
  
  print()
  log.config.reset(start_time=None)
  log.config.update(timestamp_mode=log.TimestampMode.OFF)
  log.log('timestamp_mode=OFF')
  
  log.config.update(timestamp_mode=log.TimestampMode.SINCE_START)
  log.log('timestamp_mode=SINCE_START')
  
  log.config.update(timestamp_mode=log.TimestampMode.EPOCH)
  log.log('timestamp_mode=EPOCH')
  
  print()
  log.config.reset(start_time=None)
  log.config.update(stack_mode=log.StackMode.ONLY_BAD)
  log.log('stack_mode=ONLY_BAD')
  log.warn('stack_mode=ONLY_BAD')
  log.config.update(stack_mode=log.StackMode.ON, stack_limit=2)
  log.info('stack_mode=ON, stack_limit=2')
  
  print()
  log.config.reset(start_time=None)
  log.config.update(stack_mode=log.StackMode.ON)
  log.log('stack ascend=1', stack_ascend=1)
  log.log('stack ascend=2', stack_ascend=2)
  
  print()
  log.config.reset(start_time=None),
  log.config.update(tags=['testing', 'tags'])
  log.log('This should have tags prepended to it.')
  
  print()
  log.config.reset(start_time=None)
  log.info('=============== empty_message_mode tests ===============')
  log.config.update(empty_message_mode=log.EmptyMessageMode.NEWLINE_ONLY)
  log.info('empty_message_mode=EmptyMessageMode.NEWLINE_ONLY:')
  log.log()
  log.config.update(empty_message_mode=log.EmptyMessageMode.NORMAL)
  log.info('empty_message_mode=EmptyMessageMode.NORMAL:')
  log.log()
  log.info('============ empty_message_mode tests done! ============')
  
  print()
  log.config.reset(start_time=None)
  # log.config.update(progress_width=1)
  log.info('Progress test:')
  duration   = 1
  steps      = 30
  major_step = steps // 4
  with log.set_progress(0, steps) as p:
    for i in range(0, steps + 1):
      if i != 0 and i % major_step == 0:
        log.log(f'Woah! We\'re at {i}')
      
      p(i)
      log.set_progress(i)
      
      time.sleep(duration/steps)
  
  time.sleep(0.5)
  log.log('All done!')
  log.config.reset(start_time=None)
  
if __name__ == '__main__':
  main()
