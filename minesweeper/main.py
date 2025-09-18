'''
main.py
Main Entry Point for Game that invokes Game_Manager.py
Author: Carlos Mbnedera
Last modified: 2025-09-17
'''

import argparse
import os
from game_manager import GameManager

def parse_args():
    p = argparse.ArgumentParser(description="Minesweeper MVP")
    p.add_argument("--width", type=int, default=10)
    p.add_argument("--height", type=int, default=10)
    p.add_argument("--mines", type=int, default=15)
    p.add_argument("--cell-size", type=int, default=32, dest="cell_size")
    return p.parse_args()

def main():
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    args = parse_args()
    game = GameManager(width=args.width, height=args.height, num_mines=args.mines, cell_size=args.cell_size)
    game.run()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nInterrupted.")