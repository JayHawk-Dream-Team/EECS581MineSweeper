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

def get_mine_count(mines):
        """
        get mine count from user input with validation.
        valid mine count between 10 and 20
        """
        while True:
            try:
                mine_count = input("Enter number of mines (10-20): ")
                if not mine_count:
                    return mines
                
                mine_count = int(mine_count)
                
                if 10 <= mine_count <= 20:
                    return mine_count
                else:
                    print("Mine count must be between 10 and 20")
            except ValueError:
                print("Please enter a valid number")

def main():
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    args = parse_args()
    mine_count = get_mine_count(args.mines)
    game = GameManager(width=args.width, height=args.height, num_mines=mine_count, cell_size=args.cell_size)
    game.run()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nInterrupted.")