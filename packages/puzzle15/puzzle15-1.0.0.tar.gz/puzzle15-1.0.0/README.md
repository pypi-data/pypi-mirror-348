# Puzzle15

[![codecov](https://codecov.io/gh/EvalVis/Puzzle15/branch/main/graph/badge.svg)](https://codecov.io/gh/EvalVis/Puzzle15)

A lib for a sliding block puzzle game: https://en.wikipedia.org/wiki/15_puzzle.

Allows making custom width and height puzzles.

Puzzles can be randomly generated or given as input.

## Functionality
- Create N x M puzzle
    - Random puzzle from given width and height.
    - Given puzzle from string. Giving unsolvable puzzle causes error.
- Check possible moves (up, right, down, left) in the current puzzle position.
- Make a move.
- See puzzle representation.
- Check if puzzle is solved.

## Usage

```python
from puzzle15.puzzle import Puzzle

# Create a 4x4 random puzzle
puzzle = Puzzle.from_dimensions(4, 4)
print(puzzle)

# Create a puzzle from a string (use -1 for the blank)
puzzle_another = "1 2 3 4|5 6 7 8|9 10 11 12|13 14 15 -1"
puzzle = Puzzle.from_string(puzzle_another)
print(puzzle)

# Check possible moves
moves = puzzle.possible_moves()
print("Possible moves: ", moves)

# Make a move
if 'up' in puzzle.possible_moves():
    puzzle.move('up')
    print(puzzle)

# See puzzle representation
print(puzzle)
grid = puzzle.grid()
print(grid)

# Check if puzzle is solved
if puzzle.is_solved():
    print("Puzzle is solved!")
else:
    print("Puzzle is not solved.")
```

## Caution
Please only use `str(puzzle)` method when printing.
Otherwise make use of `puzzle.grid()` method.

If you couple to `str(puzzle)` and this method will change by introducing different
formatting or showing the board in a different way, your code will break.