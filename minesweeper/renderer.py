"""
Author: Blake Ebner, Mahdi Essawi
Last modified: 09/18/2025
"""
import pygame
import os

class Renderer:
    #creating the screen size along with loading the images, scale all images to cell size
    def __init__(self, screen, cell_size: int = 32):
        self.screen = screen
        self.cell_size = cell_size
        self.font = pygame.font.SysFont("arial", 20)
        self.font_small = pygame.font.Font(None, 14)
        self.font_flag_counter = pygame.font.SysFont("arial", 15, bold=True)
        img_path = "images"
        self.images = {
            "covered": pygame.image.load(os.path.join(img_path, "empty-block.png")),
            "flag": pygame.image.load(os.path.join(img_path, "flag.png")),
            "mine_clicked": pygame.image.load(os.path.join(img_path, "bomb-at-clicked-spot.png")),
            "mine": pygame.image.load(os.path.join(img_path, "unclicked-bomb.png")),
            "wrong_flag": pygame.image.load(os.path.join(img_path, "wrong-flag.png")),
        }

        self.numbers = {
            n: pygame.image.load(os.path.join(img_path, f"{n}.png")) for n in range(0, 9)
        }

        for key in self.images:
            self.images[key] = pygame.transform.scale(self.images[key], (cell_size, cell_size))
        for key in self.numbers:
            self.numbers[key] = pygame.transform.scale(self.numbers[key], (cell_size, cell_size))

    def render_board(self, board):
        #making and rendering the game board and reacting to what the player clicked and showing final result
        for row in range(board.height):
            for col in range(board.width):
                cell = board.get_cell(col, row)
                x = col * self.cell_size
                y = row * self.cell_size

                if not getattr(cell, "revealed", False):
                    if getattr(cell, "flagged", False):
                        self.screen.blit(self.images["flag"], (x, y))
                    else:
                        self.screen.blit(self.images["covered"], (x, y))
                else:
                    if getattr(cell, "is_mine", False):
                        if getattr(cell, "clicked", False):
                            self.screen.blit(self.images["mine_clicked"], (x, y))
                        else:
                            self.screen.blit(self.images["mine"], (x, y))
                    else:
                        count = getattr(cell, "count", 0)
                        self.screen.blit(self.numbers[count], (x, y))

                if getattr(cell, "wrong_flag", False):
                    self.screen.blit(self.images["wrong_flag"], (x, y))
        # column labels (A-J)
        for x in range(10):
            label = chr(ord('A') + x)
            label_surface = self.font_small.render(label, True, (0,0,0))
            self.screen.blit(label_surface, (x * self.cell_size + self.cell_size // 2 - 5, 
                                           board.height * self.cell_size + 5))
        # row labels (1-10)
        for y in range(10):
            label = str(y + 1)
            label_surface = self.font_small.render(label, True, (0,0,0))
            self.screen.blit(label_surface, (board.width * self.cell_size + 5, 
                                           y * self.cell_size + self.cell_size // 2 - 5))
        # flag counter
        remaining_flags = board._core.mines_remaining_estimate()
        flag_text = f"Flags: {remaining_flags}"
        flag_color = (255,0,0) if remaining_flags < 0 else (0,100,0)
        flage_surface = self.font_flag_counter.render(flag_text, True, flag_color)
        self.screen.blit(flage_surface, (10, board.height * self.cell_size + 35))

    def render_game_over(self, won: bool):
        #show the outcome of the game 
        msg = "You win" if won else "Game over"
        text = self.font.render(msg, True, (0, 0, 0))
        rect = text.get_rect(center=(self.screen.get_width() // 2, 
                                     self.screen.get_height() - 50))
        self.screen.blit(text, rect)
