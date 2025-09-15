'''
logic.py
Core Minesweeper game logic
Author: Jonathan Johnston
Created: 2025-09-07
Functions:
- place_mines: places mines on the board with first click safety
- compute_neighbor_counts: calculates the number of mines surrounding each cell
- flood_reveal: reveals cells recursively based on the clicked cell
- check_win: check if all safe cells have been revealed (win condition)
- check_loss: check if clicked celll was a mine and return information for displaying loss board
- neighbors / neighbors_inclusive: helper functions for calculating neighbor cell coordinates
'''

# used for typing in functions
from typing import Set, Tuple, Dict, List, Optional
import random

# coordinates are stored as a tuple containing 2 ints
Coord = Tuple[int, int]

'''
returns the list of the cell coordinates surrounding a given cell, including the given cell coordinates
function checks if the cell is on the edge of the board
if so it ajusts the range it must iterate over
it iterates over the adjacent rows and columns and adds those coordinates to the list
'''
def neighbors_inclusive(cell_row: int, cell_col: int) -> List[Coord]:
    neighbor_cells = []
    cols_before = 1
    cols_after = 1
    rows_before = 1
    rows_after = 1
    if cell_row == 0:
        rows_before = 0
    if cell_row == 9:
        rows_after = 0
    if cell_col == 0:
        cols_before = 0
    if cell_col == 9:
        cols_after = 0
    for row in range(cell_row - rows_before, cell_row + rows_after + 1):
        for col in range(cell_col - cols_before, cell_col + cols_after + 1):
            neighbor_cells.append((row,col))
    return neighbor_cells

'''
Returns the list of the cell coordinates surrounding a given cell, excdluing the given cell coordinates
function calls neighbors inclusive then removes the given cell from the list
'''
def neighbors(cell_row: int, cell_col: int) -> List[Coord]:
    neighbor_cells = neighbors_inclusive(cell_row, cell_col)
    neighbor_cells.remove((cell_row,cell_col))
    return neighbor_cells

'''
Returns a set containing the mine coordinates
function calculates mine coordinates by using the random module
the first click coordinate is removed from the possible options for mine coordinates
a seed can be provided to make testing consistent
'''
# seed for testing with the same mine placements each time
def place_mines(mine_count: int, first_coord: Coord, seed: Optional[int] = None, neighbor_safe: bool = True) -> Set[Coord]:
    mines_seed = random.Random(seed)
    mines = set()
    excluded_cells = {first_coord}
    if neighbor_safe:
        for cell in neighbors(first_coord[0], first_coord[1]):
            excluded_cells.add(cell)
    while len(mines) < mine_count:
        row = mines_seed.randint(0,9)
        col = mines_seed.randint(0,9)
        if (row,col) not in mines and (row,col) not in excluded_cells:
            mines.add((row,col))
    return mines

'''
returns a dictionary where keys are cell coordinates and values are the number of mines surrounding the cell
function checks each cell on the board then calculates it neighbors and checks if any of them are mines
total neighboring mines is then summed up and added to the dictionary along with the cell coordinate
'''
def compute_neighbor_counts(mines: Set[Coord]) -> Dict[Coord, int]:
    adjacent_mine_counts = {}
    for row in range(10):
        for col in range(10):
            if (row,col) not in mines:
                adjacent_mine_counts[(row,col)] = 0
    for cell in adjacent_mine_counts.keys():
        neighbor_cells = neighbors(cell[0], cell[1])
        for neighbor in neighbor_cells:
            if neighbor in mines:
                adjacent_mine_counts[cell] += 1
    return adjacent_mine_counts

'''
Returns the set of coordinates for cells to be revealed after a click
function creates a set for storing coordinates if it is the first function call
if the current cell is in the revealed, mines, or flagged sets then return 
if not the cell is added to the revealed cells set
neihboring cells are checked and if they have a mine count > 0 add them to revealed but don't recurse into them
if mine count of neighboring cell is 0 then recurse by calling flood reveal and pass it the new revealed set
'''
def flood_reveal(start: Coord, mines: Set[Coord], counts: Dict[Coord, int], revealed: Set[Coord], flagged: Set[Coord], new_revealed: set[Coord] | None=None) -> Set[Coord]:
    if new_revealed is None:
        new_revealed = set()
    if start in revealed or start in mines or start in flagged:
        return new_revealed
    new_revealed.add(start)
    revealed.add(start)
    if counts[start] == 0:
        neighbor_cells = neighbors(start[0], start[1])
        for neighbor in neighbor_cells:
            if neighbor in counts:
                if neighbor not in revealed and counts[neighbor] != 0:
                    revealed.add(neighbor)
                    new_revealed.add(neighbor)
                if counts[neighbor] == 0:
                    flood_reveal(neighbor, mines, counts, revealed, flagged, new_revealed)
    return new_revealed

'''
returns a boolean value representing whether the player has won or lost
function looks at each cell on the board and checks if it is the mines or revealed sets
if all cells belong to either set then true is returned otherwise false is returned
'''
def check_win(mines: Set[Coord], revealed: Set[Coord]) -> bool:
    for row in range(10):
        for col in range(10):
            if (row,col) not in mines and (row,col) not in revealed:
                return False
    return True


'''
returns a dictionary containing loss info
dictionary is structured like this 
Keys = lost, clicked_bomb, all_mines, correct_flags, wrong_flags
    - lost = bool: True if player hit a mine
    - clicked_bomb = Coord | None: returns coordinate of clicked bomb on loss or none otherwise
    - all_mines = set[Coord]: every mine location
    - correct_flags = set[Coord]: flags that were correctly placed
    - wrong_flags = set[Coord]: flags that were incorrectly placed
on a loss the whole dictionary is relevant however if it isn't a loss values other than lost can be ignored
function checks if the first click has already happened
if so then it checks if the current click is in the mines set
if it is in the mines set return relevant information for updating board otherwise
otherwise return the dictionary containing lost = False and the other information can be ignored
'''
def check_loss(click: Coord, mines: set[Coord], flagged: set[Coord], first_click_done: bool) -> dict:

    if first_click_done and click in mines:
        return {"lost": True, "clicked_bomb": click, "all_mines": mines, "correct_flags": flagged & mines, "wrong_flags": flagged - mines}
    else:
        return {"lost": False, "clicked_bomb": None, "all_mines": mines, "correct_flags": set(), "wrong_flags": set()}
    
'''
print_board function written by chatgpt
used for testing place mines, compute neighbors, and flood reveal
'''
def print_board(rows: int,
                cols: int,
                mines: Set[Coord],
                counts: Dict[Coord, int],
                revealed: Set[Coord],
                flagged: Optional[Set[Coord]] = None,
                show_mines: bool = False) -> None:
    """
    Print a Minesweeper board to stdout.

    Symbols:
      # = covered
      F = flagged
      * = mine (only shown if revealed mine, or show_mines=True)
      . = revealed zero (0 adjacent mines)
      1..8 = revealed number

    Columns labeled A.., rows labeled 1..rows.
    """
    if flagged is None:
        flagged = set()

    # Header: A B C ...
    header = "   " + " ".join(chr(ord('A') + c) for c in range(cols))
    print(header)

    for r in range(rows):
        row_syms = []
        for c in range(cols):
            pos = (r, c)
            if pos in revealed:
                if pos in mines:
                    ch = "*"
                else:
                    n = counts.get(pos, 0)
                    ch = "." if n == 0 else str(n)
            else:
                if pos in flagged:
                    ch = "F"
                elif show_mines and pos in mines:
                    ch = "*"
                else:
                    ch = "#"
            row_syms.append(ch)

        # Row label (1..rows), right-aligned to handle 2-digit rows nicely
        print(f"{r+1:>2} " + " ".join(row_syms))


#tests to ensure functions work properly
def test():
    mines = place_mines(20, (4,4), 7, False)
    print(mines)
    counts = compute_neighbor_counts(mines)
    print(counts)
    revealed = flood_reveal((4,4), mines, counts, set(), set())
    print_board(10, 10, mines, counts, revealed, None, True)

test()