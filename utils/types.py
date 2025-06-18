from typing import NamedTuple, TypedDict

class Move(NamedTuple):
  move_number: int
  white_move: str
  black_move: str

class Game(TypedDict):
  moves: list[Move]
  outcome: str

class Entry(TypedDict):
  annotations: dict[str, str]
  game: Game

ParsedOutput = list[Entry]
