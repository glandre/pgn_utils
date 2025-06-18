import sys
import json
from utils.chess_grammar import parse_file_contents
# from utils.chessmaster.grammar import parse_file_contents

def cli_print_parsed_output():
  # Read file path from command line
  if len(sys.argv) < 2:
    print("Please provide a PGN file.")
    exit(1)

  pgn_file = sys.argv[1]

  parsedoutput = None

  with open(pgn_file, 'r') as f:
    # Print file contents
    contents = f.read()
    parsedoutput = parse_file_contents(contents)

  print(json.dumps(parsedoutput, indent=2))

if __name__ == "__main__":
  cli_print_parsed_output()
