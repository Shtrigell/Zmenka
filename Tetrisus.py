import curses
import time
import random

def draw_lev2(win, sh, sw):
    wall = []
    x = int(sw / 4)
    x_2 = int(3 * sw / 4)
    for y in range(int(sh / 4), int(3 * sh / 4)):
        wall.append((y, x))
        win.addstr(y, x, '|')
        wall.append((y, x_2))
        win.addstr(y, x_2, '|')
    return wall

def food_disp(sh, sw, restricted_locs):
    food = None
    food_start_sec = None

    while food is None:
        new_food = (random.randint(1, sh - 1), random.randint(1, sw - 1))

        if new_food in restricted_locs:
            new_food = None
        else:
            food = new_food
            food_start_sec = time.time()
    return (food, food_start_sec)

def main(stdscr):
    stdscr.clear()
    sh = 30
    sw = 90

    win = curses.initscr()

    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_WHITE)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLUE)

    win.attron(curses.color_pair(2))
    win.border()
    win.attroff(curses.color_pair(2))

    win.keypad(True)

    vel = 100
    win.timeout(vel)

    score = 0
    win.addstr(0, int(sw * 0.8), 'SCORE: {}'.format(score), curses.color_pair(1))

    lev2_score = 3
    level_now = 1
    walls = []

    vib_x = int(sw / 4)
    vib_y = int(sh / 2)

    snk = [(vib_y, vib_x),(vib_y, vib_x - 1),(vib_y, vib_x - 2)]

    d = curses.KEY_RIGHT

    food = (int(sh / 2), int(sw / 2))
    win.addch(food[0], food[1], curses.ACS_PI)
    food_start_sec = time.time()
    food_max_time = 5 

    while True:

        nhead = None

        if snk[0][0] in (0, sh) or snk[0][1] in (0, sw) or snk[0] in snk[1:] or snk[0] in walls:

            curses.endwin()
            print('GAME OVER')
            quit()
            

        key = win.getch()
        if key == -1:
            d = d
        else:
            d = key

        if d == ord('q'):
            break
        if d == curses.KEY_RIGHT or d == 454:
            nhead = (snk[0][0], snk[0][1] + 1)
        elif d == curses.KEY_LEFT or d == 452:
            nhead = (snk[0][0], snk[0][1] - 1)
        elif d == curses.KEY_UP or d == 450:
            nhead = (snk[0][0] - 1, snk[0][1])
        elif d == curses.KEY_DOWN or d == 456:
            nhead = (snk[0][0] + 1, snk[0][1])

        snk.insert(0, nhead)
        
        food_age = time.time() - food_start_sec

        if food_age > food_max_time:
            
            win.addch(food[0], food[1], ' ')

            food_start_sec = None

            food, food_start_sec = food_disp(sh, sw, snk)
            win.addch(food[0], food[1], curses.ACS_PI)

        if snk[0] == food:
            win.timeout(int(vel * 0.98))
            score += 1
            win.addstr(0, int(sw * 0.8), 'SCORE: {} '.format(score), curses.color_pair(1))

            if level_now == 1 and score >= lev2_score:
                walls = draw_lev2(win, sh, sw)

            food, food_start_sec = food_disp(sh, sw, snk)
            win.addch(food[0], food[1], curses.ACS_PI)
        else:
            tail = snk.pop()
            win.addch(tail[0], tail[1], ' ')

        win.addch(nhead[0], nhead[1], curses.ACS_BLOCK)

    print('GAME OVER')

curses.wrapper(main)







