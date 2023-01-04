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

spare = { 'shape': BEND,  'contents': None,          'rotation': 2 }

class Piece:
    def __init__(self, shape, contents, start_rotation, file_name):
        self.shape = shape
        self.contents = contents

        # the rotation of the piece in the photo
        self.start_rotation = start_rotation

        # actual rotation requested by the board. we start off assuming we want
        # it to look like in the photo
        self.rotation = start_rotation

        self.image = pygame.image.load(file_name)
        self.image = pygame.transform.smoothscale(self.image, (piece_width, piece_height))

    def __str__(self):
        return f"{self.shape}, {self.contents}, rot={self.rotation}"

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
                image = pygame.transform.rotate(piece.image, (piece.rotation - piece.start_rotation) * 90.0)
                screen.blit(image, position)

    # returns the piece if we can slide
    # if we can't slide, it returns None
    def slide(self, x, y, old_spare):
        # can't slide if we're not at an edge
        if x > 0 and x < 6 and y > 0 and y < 6:
            print(f"Cannot slide inside the board")
            return None

        # can't slide if we're on a static row
        if (x == 0 or x == 6) and (y % 2 == 0):
            print(f"Cannot slide on a static row")
            return None

        # can't slide if we're on a static column:
        if (y == 0 or y == 6) and (x % 2 == 0):
            print(f"Cannot slide on a static column")
            return None

        if x == 0:
            new_spare = self.pieces[y][6]
            for i in range(6, 0, -1):
                self.pieces[y][i] = self.pieces[y][i - 1]
            self.pieces[y][0] = old_spare
        elif x == 6:
            new_spare = self.pieces[y][0]
            for i in range(0, 6, 1):
                self.pieces[y][i] = self.pieces[y][i + 1]
            self.pieces[y][6] = old_spare
        elif y == 0:
            new_spare = self.pieces[6][x]
            for i in range(6, 0, -1):
                self.pieces[i][x] = self.pieces[i - 1][x]
            self.pieces[0][x] = old_spare
        elif y == 6:
            new_spare = self.pieces[0][x]
            for i in range(0, 6, 1):
                self.pieces[i][x] = self.pieces[i + 1][x]
            self.pieces[6][x] = old_spare
        else:
            printf("This should never happen!")
            exit()

        return new_spare

    def solve(self, route, x, y, finish_x, finish_y, entry_direction = None):
        # returns True if we found the finish point, False if we need to backtrack
        # accumulates the route directions in the route parameter

        route.positions.append([x, y])
        piece = self.pieces[y][x]

        exits = piece.exits()
        # 0 = North, 1 = East, 2 = South, 3= West
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
                    print(f"Refusing to loop back on ourselves dir={direction}, entry_dir={entry_direction}")
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
    if direction == None: opposite_direction = -1
    return opposite_direction

def wait_for_key():
    pygame.event.clear()
    while True:
        event = pygame.event.wait()
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            break

board = Board()

# load up the board with the pieces based on our photo of the board
x, y = 0, 0
for row in pieces:
    for p in row:
        piece = Piece(
            p['shape'],
            p['contents'],
            p['rotation'],
            f"img/labyrinth_{y}_{x}.jpg",
        )
        board.pieces[y][x] = piece
        x = x + 1
    x = 0
    y = y + 1

spare = Piece(
    spare['shape'],
    spare['contents'],
    spare['rotation'],
    f"img/spare.jpg",
)

screen.fill(black)
board.draw()
pygame.display.flip()
pygame.event.get()

# search all possible slides
for side in range(0, 4):
    for i in range(1, 6, 2):
        if side == 0:
            x1 = i; x2 = i;
            y1 = 0; y2 = 6;
        elif side == 1:
            x1 = 0; x2 = 6;
            y1 = i; y2 = i;
        elif side == 2:
            x1 = i; x2 = i;
            y1 = 6; y2 = 0;
        elif side == 3:
            x1 = 6; x2 = 0;
            y1 = i; y2 = i;

        for rotation in range(0, 4):
            route = Route()

            spare.rotation = rotation
            print(f"\nSliding {spare} into {x1},{y1}")
            spare = board.slide(x1, y1, spare)
            #success = board.solve(route, 6, 0, 4, 2)
            success = board.solve(route, 0, 0, 1, 5)
            board.draw()
            pygame.display.flip()
            if success:
                print(f"Route succeeded! {route}")
                route.draw()
            else:
                print(f"Failed to route!")

            wait_for_key()

            print(f"Sliding back {spare} into {x2},{y2}")
            spare = board.slide(x2, y2, spare)
            board.draw()
            pygame.display.flip()
            pygame.time.wait(200)

# success = board.solve(route, 6, 0, 4, 2)
# success = board.solve(route, 6, 5, 5, 3)

# if success:
#     print(f"Route succeeded! {route}")
#     route.draw()
# else:
#     print(f"Failed to route!")

wait_for_key()
