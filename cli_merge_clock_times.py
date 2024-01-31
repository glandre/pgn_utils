import sys
from utils.chess_grammar import parse_file_contents
from utils.chess_grammar import get_game_count
from utils.chess_grammar import get_move_count
from utils.minute_clock_times_game_formatter import MinuteClockTimesGameFormatter
from utils.pgn import PGN

def cli_merge_clock_times():
  # Read file path from command line
  if len(sys.argv) < 3:
    print("Please provide a PGN file and a clock_times file.")
    exit(1)

  pgn_file = sys.argv[1]
  clock_times_file = sys.argv[2]

  parsedoutput = None
  clock_times_loader = None

  with open(pgn_file, 'r') as f:
    # Print file contents
    contents = f.read()
    parsedoutput = parse_file_contents(contents)

  # Fail if parsedoutput length is different than 1
  games_count = get_game_count(parsedoutput)
  if games_count != 1:
    print(f"{games_count} games detected. Only one game per file is supported.")
    exit(1)

  move_count = get_move_count(parsedoutput, 0)

  with open(clock_times_file, 'r') as f:
    # Print file contents
    contents = f.read()
    clock_times_loader = MinuteClockTimesGameFormatter(contents, move_count, separator=",")


  # Print the first game
  pgn = PGN(clock_times_loader)
  print(pgn.to_pgn(parsedoutput))

if __name__ == "__main__":
  cli_merge_clock_times()
