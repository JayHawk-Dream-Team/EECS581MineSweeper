"""
main entry point for the minesweeper game
and handles initialization and command-line arguments.
"""
import sys
import argparse
from game_manager import GameManager

def get_mine_count():
    """
    get mine count from user input with validation.
    returns:
        int: Valid mine count between 10 and 20
    """
    while True:
        try:
            mine_count = int(input("Enter number of mines (10-20): "))
            if 10 <= mine_count <= 20:
                return mine_count
            else:
                print("Mine count must be between 10 and 20.")
        except ValueError:
            print("Please enter a valid number.")
        except KeyboardInterrupt:
            print("\nGame cancelled.")
            sys.exit(0)

def print_welcome():
    """Print welcome message and instructions."""
    print("=" * 50)
    print("\t    WELCOME TO MINESWEEPER")
    print("=" * 50)
    print()
    print("Game Rules:")
    print("- Left click to reveal a cell")
    print("- Right click to place/remove a flag to mark a susppected mine")
    print("- Numbers show how many mines are adjacent")
    print("- Avoid clicking on mines to Win!")
    print()
    print("Controls:")
    print("- Left Click: Reveal cell")
    print("- Right Click: Toggle flag")
    # if implemented
    #print("- ESC: Quit")
    print()

def parse_arguments():
    """
    parse command-line arguments.
    returns:
        argparse.Namespace: Parsed arguments
    """
    parser = argparse.ArgumentParser(description='Minesweeper Game')
    parser.add_argument('-m', '--mines', type=int, 
                       help='Number of mines (10-20)', 
                       metavar='COUNT')
    parser.add_argument('-s', '--size', type=int, default=32,
                       help='Cell size in pixels (default: 32)',
                       metavar='PIXELS')
    parser.add_argument('--no-intro', action='store_true',
                       help='Skip the welcome screen')
    parser.add_argument('--debug', action='store_true',
                       help='Enable debug mode')
    
    return parser.parse_args()

def validate_mine_count(mine_count):
    """
    validate mine count is within acceptable range.
    args:
        mine_count: Number of mines to validate   
    returns:
        bool: True if valid, False otherwise
    """
    return isinstance(mine_count, int) and 10 <= mine_count <= 20

def main():
    """Main entry point for the minesweeper game."""
    try:
        # parse command-line arguments
        args = parse_arguments()
        
        # show welcome screen unless skipped
        if not args.no_intro:
            print_welcome()
        
        # get mine count
        if args.mines:
            if validate_mine_count(args.mines):
                mine_count = args.mines
                if not args.no_intro:
                    print(f"Using {mine_count} mines from command line.")
            else:
                print(f"Invalid mine count: {args.mines}. Must be between 10-20.")
                mine_count = get_mine_count()
        # this can be removed if we assume no errors occur during the initiation of the game
        else:
            if not args.no_intro:
                mine_count = get_mine_count()
            else:
                mine_count = 15  # default for no-intro mode
        
        if not args.no_intro:
            print(f"\nStarting game with {mine_count} mines...")
            print("Good luck!")
            print()
        
        # create and run the game
        game = GameManager(
            width=10, 
            height=10, 
            num_mines=mine_count,
            cell_size=args.size
        )
        # can be removed too!
        if args.debug:
            print("Debug mode enabled")
            print(f"Board dimensions: {game.get_board_dimensions()}")
            print(f"Mine count: {game.get_mine_count()}")
            print(f"Cell size: {args.size}px")
        
        # run the game
        game.run()
        
    except KeyboardInterrupt:
        print("\n\nGame interrupted by user.")
        sys.exit(0)
    except Exception as e:
        print(f"\nAn error occurred: {e}")
        if args.debug if 'args' in locals() else False:
            import traceback
            traceback.print_exc()
        sys.exit(1)

# USE this function for faster Testing 
def run_quick_game(mine_count=15):
    """
    run a quick game with minimal setup (useful for testing).
    args:
        mine_count: Number of mines (default: 15)
    """
    if not validate_mine_count(mine_count):
        mine_count = 15
    
    game = GameManager(width=10, height=10, num_mines=mine_count)
    game.run()

if __name__ == "__main__":
    main()