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

#### Testing Data

##### Scenario 1

- Single game
- No comments
- No variations
- Clock times with no dups

**Input:**

- `data/scenario1/input.pgn`
```
[Event "Lynn Stringer Memorial"]
[Site "Victoria"]
[Date "2023.08.19"]
[White "Piasetski, Leon"]
[Black "Landre, Geraldo Barbosa"]
[Result "1-0"]
[UTCDate "2023.08.24"]
[UTCTime "04:58:15"]
[Variant "Standard"]
[ECO "D37"]
[Opening "Queen's Gambit Declined: Three Knights Variation"]

1. Nf3 e6 2. c4 d5 3. d4 Nf6 4. Nc3 Be7 5. cxd5 exd5 6. Qc2 c6 7. Bf4 g6 8. e3 Bf5 9. Bd3 Bxd3 10. Qxd3 Nbd7 11. O-O O-O 12. h3 Re8 13. Ne5 Nxe5 14. Bxe5 Bd6 15. f4 Nh5 16. g4 Ng7 17. e4 Bb4 18. Bxg7 dxe4 19. Nxe4 Kxg7 20. g5 Qe7 21. Nf6 Qe3+ 22. Qxe3 Rxe3 23. Kg2 Rd8 24. Rad1 Re2+ 25. Rf2 Rxf2+ 26. Kxf2 Be7 27. Ne4 Rd5 28. Ke3 Rb5 29. b3 Rf5 30. Rc1 h6 31. h4 hxg5 32. hxg5 f6 33. gxf6+ Bxf6 34. Nd6 Bxd4+ 35. Ke4 Rc5 36. Rd1 Bc3 37. Nxb7 Rb5 38. Nd8 Ra5 39. a4 c5 40. Nb7 Ra6 41. Nxc5 Rb6 42. Rd7+ Kf6 43. Rxa7 Rb4+ 44. Kf3 Bd4 45. Ne4+ Ke6 46. Ra6+ Ke7 47. Rxg6 Rxb3+ 48. Kg4 Rb4 49. Ra6 Be3 50. Kf5 Bb6 51. Nc3 1-0
```

- `data/scenario1/input.clk`
```
1,60,60
3,59,
4,53,
5,,56
6,,55
7,,53
8,,54
10,,52
11,52,
12,49,49
13,48,46
15,,44
17,,43
18,41,42
20,37,37
23,,35
24,,34
25,,33
26,38,29
27,36,27
28,34,22
29,32,21
30,28,20
31,29,
33,28,
34,27,18
35,,19
36,25,9
38,21,
39,,4
42,,3
44,19,
46,,1
48,20,

```

**Processing:**

Run `cli_merge_clock_times.py`:

```
python3 cli_merge_clock_times.py data/scenario1/input.pgn data/scenario1/input.clk > data/scenario1/output.pgn
```

**Expected Output**

- `data/scenario1/output.pgn`
```
[Event "Lynn Stringer Memorial"]
[Site "Victoria"]
[Date "2023.08.19"]
[White "Piasetski, Leon"]
[Black "Landre, Geraldo Barbosa"]
[Result "1-0"]
[UTCDate "2023.08.24"]
[UTCTime "04:58:15"]
[Variant "Standard"]
[ECO "D37"]
[Opening "Queen's Gambit Declined: Three Knights Variation"]

1. Nf3 { [%clk 1:00:00] } e6  { [%clk 1:00:00] } 2. c4 { [%clk 1:00:00] } d5  { [%clk 1:00:00] } 3. d4 { [%clk 0:59:00] } Nf6  { [%clk 1:00:00] } 4. Nc3 { [%clk 0:53:00] } Be7  { [%clk 1:00:00] } 5. cxd5 { [%clk 0:53:00] } exd5  { [%clk 0:56:00] } 6. Qc2 { [%clk 0:53:00] } c6  { [%clk 0:55:00] } 7. Bf4 { [%clk 0:53:00] } g6  { [%clk 0:53:00] } 8. e3 { [%clk 0:53:00] } Bf5  { [%clk 0:54:00] } 9. Bd3 { [%clk 0:53:00] } Bxd3  { [%clk 0:54:00] } 10. Qxd3 { [%clk 0:53:00] } Nbd7  { [%clk 0:52:00] } 11. O-O { [%clk 0:52:00] } O-O  { [%clk 0:52:00] } 12. h3 { [%clk 0:49:00] } Re8  { [%clk 0:49:00] } 13. Ne5 { [%clk 0:48:00] } Nxe5  { [%clk 0:46:00] } 14. Bxe5 { [%clk 0:48:00] } Bd6  { [%clk 0:46:00] } 15. f4 { [%clk 0:48:00] } Nh5  { [%clk 0:44:00] } 16. g4 { [%clk 0:48:00] } Ng7  { [%clk 0:44:00] } 17. e4 { [%clk 0:48:00] } Bb4  { [%clk 0:43:00] } 18. Bxg7 { [%clk 0:41:00] } dxe4  { [%clk 0:42:00] } 19. Nxe4 { [%clk 0:41:00] } Kxg7  { [%clk 0:42:00] } 20. g5 { [%clk 0:37:00] } Qe7  { [%clk 0:37:00] } 21. Nf6 { [%clk 0:37:00] } Qe3+  { [%clk 0:37:00] } 22. Qxe3 { [%clk 0:37:00] } Rxe3  { [%clk 0:37:00] } 23. Kg2 { [%clk 0:37:00] } Rd8  { [%clk 0:35:00] } 24. Rad1 { [%clk 0:37:00] } Re2+  { [%clk 0:34:00] } 25. Rf2 { [%clk 0:37:00] } Rxf2+  { [%clk 0:33:00] } 26. Kxf2 { [%clk 0:38:00] } Be7  { [%clk 0:29:00] } 27. Ne4 { [%clk 0:36:00] } Rd5  { [%clk 0:27:00] } 28. Ke3 { [%clk 0:34:00] } Rb5  { [%clk 0:22:00] } 29. b3 { [%clk 0:32:00] } Rf5  { [%clk 0:21:00] } 30. Rc1 { [%clk 0:28:00] } h6  { [%clk 0:20:00] } 31. h4 { [%clk 0:29:00] } hxg5  { [%clk 0:20:00] } 32. hxg5 { [%clk 0:29:00] } f6  { [%clk 0:20:00] } 33. gxf6+ { [%clk 0:28:00] } Bxf6  { [%clk 0:20:00] } 34. Nd6 { [%clk 0:27:00] } Bxd4+  { [%clk 0:18:00] } 35. Ke4 { [%clk 0:27:00] } Rc5  { [%clk 0:19:00] } 36. Rd1 { [%clk 0:25:00] } Bc3  { [%clk 0:09:00] } 37. Nxb7 { [%clk 0:25:00] } Rb5  { [%clk 0:09:00] } 38. Nd8 { [%clk 0:21:00] } Ra5  { [%clk 0:09:00] } 39. a4 { [%clk 0:21:00] } c5  { [%clk 0:04:00] } 40. Nb7 { [%clk 0:21:00] } Ra6  { [%clk 0:04:00] } 41. Nxc5 { [%clk 0:21:00] } Rb6  { [%clk 0:04:00] } 42. Rd7+ { [%clk 0:21:00] } Kf6  { [%clk 0:03:00] } 43. Rxa7 { [%clk 0:21:00] } Rb4+  { [%clk 0:03:00] } 44. Kf3 { [%clk 0:19:00] } Bd4  { [%clk 0:03:00] } 45. Ne4+ { [%clk 0:19:00] } Ke6  { [%clk 0:03:00] } 46. Ra6+ { [%clk 0:19:00] } Ke7  { [%clk 0:01:00] } 47. Rxg6 { [%clk 0:19:00] } Rxb3+  { [%clk 0:01:00] } 48. Kg4 { [%clk 0:20:00] } Rb4  { [%clk 0:01:00] } 49. Ra6 { [%clk 0:20:00] } Be3  { [%clk 0:01:00] } 50. Kf5 { [%clk 0:20:00] } Bb6  { [%clk 0:01:00] } 51. Nc3 { [%clk 0:20:00] }  1-0
```

## Development

### Requirements

```
python3 3.11 or above.
```

### Install dependencies

```
python3 -m pip install parsita
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
