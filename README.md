# PGN Utils

## Features

### Add Clock Times

This utility allows us to insert clock times to moves in a PGN game.

Sources:
* Is it possible to add clock time to the moves in a Lichess study? https://lichess.org/forum/lichess-feedback/is-it-possible-to-add-clock-time-to-the-moves-in-a-lichess-study
* Parsing PGN Chess Games With Python
  - https://medium.com/analytics-vidhya/parsing-pgn-chess-games-with-python-68a2c199665c
  - https://github.com/matteson/parse-pgn-files/blob/main/Parse%20PGN%20files.ipynb

* Parsita
  - https://pypi.org/project/parsita/1.1.0/
  - https://github.com/drhagen/parsita
* 

#### Scenario: Record games from the game sheet after a tournament

Steps:

1. Transcribe moves to a Lichess study

2. Export each game as a pgn file (1 game per file)

3. For each game, transcribe clock times to a text file in the following synatx:

```
1,90,90
4,89,
6,,89
```

Missing values are backfilled based on previous lines. The file above is equivalent to the following:

```
1,90,90
2,90,90
3,90,90
4,89,90
5,89,90
6,89,89
```

4. Run this script to obtain the pgn containing move times

```sh
python3 main.py round_1.pgn round_1_clock_times.txt > output.pgn
```

5. Import PGN to Lichess

6. Continue game analysisas usual

#### Limitations

* Currently supports a single game per run
* Does not support games containing variations
* Does not support games containing comments

## Development

### Requirements

```
python3 3.11 or above.
```

### Install dependencies

```
python3 -m pip -r requirements.txt
```

### Run

```
python3 main.py path/to/pgn_file.pgn path/to/clock_times.txt > output.pgn
```

### Install a new depencency

```
python3 -m pip install parsita
python3 -m pip freeze > requirements.txt
```

## Roadmap

- [x] Basic PoC: reads a pgn file containing a single game and a text file containing the clock moves, and outputs a pgn with clock times
- [x] Update `clock_times` to understand this syntax: `1 90 90` if a move is skipped, preserve previous state
- [ ] Add support to multiple games:
  - [x] PGN parser parses multiple games
  - [ ] clock_times.txt format for multiple games
- [ ] Update `chess_grammar` to support PGN file with games that contain comments
- [ ] Update `chess_grammar` to support PGN file with games that contain variantions
- [ ] Convert `clock_times` syntax to also be a grammar based on parsita
- [ ] Add a `validate_clock_times` function to check if the file is malformed before running
