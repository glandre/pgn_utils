import sys
from utils.chess_grammar import parse_file_contents, get_game_count, get_move_count
from utils.clock_times import load_clock_times
from utils.pgn import to_pgn

def cli_merge_clock_times():
  # Read file path from command line
  if len(sys.argv) < 3:
    print("Please provide a PGN file and a clock_times file.")
    exit(1)

  pgn_file = sys.argv[1]
  clock_times_file = sys.argv[2]

  # Print file path
  # print("Parsing PGN file: " + pgn_file)

  parsedoutput = None
  clock_times = None

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
    clock_times = load_clock_times(contents, move_count, separator=",")


  # Print the first game
  print(to_pgn(parsedoutput, clock_times))
