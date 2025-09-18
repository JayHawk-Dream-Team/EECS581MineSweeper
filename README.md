## Minesweeper (EECS 581 Project 1)

Implementation of The Greatest Game of Minesweeper used as a foundation for adding more advanced features for the lucky team that gets our project for Task 2 of the class

Current version supports variable board size, mine count, and cell size via CLI.

### 1. Quick Start
```bash
git clone https://github.com/JayHawk-Dream-Team/EECS581MineSweeper
cd EECS581MineSweeper/minesweeper
python -m venv .venv
source .venv/bin/activate 
pip install pygame
python main.py
```

### 2. Controls
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
	game_manager.py   # Main Loop (input -> board -> render)
	input_handler.py  # Mouse event → action
	renderer.py       # Draws board + end state message
	images/           # Cell, number, and mine sprites
	main.py           # Entry point
```

### 6. References
Course project for EECS 581. Original requirements: https://people.eecs.ku.edu/~saiedian/581/Proj/proj1
