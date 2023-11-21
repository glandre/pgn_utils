from .parse_int import parse_int

def load_clock_times_simple(contents):
  clock_times = {}
  # text file in the following format (line number is equivalent to move number):
  # <white_clock> <black_clock>
  # <white_clock> <black_clock>
  # ...
  move_number = 0
  for line in contents.splitlines():
    line = line.strip()
    if line == "":
      continue
    move_number += 1
    white_clock, black_clock = line.split(" ")

    clock_times[move_number] = (int(white_clock), int(black_clock))
  return clock_times

def load_clock_times(contents, move_count: int = None, separator: str = " "):
  clock_times = {}
  # text file in the following format (line number is equivalent to move number):
  # <move_number> <white_clock> <black_clock>
  # <move_number> <white_clock> <black_clock>
  # ...
  # moves could be missing, in which case the last clock time is used
  last_white_clock = None
  last_black_clock = None
  
  for line in contents.splitlines():
    line = line.strip()
    if line == "":
      continue
    
    move_number, white_clock, black_clock = line.split(separator)

    white_clock = parse_int(white_clock) or last_white_clock
    black_clock = parse_int(black_clock) or last_black_clock
    

    clock_times[int(move_number)] = (white_clock, black_clock)

    last_white_clock = white_clock
    last_black_clock = black_clock
  
  # get max move number
  max_move_number = move_count or max(clock_times.keys())

  # fill in missing clock times
  for move_number in range(1, max_move_number + 1):
    if move_number not in clock_times:
      clock_times[move_number] = clock_times[move_number - 1]
  
  return clock_times
