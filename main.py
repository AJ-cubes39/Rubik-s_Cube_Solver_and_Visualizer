import cv2
import numpy as np
import kociemba as kociemba_cube
import colorama

import cube

GREEN = colorama.Fore.GREEN
GRAY = colorama.Fore.LIGHTBLACK_EX
RESET = colorama.Fore.RESET
RED = colorama.Fore.RED
MAGENTA = colorama.Fore.MAGENTA
colorama.init()

state = {
    'up': ['white', 'white', 'white', 'white', 'white', 'white', 'white', 'white', 'white', ],
    'right': ['white', 'white', 'white', 'white', 'white', 'white', 'white', 'white', 'white', ],
    'front': ['white', 'white', 'white', 'white', 'white', 'white', 'white', 'white', 'white', ],
    'down': ['white', 'white', 'white', 'white', 'white', 'white', 'white', 'white', 'white', ],
    'left': ['white', 'white', 'white', 'white', 'white', 'white', 'white', 'white', 'white', ],
    'back': ['white', 'white', 'white', 'white', 'white', 'white', 'white', 'white', 'white', ]
}

sign_conv = {
    'green': 'F',
    'white': 'U',
    'blue': 'B',
    'red': 'R',
    'orange': 'L',
    'yellow': 'D'
}

color = {
    'red': (0, 0, 255),
    'orange': (0, 165, 255),
    'blue': (255, 0, 0),
    'green': (0, 255, 0),
    'white': (255, 255, 255),
    'yellow': (0, 255, 255)
}

stickers = {
    'main': [
        [200, 120], [300, 120], [400, 120],
        [200, 220], [300, 220], [400, 220],
        [200, 320], [300, 320], [400, 320]
    ],
    'current': [
        [20, 20], [54, 20], [88, 20],
        [20, 54], [54, 54], [88, 54],
        [20, 88], [54, 88], [88, 88]
    ],
    'preview': [
        [20, 130], [54, 130], [88, 130],
        [20, 164], [54, 164], [88, 164],
        [20, 198], [54, 198], [88, 198]
    ],
    'left': [
        [50, 280], [94, 280], [138, 280],
        [50, 324], [94, 324], [138, 324],
        [50, 368], [94, 368], [138, 368]
    ],
    'front': [
        [188, 280], [232, 280], [276, 280],
        [188, 324], [232, 324], [276, 324],
        [188, 368], [232, 368], [276, 368]
    ],
    'right': [
        [326, 280], [370, 280], [414, 280],
        [326, 324], [370, 324], [414, 324],
        [326, 368], [370, 368], [414, 368]
    ],
    'up': [
        [188, 128], [232, 128], [276, 128],
        [188, 172], [232, 172], [276, 172],
        [188, 216], [232, 216], [276, 216]
    ],
    'down': [
        [188, 434], [232, 434], [276, 434],
        [188, 478], [232, 478], [276, 478],
        [188, 522], [232, 522], [276, 522]
    ],
    'back': [
        [464, 280], [508, 280], [552, 280],
        [464, 324], [508, 324], [552, 324],
        [464, 368], [508, 368], [552, 368]
    ],
}

font = cv2.FONT_HERSHEY_SIMPLEX
textPoints = {
    'up': [['U', 242, 202], ['W', (255, 255, 255), 260, 208]],
    'right': [['R', 380, 354], ['R', (0, 0, 255), 398, 360]],
    'front': [['F', 242, 354], ['G', (0, 255, 0), 260, 360]],
    'down': [['D', 242, 508], ['Y', (0, 255, 255), 260, 514]],
    'left': [['L', 104, 354], ['O', (0, 165, 255), 122, 360]],
    'back': [['B', 518, 354], ['B', (255, 0, 0), 536, 360]],
}

check_state = []
solution = []
solved = False

cap = cv2.VideoCapture(0)
cv2.namedWindow('frame')


def rotate(side):
    my_main = state[side]
    front = state['front']
    left = state['left']
    right = state['right']
    up = state['up']
    down = state['down']
    back = state['back']

    if side == 'front':
        left[2], left[5], left[8], up[6], up[7], up[8], right[0], right[3], right[6], down[0], down[1], down[2] = down[
            0], down[1], down[2], left[8], left[5], left[2], up[6], up[7], up[8], right[6], right[3], right[0]
    elif side == 'up':
        left[0], left[1], left[2], back[0], back[1], back[2], right[0], right[1], right[2], front[0], front[1], front[
            2] = (front[0], front[1], front[2], left[0], left[1], left[2], back[0], back[1], back[2], right[0],
                  right[1],
                  right[2])
    elif side == 'down':
        left[6], left[7], left[8], back[6], back[7], back[8], right[6], right[7], right[8], front[6], front[7], front[
            8] = back[6], back[7], back[8], right[6], right[7], right[8], front[6], front[7], front[8], left[6], left[
            7], left[8]
    elif side == 'back':
        (left[0], left[3], left[6], up[0], up[1], up[2], right[2], right[5], right[8], down[6], down[7],
         down[8]) = up[2], \
            up[1], up[0], right[2], right[5], right[8], down[8], down[7], down[6], left[0], left[3], left[6]
    elif side == 'left':
        (front[0], front[3], front[6], down[0], down[3], down[6], back[2], back[5], back[8], up[0], up[3],
         up[6]) = up[0], \
            up[3], up[6], front[0], front[3], front[6], down[6], down[3], down[0], back[8], back[5], back[2]
    elif side == 'right':
        front[2], front[5], front[8], down[2], down[5], down[8], back[0], back[3], back[6], up[2], up[5], up[8] = down[
            2], down[5], down[8], back[6], back[3], back[0], up[8], up[5], up[2], front[2], front[5], front[8]

    (my_main[0], my_main[1], my_main[2], my_main[3], my_main[4], my_main[5], my_main[6], my_main[7],
     my_main[8]) = \
        my_main[6], my_main[3], my_main[0], my_main[
            7], my_main[4], my_main[1], my_main[8], my_main[5], my_main[2]


def rotate_module(side):
    main = state[side]
    front = state['front']
    left = state['left']
    right = state['right']
    up = state['up']
    down = state['down']
    back = state['back']

    if side == 'front':
        (left[2], left[5], left[8], up[6], up[7], up[8], right[0], right[3], right[6], down[0], down[1],
         down[2]) = up[8], \
            up[7], up[6], right[0], right[3], right[6], down[2], down[1], down[0], left[2], left[5], left[8]
    elif side == 'up':
        left[0], left[1], left[2], back[0], back[1], back[2], right[0], right[1], right[2], front[0], front[1], front[
            2] = back[0], back[1], back[2], right[0], right[1], right[2], front[0], front[1], front[2], left[0], left[
            1], left[2]
    elif side == 'down':
        left[6], left[7], left[8], back[6], back[7], back[8], right[6], right[7], right[8], front[6], front[7], front[
            8] = (front[6], front[7], front[8], left[6], left[7], left[8], back[6], back[7], back[8], right[6],
                  right[7],
                  right[8])
    elif side == 'back':
        left[0], left[3], left[6], up[0], up[1], up[2], right[2], right[5], right[8], down[6], down[7], down[8] = down[
            6], down[7], down[8], left[6], left[3], left[0], up[0], up[1], up[2], right[8], right[5], right[2]
    elif side == 'left':
        front[0], front[3], front[6], down[0], down[3], down[6], back[2], back[5], back[8], up[0], up[3], up[6] = down[
            0], down[3], down[6], back[8], back[5], back[2], up[0], up[3], up[6], front[0], front[3], front[6]
    elif side == 'right':
        (front[2], front[5], front[8], down[2], down[5], down[8], back[0], back[3], back[6], up[2], up[5],
         up[8]) = up[2], \
            up[5], up[8], front[2], front[5], front[8], down[8], down[5], down[2], back[6], back[3], back[0]

    main[0], main[1], main[2], main[3], main[4], main[5], main[6], main[7], main[8] = main[2], main[5], main[8], main[
        1], main[4], main[7], main[0], main[3], main[6]


def solve(local_state):
    raw = ''
    for local_i in local_state:
        for j in local_state[local_i]:
            raw += sign_conv[j]
    print("answer:", kociemba_cube.solve(raw))
    return kociemba_cube.solve(raw)


def my_scrambler(my_state):
    raw = ''
    for local_i in my_state:
        for j in my_state[local_i]:
            raw += sign_conv[j]
    return raw


def color_detect(h, s):
    if 9 >= h:
        return 'red'
    elif 16 >= h >= 11:
        return 'orange'
    elif 37 >= h >= 24:
        return 'yellow'
    elif 69 >= h >= 37 and s >= 32:
        return 'green'
    elif h >= 108:
        return 'blue'
    elif 40 >= s:
        return 'white'

    return 'white'


def draw_stickers(local_frame, local_stickers, name):
    for local_x, local_y in local_stickers[name]:
        cv2.rectangle(local_frame, (local_x, local_y), (local_x + 30, local_y + 30), (255, 255, 255), 2)


def draw_preview_stickers(local_frame, local_stickers):
    stick = ['front', 'back', 'left', 'right', 'up', 'down']
    for name in stick:
        for local_x, local_y in local_stickers[name]:
            cv2.rectangle(local_frame, (local_x, local_y), (local_x + 40, local_y + 40), (255, 255, 255), 2)


def text_on_preview_stickers(local_stickers):
    stick = ['front', 'back', 'left', 'right', 'up', 'down']
    for name in stick:
        for local_x, local_y in local_stickers[name]:
            sym, x1, y1 = textPoints[name][0][0], textPoints[name][0][1], textPoints[name][0][2]
            cv2.putText(preview, sym, (x1, y1), font, 1, (0, 0, 0), 1, cv2.LINE_AA)
            sym, col, x1, y1 = textPoints[name][1][0], textPoints[name][1][1], textPoints[name][1][2], \
                textPoints[name][1][3]
            cv2.putText(preview, sym, (x1, y1), font, 0.5, col, 1, cv2.LINE_AA)
            if local_x == local_y:
                pass


def fill_stickers(local_frame, local_stickers, sides):
    for side, colors in sides.items():
        num = 0
        for local_x, local_y in local_stickers[side]:
            cv2.rectangle(local_frame, (local_x, local_y), (local_x + 40, local_y + 40), color[colors[num]], -1)
            num += 1


def process(local_operation):
    replace = {
        "F": [rotate, 'front'],
        "F2": [rotate, 'front', 'front'],
        "F'": [rotate_module, 'front'],
        "U": [rotate, 'up'],
        "U2": [rotate, 'up', 'up'],
        "U'": [rotate_module, 'up'],
        "L": [rotate, 'left'],
        "L2": [rotate, 'left', 'left'],
        "L'": [rotate_module, 'left'],
        "R": [rotate, 'right'],
        "R2": [rotate, 'right', 'right'],
        "R'": [rotate_module, 'right'],
        "D": [rotate, 'down'],
        "D2": [rotate, 'down', 'down'],
        "D'": [rotate_module, 'down'],
        "B": [rotate, 'back'],
        "B2": [rotate, 'back', 'back'],
        "B'": [rotate_module, 'back']
    }
    local_a = 0
    for local_i in local_operation:
        for j in range(len(replace[local_i]) - 1):
            replace[local_i][0](replace[local_i][j + 1])
        cv2.putText(preview, local_i, (700, local_a + 50), font, 1, (0, 255, 0), 1, cv2.LINE_AA)
        fill_stickers(preview, stickers, state)
        solution.append(preview)
        cv2.imshow('solution', preview)
        cv2.waitKey()
        cv2.putText(preview, local_i, (700, 50), font, 1, (0, 0, 0), 1, cv2.LINE_AA)


if __name__ == '__main__':
    preview = np.zeros((700, 800, 3), np.uint8)
    while True:
        hsv = []
        current_state = []
        ret, img = cap.read()
        frame = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        mask = np.zeros(frame.shape, dtype=np.uint8)

        draw_stickers(img, stickers, 'main')
        draw_stickers(img, stickers, 'current')
        draw_preview_stickers(preview, stickers)
        fill_stickers(preview, stickers, state)
        text_on_preview_stickers(stickers)

        for i in range(9):
            hsv.append(frame[stickers['main'][i][1] + 10][stickers['main'][i][0] + 10])

        a = 0
        for x, y in stickers['current']:
            color_name = color_detect(hsv[a][0], hsv[a][1])
            cv2.rectangle(img, (x, y), (x + 30, y + 30), color[color_name], -1)
            a += 1
            current_state.append(color_name)

        k = cv2.waitKey(5) & 0xFF
        if k == 27:
            break
        elif k == ord('u'):
            state['up'] = current_state
            check_state.append('u')
        elif k == ord('r'):
            check_state.append('r')
            state['right'] = current_state
        elif k == ord('l'):
            check_state.append('l')
            state['left'] = current_state
        elif k == ord('d'):
            check_state.append('d')
            state['down'] = current_state
        elif k == ord('f'):
            check_state.append('f')
            state['front'] = current_state
        elif k == ord('b'):
            check_state.append('b')
            state['back'] = current_state
        elif k == ord('\r'):
            # process(["R","R'"])
            if len(set(check_state)) == 6:
                try:
                    solved = solve(state)
                    if solved:
                        my_cube = cube.Rubik_Cube()
                        my_cube.start(list(kociemba_cube.solve("UUUUUUUUURRRRRRRRRFFFFFFFFFDDDDDDDDDLLLLLLLLLBBBBBBBBB",
                                                               my_scrambler(state)).replace(" ", "")),
                                      list(kociemba_cube.solve(my_scrambler(state)).replace(" ", "")))
                        operation = solved.split(' ')
                        process(operation)
                except Exception as e:
                    print("Error in the side detection process. You may have done held the cube wrong or some colors "
                          "were incorrectly scanned. Try again.")
                    if e == "":
                        pass
                    continue
            else:
                print("Some sides are not scanned. Please check the other window to see which sides haven't been "
                      "scanned.")
                print("There are", 6 - len(set(check_state)), "sides left to scan.")
        cv2.imshow('preview', preview)
        cv2.imshow('frame', img[0:500, 0:500])

    cv2.destroyAllWindows()
