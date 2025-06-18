# Source: https://medium.com/analytics-vidhya/parsing-pgn-chess-games-with-python-68a2c199665c
from parsita import *

def formatannotations(annotations):
    return {ant[0]: ant[1] for ant in annotations}

def formatgame(game):
    return {
        'moves': game[0],
        'outcome': game[1]
    }

def formatentry(entry):
    return {'annotations': entry[0], 'game': entry[1]}

def handleoptional(optionalmove):
    if len(optionalmove) > 0:
        return optionalmove[0]
    else:
        return None

# Define Grammar by building up from smallest components

# tokens
quote = lit(r'"')
whitespace = reg(r'\s+')
tag = reg(r'[\u0021-\u0021\u0023-\u005A\u005E-\u007E]+')
string = reg(r'[\u0020-\u0021\u0023-\u005A\u005E-\U0010FFFF]+')

# Annotations: [Foo "Super Awesome Information"]
annotation = '[' >> (tag) << ' ' & (quote >> string << quote) << ']'
annotations = repsep(annotation, '\n') > formatannotations

# Moves are more complicated
regularmove = reg(r'[a-h1-8NBRQKx\+#=]+') # Matches more than just chess moves
longcastle = reg(r'O-O-O[+#]?') # match first to avoid castle matching spuriously
castle = reg(r'O-O[+#]?')
nullmove = lit('--') # Illegal move rarely used in annotations

move = regularmove | longcastle | castle | nullmove

# Clock time
clock = reg(r'[0-9][0-9]:[0-9][0-9]:[0-9][0-9]') | reg(r'[0-9][0-9]:[0-9][0-9]') | reg(r'[0-9][0-9]') | reg(r'[0-9]')
extra_info = ' (' >> reg(r'[^)]+') << ')'

clock_situation = '{' >> (clock) << opt(extra_info) << '/}'

# Build up the game
white_movenumber = (reg(r'[0-9]+') << '.') > int
black_movenumber = (reg(r'[0-9]+') << '...')  > int

white_move = white_movenumber & (move << whitespace) & clock_situation << whitespace
black_move = black_movenumber & (move << whitespace) & clock_situation << whitespace

turn = (white_move) & (opt(black_move) > handleoptional)

draw = lit('1/2-1/2')
white = lit('1-0')
black = lit('0-1')
outcome = draw | white | black

game = (rep(turn) & outcome) > formatgame

# A PGN entry is annotations and the game
entry = ((annotations << rep(whitespace)) & (game << rep(whitespace))) > formatentry

# A file is repeated entries
file = rep(entry)

def sanitize_pgn(content: str) -> str:
  # Parsita does not recognize the '}' character, so we have to escape it
  content = content.replace('}', '/}')
  
  # print('>>> Sanitized PGN file contents:')
  # print(content)
  return content

def parse_file_contents(file_contents: str):
  parsedoutput = file.parse(sanitize_pgn(file_contents))
  return parsedoutput.unwrap()

def get_game_count(parsedoutput):
  return len(parsedoutput)

def get_move_count(parsedoutput, game_index = 0):
  return len(parsedoutput[game_index]['game']['moves'])
