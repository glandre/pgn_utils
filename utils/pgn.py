from utils.types import Entry, ParsedOutput
from utils.game_formatter import GameFormatter
from pprint import pprint

class PGN:
  def __init__(self, game_formatter: GameFormatter) -> None:
    self.game_formatter = game_formatter

  def entry_to_pgn(self, entry: Entry) -> str:
    # print(">>> entry_to_pgn > entry:")
    # pprint(entry)
    # an entry contains annotations and a game
    annotations = self.annotations_to_pgn_part(entry['annotations'])
    game = self.game_formatter.format(entry['game'])
    return annotations + "\n\n" + game + "\n"

  def annotations_to_pgn_part(self, annotations):
    return "\n".join([f"[{key} \"{value}\"]" for key, value in annotations.items()])
    

  def to_pgn(self, parsedoutput: ParsedOutput) -> str:
    content = ""
    for entry in parsedoutput:
        content += self.entry_to_pgn(entry) + "\n"
    return content
