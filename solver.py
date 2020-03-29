#!/usr/bin/env python3

import pygame
import sys

pygame.init()

size = width, height = 1024, 1024
black = 0, 0, 0

screen = pygame.display.set_mode(size)

pieces = [[None for x in range(7)] for y in range(7)]
piece_pos = [[None for x in range(7)] for y in range(7)]
for x in range(7):
    for y in range(7):
        piece = pygame.image.load(f"img/labyrinth_{y}_{x}.jpg")
        w = int(width / 7)
        h = int(height / 7)
        pieces[y][x] = pygame.transform.smoothscale(piece, (w, h))
        rect = pieces[y][x].get_rect()
        piece_pos[y][x] = pygame.Rect(x * w, y * h, w, h)

angle = 0.0;
while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()

    screen.fill(black)

    for x in range(7):
        for y in range (7):
            angle += 0.01
            piece = pygame.transform.rotate(pieces[y][x], angle)
            screen.blit(piece, piece_pos[y][x])

    pygame.display.flip()

PIPE =  "pipe"
TEE =   "tee"
ELBOW = "elbow"

pieces = [
    [ # top row (row 0)
        { shape: ELBOW, contents: "red",         orientation: 3 },
        { shape: PIPE,  contents: None,          orientation: 1 },
        { shape: TEE,   contents: "skull",       orientation: 1 },
        { shape: ELBOW, contents: None,          orientation: 1 },
        { shape: TEE,   contents: "sword",       orientation: 1 },
        { shape: ELBOW, contents: None,          orientation: 1 },
        { shape: ELBOW, contents: "blue",        orientation: 0 },
    ],
    [ # row 1
        { shape: PIPE,  contents: None,          orientation: 1 },
        { shape: ELBOW, contents: None,          orientation: 2 },
        { shape: PIPE,  contents: None,          orientation: 0 },
        { shape: TEE,   contents: "troll",       orientation: 1 },
        { shape: ELBOW, contents: "salamander",  orientation: 0 },
        { shape: PIPE,  contents: None,          orientation: 0 },
        { shape: ELBOW, contents: "moth",        orientation: 0 },
    ],
    [ # row 2
        { shape: TEE,   contents: "gold",        orientation: 0 },
        { shape: PIPE,  contents: None,          orientation: 0 },
        { shape: TEE,   contents: "keys",        orientation: 0 },
        { shape: ELBOW, contents: "spider",      orientation: 3 },
        { shape: TEE,   contents: "jewel",       orientation: 1 },
        { shape: PIPE,  contents: None,          orientation: 1 },
        { shape: TEE,   contents: "helmet",      orientation: 2 },
    ],
    [ # row 3
        { shape: TEE,   contents: "ghost",       orientation: 2 },
        { shape: PIPE,  contents: None,          orientation: 1 },
        { shape: PIPE,  contents: None,          orientation: 0 },
        { shape: ELBOW, contents: None,          orientation: 0 },
        { shape: ELBOW, contents: None,          orientation: 2 },
        { shape: ELBOW, contents: None,          orientation: 1 },
        { shape: TEE,   contents: "dragon",      orientation: 2 },
    ],
    [ # row 4
        { shape: TEE,   contents: "book",        orientation: 0 },
        { shape: PIPE,  contents: None,          orientation: 0 },
        { shape: TEE,   contents: "crown",       orientation: 3 },
        { shape: TEE,   contents: "princess",    orientation: 2 },
        { shape: TEE,   contents: "treasure",    orientation: 2 },
        { shape: ELBOW, contents: "owl",         orientation: 3 },
        { shape: TEE,   contents: "candelabra",  orientation: 2 },
    ],
    [ # row 5
        { shape: ELBOW, contents: "rat",         orientation: 2 },
        { shape: TEE,   contents: "bat",         orientation: 0 },
        { shape: TEE,   contents: "genie",       orientation: 3 },
        { shape: ELBOW, contents: None,          orientation: 3 },
        { shape: PIPE,  contents: None,          orientation: 0 },
        { shape: ELBOW, contents: None,          orientation: 3 },
        { shape: ELBOW, contents: "scarab",      orientation: 2 },
    ],
    [ # row 6 (bottom row)
        { shape: ELBOW, contents: "yellow",      orientation: 2 },
        { shape: PIPE,  contents: None,          orientation: 0 },
        { shape: TEE,   contents: "map",         orientation: 3 },
        { shape: ELBOW, contents: None,          orientation: 0 },
        { shape: TEE,   contents: "ring",        orientation: 3 },
        { shape: PIPE,  contents: None,          orientation: 1 },
        { shape: ELBOW, contents: "green",       orientation: 1 },
    ],
]

spare = { shape: ELBOW, contents: None }

print("HELLO ISLA")