def annotations_to_pgn_part(annotations):
  return "\n".join([f"[{key} \"{value}\"]" for key, value in annotations.items()])

# TODO: Add support for comments
# TODO: Allow choosing between " " and "\n" as separators
def game_to_pgn_part(game, clock_times = None):
  if clock_times is None:
    return " ".join([f"{move[0]}. {move[1]} {move[2] or ''}" for move in game['moves']]) + " " + game['outcome']
  
  move_strings = []
  for move in game['moves']:
    (white_clock_time, black_clock_time) = clock_times.get(move[0], (None, None))
    white_clock_comment = f" {format_clock_time(white_clock_time)}"
    black_clock_comment = f" {format_clock_time(black_clock_time)}"
    
    move_strings.append(f"{move[0]}. {move[1]}{white_clock_comment} {move[2] or ''}{black_clock_comment}")
  
  return " ".join(move_strings) + " " + game['outcome']

def entry_to_pgn(entry, clock_times = None):
  # an entry contains annotations and a game
  annotations = annotations_to_pgn_part(entry['annotations'])
  game = game_to_pgn_part(entry['game'], clock_times)
  return annotations + "\n\n" + game + "\n"

# 90 -> { [%clk 1:30:00] }
# 60 -> { [%clk 0:60:00] }
def format_clock_time(clock_time):
  if clock_time is None:
    return ""
  
  hours = int(clock_time / 60)
  minutes = int(clock_time % 60)
  seconds = 0
  clock_str = f"[%clk {hours}:{minutes:02d}:{seconds:02d}]"
  clock_comment = f"{{ {clock_str} }}"
  return clock_comment
  

def to_pgn(parsedoutput, clock_times = None):
  content = ""
  for entry in parsedoutput:
      content += entry_to_pgn(entry, clock_times) + "\n"
  return content
