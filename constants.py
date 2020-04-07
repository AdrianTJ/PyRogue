import pygame
import tcod as libtcod

pygame.init()

# Game Sizes
GAME_WIDTH = 800
GAME_HEIGHT = 600
CELL_WIDTH = 32
CELL_HEIGHT = 32

# Map Variables
MAP_WIDTH = 20
MAP_HEIGHT = 20

# Color definitions
COLOR_BLACK = (0, 0, 0)
COLOR_WHITE = (255, 255, 255)
COLOR_GREY = (100, 100, 100)

# Game Colors
COLOR_DEFAULT_BG = COLOR_GREY

# Sprites
S_PLAYER = pygame.image.load("./data/snake.png")
S_ENEMY = pygame.image.load("./data/enemy.png")
S_WALL = pygame.image.load('./data/wall.jpg')
S_FLOOR = pygame.image.load('./data/floor.jpg')
S_WALL_EX = pygame.image.load("./data/wall.jpg")
S_FLOOR_EX = pygame.image.load("./data/floor.jpg")

S_WALL_EX.fill ((40,50,60), special_flags = pygame.BLEND_RGBA_MULT)
S_FLOOR_EX.fill ((40,50,60), special_flags = pygame.BLEND_RGBA_MULT)

# FOV settings
FOV_ALGO = libtcod.FOV_BASIC
FOV_LIGHT_WALLS = True
TORCH_RADIUS = 10