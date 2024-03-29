# -------
# Modules
# -------
from pygame.constants import K_r
import numpy as np
import pygame
import math
import sys

BOARD_ROWS = 3
BOARD_COLS = 3

BOARD_SIZE = 200
CIRCLE_RADIUS = 60
OFFSET = 55
CIRCLE_LINE_WIDTH = 15
X_LINE_WIDTH = 50

BOARD_WIDTH = BOARD_COLS * BOARD_SIZE
BOARD_HEIGHT = BOARD_ROWS * BOARD_SIZE

LINE_COLOR = (23, 145, 135)
BG_COLOR = (28, 170, 156)
CIRCLE_COLOR = (0, 255, 0)
X_COLOR = (250, 66, 66)


# ---------
# Functions
# ---------
def print_board():
	flipped_board = np.flip(board, 0)
	print(flipped_board)
	print("")


def draw_board():
	draw_lines()
	draw_figures()


def draw_lines():
	pygame.draw.line(screen, LINE_COLOR, (0, 200), (600, 200), 10)
	pygame.draw.line(screen, LINE_COLOR, (0, 400), (600, 400), 10)
	pygame.draw.line(screen, LINE_COLOR, (200, 0), (200, 600), 10)
	pygame.draw.line(screen, LINE_COLOR, (400, 0), (400, 600), 10)
    

def draw_figures():
	for col in range(BOARD_COLS):
		for row in range(BOARD_ROWS):
			if board[row][col] == 1:
				pygame.draw.circle(screen, CIRCLE_COLOR, (int(col * BOARD_SIZE + BOARD_SIZE / 2),
				                   int(row * BOARD_SIZE + BOARD_SIZE / 2)), CIRCLE_RADIUS, CIRCLE_LINE_WIDTH)
			elif board[row][col] == 2:
				pygame.draw.line(screen, X_COLOR, (col * BOARD_SIZE + OFFSET, row * BOARD_SIZE + OFFSET),
				                 (col * BOARD_SIZE + BOARD_SIZE - OFFSET, row * BOARD_SIZE + BOARD_SIZE - OFFSET), X_LINE_WIDTH)
				pygame.draw.line(screen, X_COLOR, (col * BOARD_SIZE + OFFSET, row * BOARD_SIZE + BOARD_SIZE - OFFSET),
				                 (col * BOARD_SIZE + BOARD_SIZE - OFFSET, row * BOARD_SIZE + OFFSET), X_LINE_WIDTH)


def full_board():
	for col in range(BOARD_COLS):
		for row in range(BOARD_ROWS):
			if board[row][col] == 0:
				return False

	return True


def available_square(row, col):
	is_available = board[row][col] == 0
	return is_available


def mark_square(row, col, player):
	board[row][col] = player


def check_win(player):
	ver_win = check_vertical_win(player)
	hor_win = check_horizontal_win(player)
	diag_win = check_diagonal_win(player)

	if ver_win or hor_win or diag_win:
		return True
	else:
		return False


def check_vertical_win(player):
	for col in range(BOARD_COLS):
		if board[0][col] == player and board[1][col] == player and board[2][col] == player:
			draw_vertical_winning_line(col, player)
			return True

	return False


def check_horizontal_win(player):
	for row in range(BOARD_ROWS):
		if board[row][0] == player and board[row][1] == player and board[row][2] == player:
			draw_horizontal_winning_line(row, player)
			return True

	return False


def check_diagonal_win(player):
	if board[0][0] == player and board[1][1] == player and board[2][2] == player:
		draw_diagonal_winning_line(player)
		return True
	elif board[2][0] == player and board[1][1] == player and board[0][2] == player:
		draw_diagonal_winning_line(player, False)
		return True
	else:
		return False


def draw_vertical_winning_line(col, player):
	posX = col * BOARD_SIZE + BOARD_SIZE / 2

	if player == 1:
		pygame.draw.line(screen, CIRCLE_COLOR, (posX, 10),
		                 (posX, BOARD_HEIGHT - 10), CIRCLE_LINE_WIDTH)
	else:
		pygame.draw.line(screen, X_COLOR, (posX, 10),
		                 (posX, BOARD_HEIGHT - 10), CIRCLE_LINE_WIDTH)


def draw_horizontal_winning_line(row, player):
	posY = row * BOARD_SIZE + BOARD_SIZE / 2

	if player == 1:
		pygame.draw.line(screen, CIRCLE_COLOR, (10, posY),
		                 (BOARD_WIDTH - 10, posY), CIRCLE_LINE_WIDTH)
	else:
		pygame.draw.line(screen, X_COLOR, (10, posY),
		                 (BOARD_WIDTH - 10, posY), CIRCLE_LINE_WIDTH)


def draw_diagonal_winning_line(player, down_diag=True):
	if down_diag:
		if player == 1:
			pygame.draw.line(screen, CIRCLE_COLOR, (0, 25),
			                 (BOARD_WIDTH - 25, BOARD_HEIGHT - 25), X_LINE_WIDTH)
		else:
			pygame.draw.line(screen, X_COLOR, (25, 25),
			                 (BOARD_WIDTH - 25, BOARD_HEIGHT - 25), X_LINE_WIDTH)



board = np.zeros((BOARD_ROWS, BOARD_COLS))



pygame.init()
pygame.display.set_caption("TIC TAC TOE 🏓")
screen = pygame.display.set_mode((BOARD_WIDTH, BOARD_HEIGHT))
screen.fill(BG_COLOR)
draw_lines()
pygame.display.update()




player = 1
game_over = False
in_menu = True


while True:
    

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			sys.exit()

		if event.type == pygame.MOUSEBUTTONDOWN and not game_over:
			posY = event.pos[1]
			row = int(math.floor(posY / BOARD_SIZE))
			posX = event.pos[0]
			col = int(math.floor(posX / BOARD_SIZE))

			if player % 2 == 0:
				if available_square(row, col):
					mark_square(row, col, 1)

					if check_win(1):
						game_over = True

					player += 1

			else:
				if available_square(row, col):
					mark_square(row, col, 2)

					if check_win(2):
						game_over = True

					player += 1

			if full_board():
				game_over = True
	draw_figures()
	pygame.display.update()
   
