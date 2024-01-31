from abc import ABC, abstractmethod
from .types import Game

class GameFormatter(ABC):
  @abstractmethod
  def format(self, game: Game):
      pass
