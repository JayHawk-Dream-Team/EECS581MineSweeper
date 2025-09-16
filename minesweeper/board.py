'''
board.py
Minesweeper board state and game logic wrapper
Author: Yoseph Ephrem
Created: 2025-09-15
Classes:
- GameState: possible states of the current game
- Cell: represents the state of a single cell (mine, revealed, flagged, etc.)
- Board: manages the full grid of cells, mine placement, and game state
Board class key methods:
- reveal_cell: handle left-click, including mine placement, flood fill, win/loss check
- toggle_flag: handle right-click flag toggling
- get_cell / __getitem__: access individual cell(s) for rendering
'''

from __future__ import annotations
from dataclasses import dataclass
from enum import Enum, auto
from typing import List, Tuple, Optional, Iterable, Deque
import random
from collections import deque

Coord = Tuple[int, int] #tuple for the coordinates in the game

class GameState(Enum): #class for the current states of the game
    PLAYING = auto()
    WON = auto()
    LOST = auto()
    MENU = auto()
    PAUSED = auto()

@dataclass
class Cell: #class with according attributes for each cell
    is_mine: bool = False
    revealed: bool = False
    flagged: bool = False
    count: int = 0              # adjacent mines
    exploded: bool = False      # true only for the clicked mine on loss
    wrong_flag: bool = False    # flagged but not a mine (used for loss reveal)

class Board:
    """
    Pure game-logic board for Minesweeper. No Pygame here.
    Exposes a rendering-friendly grid of Cell objects and two public actions:
      - reveal_cell(r, c)
      - toggle_flag(r, c)
    """
    def __init__(self, rows: int, cols: int, mines: int, *, seed: Optional[int] = None, first_click_safe: bool = True):
        if rows <= 0 or cols <= 0:
            raise ValueError("rows and cols must be positive")
        if mines <= 0 or mines >= rows * cols:
            raise ValueError("mines must be between 1 and rows*cols-1")
        self.rows = rows # number of rows
        self.cols = cols # number of columns
        self.total_mines = mines # total mines for this game
        self._rng = random.Random(seed) # dedicated RNG for testing
        self._first_click_safe = first_click_safe  # store whether first click is guaranteed safe
        self._grid: List[List[Cell]] = [[Cell() for _ in range(cols)] for _ in range(rows)] # Create a 2D list of Cell objects, all covered and empty initially
        self._first_click_done = False # flag to delay mine placement until first click
        self.state: GameState = GameState.PLAYING # current state (PLAYING / WON / LOST)
        self._revealed_safe: int = 0 # count of non-mine cells revealed so far
        self._flags: int = 0 # number of flags currently placed

    def reveal_cell(self, r: int, c: int) -> None:
        """
        Left-click process.
        - On first click, mines are placed with (r,c) guaranteed safe.
        - If clicking a mine (after first placement), game becomes LOST and we reveal all.
        - If clicking a zero-count cell, flood-reveal opens its region.
        - Revealing flagged or already revealed cells is a no-op.
        """
        if self.state is not GameState.PLAYING or not self._in_bounds(r, c):
            return # ignore if game ended or out of bounds
        cell = self._grid[r][c]
        if cell.revealed or cell.flagged:
            return # ignore if cell already revealed or flagged

        if not self._first_click_done:
            self._place_mines_safe((r, c)) # place mines away from first click
            self._compute_counts() # compute neighbor mine counts
            self._first_click_done = True

        if self._grid[r][c].is_mine:
            self._handle_loss((r, c)) # clicked a mine -> game lost
            return

        if self._grid[r][c].count == 0:
            self._flood_reveal((r, c)) # reveal region if no adjacent mines
        else:
            self._reveal_single((r, c)) # reveal only this cell

        if self._revealed_safe == self.rows * self.cols - self.total_mines:
            self.state = GameState.WON # all safe cells revealed
            self._reveal_mines_on_win() # show all mines at win (optional visual)


    def toggle_flag(self, r: int, c: int) -> None:
        """
        Right-click behavior. Toggle a flag on an unrevealed cell while PLAYING.
        Does nothing on revealed cells or after game over.
        """
        # handle right-click action: toggle flag on cell (r,c)
        if self.state is not GameState.PLAYING or not self._in_bounds(r, c):
            return # ignore if game ended or out of bounds
        cell = self._grid[r][c]
        if cell.revealed:
            return # cannot flag a revealed cell
        cell.flagged = not cell.flagged # flip flag state
        self._flags += 1 if cell.flagged else -1 # update flag counter

    def get_cells(self) -> List[List[Cell]]:
        return self._grid # returns the full 2D grid of Cell objects

    def flags_used(self) -> int:
        return self._flags # returns how many flags the player has currently placed

    def mines_remaining_estimate(self) -> int:
        return self.total_mines - self._flags # returns total mines - current flags

    def _in_bounds(self, r: int, c: int) -> bool:
        return 0 <= r < self.rows and 0 <= c < self.cols

    def _neighbors(self, r: int, c: int) -> Iterable[Coord]:
        for dr in (-1, 0, 1):
            for dc in (-1, 0, 1):
                if dr == 0 and dc == 0:
                    continue
                rr, cc = r + dr, c + dc
                if 0 <= rr < self.rows and 0 <= cc < self.cols:
                    yield (rr, cc)

    def _place_mines_safe(self, safe: Coord) -> None:
        """
        Place total_mines mines randomly, excluding the safe cell on first click.
        (Optionally could exclude neighbors too; keep simple & deterministic.)
        """
        all_coords = [(r, c) for r in range(self.rows) for c in range(self.cols)]
        all_coords.remove(safe) # never place on the first-clicked cell
        self._rng.shuffle(all_coords) # shuffle with board RNG (seedable)
        for (r, c) in all_coords[: self.total_mines]:
            self._grid[r][c].is_mine = True # mark selected cells as mines

    def _compute_counts(self) -> None:
        for r in range(self.rows):
            for c in range(self.cols):
                if self._grid[r][c].is_mine:
                    self._grid[r][c].count = 0
                else:
                    self._grid[r][c].count = sum(1 for (rr, cc) in self._neighbors(r, c) if self._grid[rr][cc].is_mine)

    def _reveal_single(self, coord: Coord) -> None:
        r, c = coord
        cell = self._grid[r][c]
        if cell.revealed or cell.is_mine:
            return # ignore if already revealed or a mine
        cell.revealed = True # uncover this safe cell
        self._revealed_safe += 1 # track revealed safe cells for win check


    def _flood_reveal(self, start: Coord) -> None:
        """
        Breadth-first flood reveal from a zero-count start cell.
        Reveals zeros and their bordering number cells.
        """
        sr, sc = start
        if self._grid[sr][sc].is_mine or self._grid[sr][sc].flagged:
            return # do nothing if starting on a mine or a flagged cell
        q: Deque[Coord] = deque()
        q.append((sr, sc)) # begin BFS at the clicked zero
        while q:
            r, c = q.popleft()
            cell = self._grid[r][c]
            if cell.revealed or cell.flagged:
                continue # skip already processed or flagged cells
            self._reveal_single((r, c)) # reveal current cell
            if cell.count == 0:
                # enqueue neighbors so zeros expand and edge numbers get revealed
                for rr, cc in self._neighbors(r, c):
                    ncell = self._grid[rr][cc]
                    if not ncell.revealed and not ncell.flagged and not ncell.is_mine:
                        q.append((rr, cc))

    def _handle_loss(self, exploded_at: Coord) -> None:
        er, ec = exploded_at
        self.state = GameState.LOST # mark game as lost
        self._grid[er][ec].exploded = True # mark the clicked mine as exploded
        for r in range(self.rows):
            for c in range(self.cols):
                cell = self._grid[r][c]
                if cell.is_mine:
                    cell.revealed = True # show all mines
                if cell.flagged and not cell.is_mine:
                    cell.wrong_flag = True # mark incorrect flags

    def _reveal_mines_on_win(self) -> None:
        for r in range(self.rows):
            for c in range(self.cols):
                cell = self._grid[r][c]
                if cell.is_mine:
                    cell.revealed = True # show all mines when player wins

    def __getitem__(self, r: int) -> List[Cell]:
        return self._grid[r] # allow board[row][col] access directly
