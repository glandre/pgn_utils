from typing import NamedTuple, TypedDict

class ElapsedTime(NamedTuple):
  hours: int
  minutes: int
  seconds: int

class TurnElapsedTimes(NamedTuple):
  white_elapsed_time: ElapsedTime
  black_elapsed_time: ElapsedTime

GameElapsedTimes = dict[int, TurnElapsedTimes]

class ChessmasterBlackFragment(NamedTuple):
  move_number: int
  black_move: str
  black_elapsed_time: str

class ChessmasterMove(NamedTuple):
  move_number: int
  white_move: str
  white_elapsed_time: str
  black_fragment: ChessmasterBlackFragment

class ChessmasterGame(TypedDict):
  moves: list[ChessmasterMove]
  outcome: str

class ChessmasterEntry(TypedDict):
  annotations: dict[str, str]
  game: ChessmasterGame

ChessmasterParsedOutput = list[ChessmasterEntry]
