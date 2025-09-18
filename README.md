## Minesweeper (EECS 581 Project 1)

Minimal playable Minesweeper implementation used as a foundation for adding more advanced features (IPC, enhanced input handling, etc.). Current version supports variable board size, mine count, and cell size via CLI.

### 1. Quick Start
```bash
git clone <repo-url>
cd EECS581MineSweeper/minesweeper
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install --upgrade pip
pip install pygame
python main.py --width 10 --height 10 --mines 15 --cell-size 32
```

### 2. Game Rules (Brief)
- Board hides a set number of mines.
- Left click: reveal a cell.
	- Number = count of adjacent mines (0–8).
	- 0 auto-expands contiguous empty region.
- Right click: toggle a flag (mark suspected mine).
- Win: all non-mine cells are revealed.
- Lose: you reveal a mine.

### 3. Controls
- Left Mouse Button: Reveal
- Right Mouse Button: Flag / Unflag
- R: Restart
- ESC / Window Close: Quit

### 4. Command-Line Options
```bash
python main.py --width 12 --height 12 --mines 25 --cell-size 28
```
- `--width` / `--height`: board dimensions (cells)
- `--mines`: total mines (ensure < width*height)
- `--cell-size`: pixel size of each cell

### 5. Project Structure (Relevant Parts)
```
minesweeper/
	board.py          # Core game logic & cell state
	game_manager.py   # Minimal loop (input -> board -> render)
	input_handler.py  # Mouse event → action
	renderer.py       # Draws board + end state message
	images/           # Cell, number, and mine sprites
	main.py           # Entry point
```

### 6. Development Notes
- Keep PRs small; only modify core loop files (`game_manager.py`, `main.py`) if integrating new systems.
- Consider adding `__init__.py` later to run as a package: `python -m minesweeper.main`.
- Use a virtual environment to avoid global dependency pollution.

### 7. License / Attribution
Course project for EECS 581. Original requirements: https://people.eecs.ku.edu/~saiedian/581/Proj/proj1

Feel free to extend—HUD (timer, flags remaining), difficulty presets, and test harnesses are natural next steps.
