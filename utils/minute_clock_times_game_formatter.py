from .parse_int import parse_int
from typing import NamedTuple, Optional
from utils.types import Game, Move
from utils.game_formatter import GameFormatter

class TurnClockTimesInMinutes(NamedTuple):
  white_minutes: int | None
  """The time on the white clock in minutes"""

  black_minutes: int | None
  """The time on the black clock in minutes"""

MoveNumber = int

ClockTimesInMinutes = dict[MoveNumber, TurnClockTimesInMinutes]

def load_clock_times_simple(contents: str) -> ClockTimesInMinutes:
  clock_times: ClockTimesInMinutes = {}
  # text file in the following format (line number is equivalent to move number):
  # <white_minutes> <black_minutes>
  # <white_minutes> <black_minutes>
  # ...
  move_number = 0
  for line in contents.splitlines():
    line = line.strip()
    if line == "":
      continue
    move_number += 1
    white_minutes, black_minutes = line.split(" ")

    clock_times[move_number] = (int(white_minutes), int(black_minutes))
  return clock_times

class MinuteClockTimesGameFormatter(GameFormatter):
  def __init__(self, contents: str, move_count: int, separator = " ") -> None:
    self.contents = contents
    self.move_count = move_count
    self.separator = separator
  
  def set_movecount(self, move_count: int):
    self.move_count = move_count

  def set_separator(self, separator: str):
    self.separator = separator
    

  def load(self) -> ClockTimesInMinutes:
    """
    Loads clock times from a text file.
    The dict returned has the following format:
    {
      <move_number>: (<white_minutes>, <black_minutes>),
      <move_number>: (<white_minutes>, <black_minutes>),
      ...
    }

    e.g.:
    {
      1: (60, 60),
      2: (59, 59),
      ...
    }
    """
    clock_times: ClockTimesInMinutes = {}
    # text file in the following format (line number is equivalent to move number):
    # <move_number> <white_minutes> <black_minutes>
    # <move_number> <white_minutes> <black_minutes>
    # ...
    # moves could be missing, in which case the last clock time is used
    last_white_minutes = None
    last_black_minutes = None
    
    for line in self.contents.splitlines():
      line = line.strip()
      if line == "":
        continue
      
      move_number, white_minutes, black_minutes = line.split(self.separator)

      white_minutes = parse_int(white_minutes) or last_white_minutes
      black_minutes = parse_int(black_minutes) or last_black_minutes
      

      clock_times[int(move_number)] = (white_minutes, black_minutes)

      last_white_minutes = white_minutes
      last_black_minutes = black_minutes
    
    # get max move number
    max_move_number = self.move_count or max(clock_times.keys())

    # fill in missing clock times
    for move_number in range(1, max_move_number + 1):
      if move_number not in clock_times:
        clock_times[move_number] = clock_times[move_number - 1]
    
    return clock_times
  
  # TODO: Add support for comments
  # TODO: Allow choosing between " " and "\n" as separators
  def format(self, game: Game) -> str:
    clock_times = self.load()

    if clock_times is None:
      return (
        " ".join([f"{move[0]}. {move[1]} {move[2] or ''}" for move in game['moves']])
        + " " + game['outcome']
      )
    
    move_strings = []
    for move in game['moves']:
      # (white_clock_time, black_clock_time) = clock_times.get(move[0], (None, None))
      # white_clock_comment = f" {format_clock_time(white_clock_time)}"
      # black_clock_comment = f" {format_clock_time(black_clock_time)}"
      # move_strings.append(f"{move[0]}. {move[1]}{white_clock_comment} {move[2] + ' ' + black_clock_comment if move[2] else ''}")
      turn_clock_times = clock_times.get(move[0], TurnClockTimesInMinutes(None, None))
      move_strings.append(self.format_moves(move, turn_clock_times))
    
    return " ".join(move_strings) + " " + game['outcome']

  def format_moves(self,
                   move: Move, 
                   turn_clock_times: TurnClockTimesInMinutes) -> str:
    
    move_number = move[0]

    white_move = move[1]
    black_move = move[2]

    (white_clock_time, black_clock_time) = turn_clock_times
    
    white_clock_comment = self.format_clock_time(white_clock_time)
    if white_clock_comment:
      white_clock_comment = f" {white_clock_comment}"
    
    black_clock_comment = self.format_clock_time(black_clock_time)
    if black_clock_comment:
      black_clock_comment = f" {black_clock_comment}"
    
    white_fragment = f"{move_number}. {white_move}{white_clock_comment}"
    black_fragment = f"{black_move}{black_clock_comment}" if black_move else ""

    if white_clock_time and black_fragment:
      black_fragment = f"{move_number}...{black_fragment}"

    return f"{white_fragment} {black_fragment}".strip()
  


  # 90 -> { [%clk 1:30:00] }
  # 60 -> { [%clk 0:60:00] }
  def format_clock_time(self, clock_time: Optional[int]):
    if clock_time is None:
      return ""
    
    hours = int(clock_time / 60)
    minutes = int(clock_time % 60)
    seconds = 0
    clock_str = f"[%clk {hours}:{minutes:02d}:{seconds:02d}]"
    clock_comment = f"{{ {clock_str} }}"
    return clock_comment
