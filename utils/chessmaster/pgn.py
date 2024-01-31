from utils.pgn import PGN
from utils.types import Entry
from .game_formatter import ChessmasterGameFormatter
from .types import GameElapsedTimes, ChessmasterParsedOutput, ChessmasterEntry
from pprint import pprint

class ChessmasterPGN(PGN):
  def __init__(self, game_formatter: ChessmasterGameFormatter) -> None:
    super().__init__(game_formatter)
  
  def load_clock_times(self, chessmaster_entry: ChessmasterEntry) -> None:
    """
    Loads the clock times from the Chessmaster entry into the game formatter.
    """
    elapsed_times: GameElapsedTimes = {}
    for move in chessmaster_entry["game"]["moves"]:
      move_number = move[0]
      white_elapsed_time = move[2]
      black_elapsed_time = move[3][2] if move[3] else None

      elapsed_times[move_number] = (
        self.game_formatter.parse_elapsed_time(white_elapsed_time), 
        self.game_formatter.parse_elapsed_time(black_elapsed_time)
      )
    
    self.game_formatter.set_elapsed_times(elapsed_times)

  
  def convert_entry(self, chessmaster_entry: ChessmasterEntry) -> Entry:
    """
    Converts the parsedoutput from the Chessmaster format to the base parsedoutput format.
    Chessmaster format:
    {
      "annotations": {
        "Event": "Rated Blitz game",
        "Site": "https://lichess.org/6X4j3o3C",
      },
      "game": {
        "moves": [
          [
            1, # move number
            "e4", # white move
            "00:00", # white elapsed time
            [
              1,
              "c5", # black move
              "00:00" # black elapsed time
            ]
          ],
          [
            2,
            "c3",
            "00:12",
            [
              2,
              "d6",
              "00:00"
            ]
          ],
        ],
        "outcome": "0-1", # game outcome
      }
    }

    Base parsedoutput format changes the "moves" key:
    {
      "game": {
        "moves": [
          [
            1, # move number
            "e4", # white move
            "c5" # black move
          ],
          [
            2,
            "c3",
            "d6"
          ]
        ],
      }
    }
    """
    # print('>>> convert_to_base_parsedoutput:')
    # pprint(chessmaster_entry)
    
    base_entry: Entry = {
      "game": {
        "moves": []
      }
    }


    # convert annotations
    base_entry["annotations"] = chessmaster_entry["annotations"]

    # convert game
    base_entry["game"]["outcome"] = chessmaster_entry["game"]["outcome"]
    for move in chessmaster_entry["game"]["moves"]:
      move_number = move[0]
      white_move = move[1]
      black_move = move[3][1] if move[3] else None

      base_entry["game"]["moves"].append([
        move_number,
        white_move,
        black_move
      ])

    return base_entry
  
  def to_pgn(self, parsedoutput: ChessmasterParsedOutput):
    if len(parsedoutput) != 1:
      raise ValueError("Multiple games not supported")
    
    chessmaster_entry = parsedoutput[0]
    self.load_clock_times(chessmaster_entry)
    base_parsedoutput  = self.convert_entry(chessmaster_entry)
    
    # print('>>> to_pgn > base_parsedoutput:')
    # pprint(base_parsedoutput)
    # print('>>> to_pgn > base_parsedoutput:')
    # pprint(base_parsedoutput)

    return super().to_pgn([base_parsedoutput])
  