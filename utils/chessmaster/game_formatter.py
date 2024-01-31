from typing import Optional
from utils.game_formatter import GameFormatter
from .types import ElapsedTime, GameElapsedTimes, TurnElapsedTimes
from pprint import pprint

# a dict denoting the possible time control formats
# the value is a tuple of the form (initial_time, increment)
# where initial_time and increment are in minutes
supported_time_controls = {
  "90+30": (90, 30), # 90 minutes + 30 seconds increment
  "90": (90, 0), # 90 minutes
  "60": (60, 0), # 60 minutes
}

class ChessmasterGameFormatter(GameFormatter):
  def __init__(self, time_control: str):
    self.elapsed_times: dict[int, ElapsedTime] = None

    if time_control not in supported_time_controls:
      raise ValueError(f"Unsupported time control: {time_control}")
    
    self.time_control = time_control
  
  def format(self, game):
    print('>>> ChessmasterGameFormatter > format > game:')
    pprint(game)
    
    if self.elapsed_times is None:
      return (
        " ".join([f"{move[0]}. {move[1]} {move[2] or ''}" for move in game['moves']])
        + " " + game['outcome']
      )
    
    move_strings = []
    for move in game['moves']:
      turn_elapsed_times: Optional[TurnElapsedTimes] = self.elapsed_times.get(move[0], None)
      #TODO: format moves
    
    return " ".join(move_strings) + " " + game['outcome']
  
  def parse_elapsed_time(self, elapsed_time_str: str) -> ElapsedTime:
    """
    Converts elapsed time from string into a tuple (hours, minutes, seconds):
    Formats:
     - "mm:ss": e.g. "30:05" -> (0, 30, 5)
     - "hh:mm:ss": e.g. "01:30:05" -> (1, 30, 5)
    """
    if elapsed_time_str is None:
      return None

    parts = elapsed_time_str.split(":")
    if len(parts) == 2:
      return (0, int(parts[0]), int(parts[1]))
    elif len(parts) == 3:
      return (int(parts[0]), int(parts[1]), int(parts[2]))
    else:
      raise ValueError(f"Invalid elapsed time format: {elapsed_time_str}")
  
  def set_elapsed_times(self, elapsed_times: GameElapsedTimes):
    self.elapsed_times = elapsed_times

  def to_clock_time(self, elapsed_time: ElapsedTime) -> str:
    """
    Calculate the move's clock time in the format used by PGN: "hh:mm:ss"
    To do so, it takes the time control and subtracts the elapsed time.
    """
    initial_time, increment = supported_time_controls[self.time_control]
    hours, minutes, seconds = elapsed_time
    total_seconds = hours * 3600 + minutes * 60 + seconds
    remaining_time = initial_time * 60 - total_seconds
    return f"{remaining_time // 3600:02}:{remaining_time % 3600 // 60:02}:{remaining_time % 60:02}"
  