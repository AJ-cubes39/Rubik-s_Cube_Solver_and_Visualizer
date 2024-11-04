from vpython import *
import numpy as np


class Rubik_Cube:
    def __init__(self):
        self.my_cube = None
        self.running = True
        self.tiles = []
        self.dA = np.pi / 40
        # center
        sphere(pos=vector(0, 0, 0), size=vector(3, 3, 3), color=vector(0, 0, 0))
        tile_pos = [[vector(-1, 1, 1.5), vector(0, 1, 1.5), vector(1, 1, 1.5),  # front
                     vector(-1, 0, 1.5), vector(0, 0, 1.5), vector(1, 0, 1.5),
                     vector(-1, -1, 1.5), vector(0, -1, 1.5), vector(1, -1, 1.5), ],
                    [vector(1.5, 1, -1), vector(1.5, 1, 0), vector(1.5, 1, 1),  # right
                     vector(1.5, 0, -1), vector(1.5, 0, 0), vector(1.5, 0, 1),
                     vector(1.5, -1, -1), vector(1.5, -1, 0), vector(1.5, -1, 1), ],
                    [vector(-1, 1, -1.5), vector(0, 1, -1.5), vector(1, 1, -1.5),  # back
                     vector(-1, 0, -1.5), vector(0, 0, -1.5), vector(1, 0, -1.5),
                     vector(-1, -1, -1.5), vector(0, -1, -1.5), vector(1, -1, -1.5), ],
                    [vector(-1.5, 1, -1), vector(-1.5, 1, 0), vector(-1.5, 1, 1),  # left
                     vector(-1.5, 0, -1), vector(-1.5, 0, 0), vector(-1.5, 0, 1),
                     vector(-1.5, -1, -1), vector(-1.5, -1, 0), vector(-1.5, -1, 1), ],
                    [vector(-1, 1.5, -1), vector(0, 1.5, -1), vector(1, 1.5, -1),  # top
                     vector(-1, 1.5, 0), vector(0, 1.5, 0), vector(1, 1.5, 0),
                     vector(-1, 1.5, 1), vector(0, 1.5, 1), vector(1, 1.5, 1), ],
                    [vector(-1, -1.5, -1), vector(0, -1.5, -1), vector(1, -1.5, -1),  # bottom
                     vector(-1, -1.5, 0), vector(0, -1.5, 0), vector(1, -1.5, 0),
                     vector(-1, -1.5, 1), vector(0, -1.5, 1), vector(1, -1.5, 1), ],
                    ]
        colors = [vector(0, 1, 0), vector(1, 0, 0), vector(0, 0, 1), vector(1, 0.5, 0), vector(1, 1, 1),
                  vector(1, 1, 0)]
        angle = [(0, vector(0, 0, 0)), (np.pi / 2, vector(0, 1, 0)), (0, vector(0, 0, 0)), (np.pi / 2, vector(0, 1, 0)),
                 (np.pi / 2, vector(1, 0, 0)), (np.pi / 2, vector(1, 0, 0))]
        # sides
        for rank, side in enumerate(tile_pos):
            for my_vec in side:
                tile = box(pos=my_vec, size=vector(0.98, 0.98, 0.1), color=colors[rank])
                tile.rotate(angle=angle[rank][0], axis=angle[rank][1])
                self.tiles.append(tile)
        # positions
        self.positions = {'front': [], 'right': [], 'back': [], 'left': [], 'top': [], 'bottom': []}
        # variables
        self.rotate = [None, 0, 0]
        self.moves = []

    def reset_positions(self):
        self.positions = {'front': [], 'right': [], 'back': [], 'left': [], 'top': [], 'bottom': []}
        for tile in self.tiles:
            if tile.pos.z > 0.4:
                self.positions['front'].append(tile)
            if tile.pos.x > 0.4:
                self.positions['right'].append(tile)
            if tile.pos.z < -0.4:
                self.positions['back'].append(tile)
            if tile.pos.x < -0.4:
                self.positions['left'].append(tile)
            if tile.pos.y > 0.4:
                self.positions['top'].append(tile)
            if tile.pos.y < -0.4:
                self.positions['bottom'].append(tile)
        for key in self.positions.keys():
            self.positions[key] = set(self.positions[key])

    def animations(self):
        if self.rotate[0] == 'front_counter':
            pieces = self.positions['front']
            for tile in pieces:
                tile.rotate(angle=self.dA, axis=vector(0, 0, 1), origin=vector(0, 0, 0))
            self.rotate[1] += self.dA
        elif self.rotate[0] == 'right_counter':
            pieces = self.positions['right']
            for tile in pieces:
                tile.rotate(angle=self.dA, axis=vector(1, 0, 0), origin=vector(0, 0, 0))
            self.rotate[1] += self.dA
        elif self.rotate[0] == 'back_counter':
            pieces = self.positions['back']
            for tile in pieces:
                tile.rotate(angle=self.dA, axis=vector(0, 0, -1), origin=vector(0, 0, 0))
            self.rotate[1] += self.dA
        elif self.rotate[0] == 'left_counter':
            pieces = self.positions['left']
            for tile in pieces:
                tile.rotate(angle=self.dA, axis=vector(-1, 0, 0), origin=vector(0, 0, 0))
            self.rotate[1] += self.dA
        elif self.rotate[0] == 'top_counter':
            pieces = self.positions['top']
            for tile in pieces:
                tile.rotate(angle=self.dA, axis=vector(0, 1, 0), origin=vector(0, 0, 0))
            self.rotate[1] += self.dA
        elif self.rotate[0] == 'bottom_counter':
            pieces = self.positions['bottom']
            for tile in pieces:
                tile.rotate(angle=self.dA, axis=vector(0, -1, 0), origin=vector(0, 0, 0))
            self.rotate[1] += self.dA
        elif self.rotate[0] == 'front_clock':
            pieces = self.positions['front']
            for tile in pieces:
                tile.rotate(angle=(-self.dA), axis=vector(0, 0, 1), origin=vector(0, 0, 0))
            self.rotate[1] += self.dA
        elif self.rotate[0] == 'right_clock':
            pieces = self.positions['right']
            for tile in pieces:
                tile.rotate(angle=(-self.dA), axis=vector(1, 0, 0), origin=vector(0, 0, 0))
            self.rotate[1] += self.dA
        elif self.rotate[0] == 'back_clock':
            pieces = self.positions['back']
            for tile in pieces:
                tile.rotate(angle=(-self.dA), axis=vector(0, 0, -1), origin=vector(0, 0, 0))
            self.rotate[1] += self.dA
        elif self.rotate[0] == 'left_clock':
            pieces = self.positions['left']
            for tile in pieces:
                tile.rotate(angle=(-self.dA), axis=vector(-1, 0, 0), origin=vector(0, 0, 0))
            self.rotate[1] += self.dA
        elif self.rotate[0] == 'top_clock':
            pieces = self.positions['top']
            for tile in pieces:
                tile.rotate(angle=(-self.dA), axis=vector(0, 1, 0), origin=vector(0, 0, 0))
            self.rotate[1] += self.dA
        elif self.rotate[0] == 'bottom_clock':
            pieces = self.positions['bottom']
            for tile in pieces:
                tile.rotate(angle=(-self.dA), axis=vector(0, -1, 0), origin=vector(0, 0, 0))
            self.rotate[1] += self.dA
        if self.rotate[1] + self.dA / 2 > self.rotate[2] > self.rotate[1] - self.dA / 2:
            self.rotate = [None, 0, 0]
            self.reset_positions()

    def rotate_front_counter(self):
        if self.rotate[0] is None:
            self.rotate = ['front_counter', 0, np.pi / 2]

    def rotate_right_counter(self):
        if self.rotate[0] is None:
            self.rotate = ['right_counter', 0, np.pi / 2]

    def rotate_back_counter(self):
        if self.rotate[0] is None:
            self.rotate = ['back_counter', 0, np.pi / 2]

    def rotate_left_counter(self):
        if self.rotate[0] is None:
            self.rotate = ['left_counter', 0, np.pi / 2]

    def rotate_top_counter(self):
        if self.rotate[0] is None:
            self.rotate = ['top_counter', 0, np.pi / 2]

    def rotate_bottom_counter(self):
        if self.rotate[0] is None:
            self.rotate = ['bottom_counter', 0, np.pi / 2]

    def rotate_front_clock(self):
        if self.rotate[0] is None:
            self.rotate = ['front_clock', 0, np.pi / 2]

    def rotate_right_clock(self):
        if self.rotate[0] is None:
            self.rotate = ['right_clock', 0, np.pi / 2]

    def rotate_back_clock(self):
        if self.rotate[0] is None:
            self.rotate = ['back_clock', 0, np.pi / 2]

    def rotate_left_clock(self):
        if self.rotate[0] is None:
            self.rotate = ['left_clock', 0, np.pi / 2]

    def rotate_top_clock(self):
        if self.rotate[0] is None:
            self.rotate = ['top_clock', 0, np.pi / 2]

    def rotate_bottom_clock(self):
        if self.rotate[0] is None:
            self.rotate = ['bottom_clock', 0, np.pi / 2]

    def move(self):
        possible_moves = ["F", "R", "B", "L", "U", "D", "F'", "R'", "B'", "L'", "U'", "D'", "F2", "R2", "B2", "L2",
                          "U2", "D2"]
        if self.rotate[0] is None and len(self.moves) > 0:
            if self.moves[0] == possible_moves[0]:
                self.rotate_front_clock()
            elif self.moves[0] == possible_moves[1]:
                self.rotate_right_clock()
            elif self.moves[0] == possible_moves[2]:
                self.rotate_back_clock()
            elif self.moves[0] == possible_moves[3]:
                self.rotate_left_clock()
            elif self.moves[0] == possible_moves[4]:
                self.rotate_top_clock()
            elif self.moves[0] == possible_moves[5]:
                self.rotate_bottom_clock()
            elif self.moves[0] == possible_moves[6]:
                self.rotate_front_counter()
            elif self.moves[0] == possible_moves[7]:
                self.rotate_right_counter()
            elif self.moves[0] == possible_moves[8]:
                self.rotate_back_counter()
            elif self.moves[0] == possible_moves[9]:
                self.rotate_left_counter()
            elif self.moves[0] == possible_moves[10]:
                self.rotate_top_counter()
            elif self.moves[0] == possible_moves[11]:
                self.rotate_bottom_counter()
            elif self.moves[0] == possible_moves[12]:
                self.rotate_front_clock()
                self.rotate_front_clock()
            elif self.moves[0] == possible_moves[13]:
                self.rotate_right_clock()
                self.rotate_right_clock()
            elif self.moves[0] == possible_moves[14]:
                self.rotate_back_clock()
                self.rotate_back_clock()
            elif self.moves[0] == possible_moves[15]:
                self.rotate_left_clock()
                self.rotate_left_clock()
            elif self.moves[0] == possible_moves[16]:
                self.rotate_top_clock()
                self.rotate_top_clock()
            elif self.moves[0] == possible_moves[17]:
                self.rotate_bottom_clock()
                self.rotate_bottom_clock()
            self.moves.pop(0)

    def scramble(self, my_list):
        if len(my_list) == 1:
            self.moves.append(my_list[0])
        else:
            for i in range(len(my_list) - 1):
                if my_list[i + 1] == "'":
                    for_now = my_list[i] + my_list[i + 1]
                    self.moves.append(for_now)
                elif my_list[i + 1] == "2":
                    self.moves.append(my_list[i])
                    self.moves.append(my_list[i])
                elif my_list[i] != "2" and my_list[i] != "'":
                    self.moves.append(my_list[i])
                elif i + 1 == len(my_list) - 1 and my_list[i + 1] != "2" and my_list[i + 1] != "'":
                    self.moves.append(my_list[i + 1])

    def control(self):
        button(bind=self.next_move, text='Next Move')

    def next_move(self):
        if len(self.my_cube) == 0:
            print("Done")
        else:
            if len(self.my_cube) == 1:
                self.moves.append(self.my_cube[0])
                self.my_cube.pop(0)
            else:
                if self.my_cube[1] == "'":
                    for_now = self.my_cube[0] + self.my_cube[1]
                    self.moves.append(for_now)
                    self.my_cube.pop(0)
                    self.my_cube.pop(0)
                elif self.my_cube[1] == "2":
                    self.moves.append(self.my_cube[0])
                    self.moves.append(self.my_cube[0])
                    self.my_cube.pop(0)
                    self.my_cube.pop(0)
                elif self.my_cube[0] != "2" and self.my_cube[0] != "'":
                    self.moves.append(self.my_cube[0])
                    self.my_cube.pop(0)
                elif 1 == len(self.my_cube) - 1 and self.my_cube[1] != "2" and self.my_cube[1] != "'":
                    self.moves.append(self.my_cube[1])
                    self.my_cube.pop(1)

    def update(self):
        rate(60)
        self.animations()
        self.move()

    def start(self, my_scramble, my_solve):
        self.my_cube = my_solve
        self.scramble(my_scramble)
        self.control()
        while self.running:
            self.update()
