"""
Game Manager Module for Minesweeper Game

This module contains the GameManager class which serves as the central controller
for the minesweeper game, coordinating between the board, input handler, and renderer.
"""

import pygame
import sys
from typing import Optional

# Import other modules (these will be implemented by other team members)
try:
    from .board import Board
except ImportError:
    # Stub for Board class if not yet implemented
    class Board:
        def __init__(self, width: int, height: int, num_mines: int):
            self.width = width
            self.height = height
            self.num_mines = num_mines
            self.game_over = False
            self.game_won = False
        
        def get_cell(self, x: int, y: int):
            pass
        
        def reveal_cell(self, x: int, y: int):
            pass
        
        def toggle_flag(self, x: int, y: int):
            pass
        
        def is_game_over(self) -> bool:
            return self.game_over
        
        def is_game_won(self) -> bool:
            return self.game_won

try:
    from .input_handler import InputHandler
except ImportError:
    # Stub for InputHandler class if not yet implemented
    class InputHandler:
        def __init__(self):
            pass
        
        def handle_events(self, events):
            return None
        
        def get_mouse_position(self):
            return pygame.mouse.get_pos()

try:
    from .renderer import Renderer
except ImportError:
    # Stub for Renderer class if not yet implemented
    class Renderer:
        def __init__(self, screen, cell_size: int = 32):
            self.screen = screen
            self.cell_size = cell_size
        
        def render_board(self, board):
            pass
        
        def render_game_over(self, won: bool):
            pass


class GameState:
    """Enumeration of game states"""
    PLAYING = "PLAYING"
    WIN = "WIN"
    LOSS = "LOSS"
    MENU = "MENU"
    PAUSED = "PAUSED"


class GameManager:
    """
    Central controller for the Minesweeper game.
    
    This class manages the game loop, coordinates between different components
    (Board, InputHandler, Renderer), and handles game state transitions.
    """
    
    def __init__(self, width: int = 16, height: int = 16, num_mines: int = 40, 
                 cell_size: int = 32):
        """
        Initialize the GameManager.
        
        Args:
            width: Number of cells horizontally
            height: Number of cells vertically
            num_mines: Number of mines on the board
            cell_size: Size of each cell in pixels
        """
        # Game configuration
        self.board_width = width
        self.board_height = height
        self.num_mines = num_mines
        self.cell_size = cell_size
        
        # Calculate screen dimensions
        self.screen_width = width * cell_size
        self.screen_height = height * cell_size + 100  # Extra space for UI
        
        # Initialize pygame
        pygame.init()
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Minesweeper")
        self.clock = pygame.time.Clock()
        
        # Game state
        self.state = GameState.PLAYING
        self.running = True
        
        # Initialize game components
        self._initialize_components()
        
        # Game timing
        self.start_time = pygame.time.get_ticks()
        self.game_time = 0
        
    def _initialize_components(self):
        """Initialize the game components (Board, InputHandler, Renderer)."""
        try:
            self.board = Board(self.board_width, self.board_height, self.num_mines)
            self.input_handler = InputHandler()
            self.renderer = Renderer(self.screen, self.cell_size)
        except Exception as e:
            print(f"Warning: Error initializing components: {e}")
            # Use stub classes if components are not yet implemented
            self.board = Board(self.board_width, self.board_height, self.num_mines)
            self.input_handler = InputHandler()
            self.renderer = Renderer(self.screen, self.cell_size)
    
    def start_new_game(self):
        """Start a new game by resetting all components."""
        self.state = GameState.PLAYING
        self.board = Board(self.board_width, self.board_height, self.num_mines)
        self.start_time = pygame.time.get_ticks()
        self.game_time = 0
    
    def update_game_state(self):
        """Update the current game state based on board conditions."""
        if self.state == GameState.PLAYING:
            if self.board.is_game_over():
                self.state = GameState.LOSS
            elif self.board.is_game_won():
                self.state = GameState.WIN
    
    def handle_input(self):
        """Handle all input events through the InputHandler."""
        events = pygame.event.get()
        
        for event in events:
            if event.type == pygame.QUIT:
                self.running = False
                return
            
            # Handle restart key (R)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    self.start_new_game()
                elif event.key == pygame.K_ESCAPE:
                    self.running = False
        
        # Delegate input handling to InputHandler
        action = self.input_handler.handle_events(events)
        
        # Process the action if we're in playing state
        if self.state == GameState.PLAYING and action:
            self._process_game_action(action)
    
    def _process_game_action(self, action):
        """
        Process game actions from input handler.
        
        Args:
            action: Dictionary containing action type and parameters
        """
        if not action:
            return
        
        action_type = action.get('type')
        x = action.get('x', 0)
        y = action.get('y', 0)
        
        if action_type == 'reveal':
            self.board.reveal_cell(x, y)
        elif action_type == 'flag':
            self.board.toggle_flag(x, y)
    
    def update(self):
        """Update game logic."""
        if self.state == GameState.PLAYING:
            # Update game timer
            current_time = pygame.time.get_ticks()
            self.game_time = (current_time - self.start_time) // 1000
        
        # Update game state based on board conditions
        self.update_game_state()
    
    def render(self):
        """Render the game using the Renderer."""
        # Clear screen
        self.screen.fill((192, 192, 192))  # Light gray background
        
        # Render board
        self.renderer.render_board(self.board)
        
        # Render UI elements based on game state
        if self.state == GameState.WIN:
            self.renderer.render_game_over(won=True)
        elif self.state == GameState.LOSS:
            self.renderer.render_game_over(won=False)
        
        # Update display
        pygame.display.flip()
    
    def run(self):
        """
        Main game loop.
        
        This method contains the core game loop that handles input,
        updates game state, and renders the game.
        """
        print("Starting Minesweeper Game...")
        print("Controls:")
        print("  Left click: Reveal cell")
        print("  Right click: Toggle flag")
        print("  R: Restart game")
        print("  ESC: Quit game")
        
        while self.running:
            # Handle input
            self.handle_input()
            
            # Update game logic
            self.update()
            
            # Render everything
            self.render()
            
            # Control frame rate
            self.clock.tick(60)  # 60 FPS
        
        # Cleanup
        self.quit()
    
    def quit(self):
        """Clean up and quit the game."""
        print("Shutting down Minesweeper...")
        pygame.quit()
        sys.exit()
    
    def get_state(self) -> str:
        """Get the current game state."""
        return self.state
    
    def get_game_time(self) -> int:
        """Get the current game time in seconds."""
        return self.game_time
    
    def pause_game(self):
        """Pause the game (if currently playing)."""
        if self.state == GameState.PLAYING:
            self.state = GameState.PAUSED
    
    def resume_game(self):
        """Resume the game (if currently paused)."""
        if self.state == GameState.PAUSED:
            self.state = GameState.PLAYING
    
    def is_game_active(self) -> bool:
        """Check if the game is currently active (playing or paused)."""
        return self.state in [GameState.PLAYING, GameState.PAUSED]
    
    def get_board_dimensions(self) -> tuple:
        """Get the board dimensions as (width, height)."""
        return self.board_width, self.board_height
    
    def get_mine_count(self) -> int:
        """Get the number of mines on the board."""
        return self.num_mines


# Example usage and testing
if __name__ == "__main__":
    # Create and run a game instance for testing
    game = GameManager(width=10, height=10, num_mines=15)
    game.run()
