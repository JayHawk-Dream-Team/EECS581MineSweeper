'''
input_handler.py
Handle User Inputs
Author: Cole DuBois
Created: 2025-09-15
Functions:
- handle_events: process pygame events and return action dicts
- screen_to_grid: convert screen coordinates to board grid coordinates
- get_mouse_position: return current mouse position
'''
import pygame

class InputHandler:
	def __init__(self, cell_size: int = 32, board_offset_y: int = 0):
		"""
		Args:
			cell_size: Size of each cell in pixels
			board_offset_y: Vertical offset for the board (for UI space above board)
		"""
		self.cell_size = cell_size
		self.board_offset_y = board_offset_y

	def handle_events(self, events):
		"""
		Process pygame events and return an action dict if a relevant mouse event occurs.
		Returns:
			dict: { 'type': 'reveal'|'flag', 'x': int, 'y': int } or None
		"""
		for event in events:
			if event.type == pygame.MOUSEBUTTONDOWN:
				mouse_x, mouse_y = event.pos
				grid_x, grid_y = self.screen_to_grid(mouse_x, mouse_y)
				if grid_x is not None and grid_y is not None:
					if event.button == 1:
						# Left click: reveal
						return {'type': 'reveal', 'x': grid_x, 'y': grid_y}
					elif event.button == 3:
						# Right click: flag
						return {'type': 'flag', 'x': grid_x, 'y': grid_y}
		return None

	def screen_to_grid(self, x, y):
		"""
		Convert screen (pixel) coordinates to board grid coordinates.
		Returns (grid_x, grid_y) or (None, None) if out of bounds.
		"""
		if y < self.board_offset_y:
			return (None, None)
		grid_x = x // self.cell_size
		grid_y = (y - self.board_offset_y) // self.cell_size
		# Optionally, add bounds checking here if board size is known
		return (grid_x, grid_y)

	def get_mouse_position(self):
		"""Return the current mouse position in screen coordinates."""
		return pygame.mouse.get_pos()
