#!/usr/bin/env python3

import pygame
import sys

size = board_width, board_height = 1024, 1024
black = 0, 0, 0

piece_width = int(board_width / 7)
piece_height = int(board_height / 7)

pygame.init()
screen = pygame.display.set_mode(size)

PIPE = "pipe" # is ⎮ in rotation 0
TEE  = "tee"  # is ├ in rotation 0
BEND = "bend" # is ⏋in rotation 0

pieces = [
    [ # row 0 (top row)
        { 'shape': BEND,  'contents': "red",         'rotation': 3 },
        { 'shape': PIPE,  'contents': None,          'rotation': 1 },
        { 'shape': TEE,   'contents': "skull",       'rotation': 1 },
        { 'shape': BEND,  'contents': None,          'rotation': 1 },
        { 'shape': TEE,   'contents': "sword",       'rotation': 1 },
        { 'shape': BEND,  'contents': None,          'rotation': 1 },
        { 'shape': BEND,  'contents': "blue",        'rotation': 0 },
    ],
    [ # row 1
        { 'shape': PIPE,  'contents': None,          'rotation': 1 },
        { 'shape': BEND,  'contents': None,          'rotation': 2 },
        { 'shape': PIPE,  'contents': None,          'rotation': 0 },
        { 'shape': TEE,   'contents': "troll",       'rotation': 1 },
        { 'shape': BEND,  'contents': "salamander",  'rotation': 0 },
        { 'shape': PIPE,  'contents': None,          'rotation': 0 },
        { 'shape': BEND,  'contents': "moth",        'rotation': 0 },
    ],
    [ # row 2
        { 'shape': TEE,   'contents': "gold",        'rotation': 0 },
        { 'shape': PIPE,  'contents': None,          'rotation': 0 },
        { 'shape': TEE,   'contents': "keys",        'rotation': 0 },
        { 'shape': BEND,  'contents': "spider",      'rotation': 3 },
        { 'shape': TEE,   'contents': "jewel",       'rotation': 1 },
        { 'shape': PIPE,  'contents': None,          'rotation': 1 },
        { 'shape': TEE,   'contents': "helmet",      'rotation': 2 },
    ],
    [ # row 3
        { 'shape': TEE,   'contents': "ghost",       'rotation': 2 },
        { 'shape': PIPE,  'contents': None,          'rotation': 1 },
        { 'shape': PIPE,  'contents': None,          'rotation': 0 },
        { 'shape': BEND,  'contents': None,          'rotation': 0 },
        { 'shape': BEND,  'contents': None,          'rotation': 2 },
        { 'shape': BEND,  'contents': None,          'rotation': 1 },
        { 'shape': TEE,   'contents': "dragon",      'rotation': 2 },
    ],
    [ # row 4
        { 'shape': TEE,   'contents': "book",        'rotation': 0 },
        { 'shape': PIPE,  'contents': None,          'rotation': 0 },
        { 'shape': TEE,   'contents': "crown",       'rotation': 3 },
        { 'shape': TEE,   'contents': "princess",    'rotation': 2 },
        { 'shape': TEE,   'contents': "treasure",    'rotation': 2 },
        { 'shape': BEND,  'contents': "owl",         'rotation': 3 },
        { 'shape': TEE,   'contents': "candelabra",  'rotation': 2 },
    ],
    [ # row 5
        { 'shape': BEND,  'contents': "rat",         'rotation': 2 },
        { 'shape': TEE,   'contents': "bat",         'rotation': 0 },
        { 'shape': TEE,   'contents': "genie",       'rotation': 3 },
        { 'shape': BEND,  'contents': None,          'rotation': 3 },
        { 'shape': PIPE,  'contents': None,          'rotation': 0 },
        { 'shape': BEND,  'contents': None,          'rotation': 3 },
        { 'shape': BEND,  'contents': "scarab",      'rotation': 2 },
    ],
    [ # row 6 (bottom row)
        { 'shape': BEND,  'contents': "yellow",      'rotation': 2 },
        { 'shape': PIPE,  'contents': None,          'rotation': 0 },
        { 'shape': TEE,   'contents': "map",         'rotation': 3 },
        { 'shape': BEND,  'contents': None,          'rotation': 0 },
        { 'shape': TEE,   'contents': "ring",        'rotation': 3 },
        { 'shape': PIPE,  'contents': None,          'rotation': 1 },
        { 'shape': BEND,  'contents': "green",       'rotation': 1 },
    ],
]

spare = { 'shape': BEND, 'contents': None }

class Piece:
    def __init__(self, shape, contents, start_rotation, start_x, start_y):
        self.shape = shape
        self.contents = contents

        # the rotation of the piece in the photo
        self.start_rotation = start_rotation

        # actual rotation requested by the board. we start off assuming we want
        # it to look like in the photo
        self.rotation = start_rotation

        self.image = pygame.image.load(f"img/labyrinth_{start_y}_{start_x}.jpg")
        self.image = pygame.transform.smoothscale(self.image, (piece_width, piece_height))

    def exits(self):
        if self.shape == PIPE:
            exits = [True, False, True, False]
        elif self.shape == TEE:
            exits = [True, True, True, False]
        elif self.shape == BEND:
            exits = [False, False, True, True]
        else:
            assert(f"No such shape {self.shape}")

        # return the exits, rotated by our current orientation
        r = self.rotation
        return [
            exits[(0 - r) % 4],
            exits[(1 - r) % 4],
            exits[(2 - r) % 4],
            exits[(3 - r) % 4],
        ]

class Route:
    def __init__(self):
        self.positions = []

    def draw(self):
        points = list(map(lambda p: [
            (p[0] + 0.5) * piece_width,
            (p[1] + 0.5) * piece_height,
        ], self.positions))
        pygame.draw.lines(
            screen,
            (255, 0, 0),
            False,
            points,
            3,
        )
        pygame.display.flip()

    def __str__(self):
        return ",".join(f"[{ position[0] },{ position[1] }]" for position in self.positions)

class Board:
    def __init__(self):
        self.pieces = [[None for x in range(7)] for y in range(7)]

    def draw(self):
        for x in range(7):
            for y in range(7):
                piece = self.pieces[y][x]
                rect = piece.image.get_rect()
                position = pygame.Rect(x * piece_width, y * piece_height, piece_width, piece_height)

                # piece = pygame.transform.rotate(pieces[y][x], angle)
                screen.blit(piece.image, position)

    def solve(self, route, x, y, finish_x, finish_y, entry_direction = 0):
        # returns True if we found the finish point, False if we need to backtrack
        # accumulates the route directions in the route parameter

        route.positions.append([x, y])
        piece = self.pieces[y][x]

        exits = piece.exits()
        for direction in [0, 1, 2, 3]:
            print(f"Searching: {x},{y} to {finish_x},{finish_y} with entry dir {entry_direction} in dir {direction} and exits {exits} and route {route}")
            if exits[direction] is True:
                x2, y2 = x, y
                if direction == 0:
                    y2 = y - 1
                elif direction == 1:
                    x2 = x + 1
                elif direction == 2:
                    y2 = y + 1
                elif direction == 3:
                    x2 = x - 1

                # check that we haven't gone off the board
                if (x2 < 0 or x2 > 6 or
                    y2 < 0 or y2 > 6):
                    print(f"We went off the board! {x2},{y2}")
                    continue

                # check we're not looping back on ourselves
                if direction == opposite_direction(entry_direction):
                    print(f"Refusing to loop back on ourselves")
                    continue

                # check that the new position has an entrance that matches this exit
                next_piece = self.pieces[y2][x2]
                entrances = next_piece.exits()
                entrance_direction = opposite_direction(direction)
                if entrances[entrance_direction] is False:
                    print(f"No entrance in direction {direction}")
                    continue

                # check if we've found our target
                if (x2 == finish_x and y2 == finish_y):
                    route.positions.append([x2, y2])
                    return True

                # otherwise, recurse into our new position
                success = self.solve(route, x2, y2, finish_x, finish_y, direction)
                if success:
                    return True
                else:
                    print(f"Failed to find a route in direction {direction}")
                    continue
            else:
                print(f"No exit in direction {direction}")

        # all our exits failed, so backtrack
        print("Failed to find any route forwards; backtracking")
        route.positions.pop()
        return False

def opposite_direction(direction):
    if direction == 0: opposite_direction = 2
    if direction == 1: opposite_direction = 3
    if direction == 2: opposite_direction = 0
    if direction == 3: opposite_direction = 1
    return opposite_direction

board = Board()

# load up the board with the pieces based on our photo of the board
x, y = 0, 0
for row in pieces:
    for p in row:
        piece = Piece(
            p['shape'],
            p['contents'],
            p['rotation'],
            x,
            y,
        )
        board.pieces[y][x] = piece
        x = x + 1
    x = 0
    y = y + 1

screen.fill(black)
board.draw()
pygame.display.flip()

route = Route()
success = board.solve(route, 0, 0, 3, 4)
# success = board.solve(route, 6, 5, 5, 3)
if success:
    print(f"Route succeeded! {route}")
    route.draw()
else:
    print(f"Failed to route!")

while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()

