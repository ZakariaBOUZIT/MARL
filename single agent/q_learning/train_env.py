'''
train env.
'''
from tkinter import *
import pickle
import random
master = Tk()
triangle_size = 0.001
cell_score_min = -1
cell_score_max = 1
score = 0
restart = False
goal1_done = False
walk_reward = -10
red_reward=-40
player_a,player_b,player_c,player_d=[2,2,8,8] #agent dim
actions = ["up", "down", "left", "right"]
########################################################################################################################
Width = 10
(x, y) = (500,500)
board = Canvas(master, width=x*Width, height=y*Width)
player_x=0
player_y=y-1
player=(player_x,player_y)
goal1_x=x-1
goal1_y=0

walls = []
specials = [(goal1_x, goal1_y, "green", 20)]

def generate_random():
    walls = []
    specials = [(goal_x, goal_y, "green", 50)]
    for i in range(10):
        for j in range(6):
            n = random.randint(0, x - 1)
            m = random.randint(0, y - 1)
            ns = random.randint(0, x - 1)
            ms = random.randint(0, y - 1)
            while (n==goal_x and m==goal_y) or (n==player_x and m==player_y ) or (ns==goal_x and ms==goal_y) or (ns==player_x and ms==player_y ):
                n = random.randint(0, x - 1)
                ns = random.randint(0, x - 1)
                m = random.randint(0, y - 1)
                ms = random.randint(0, y - 1)
            walls.append((n,m))
            s_=(ns,ms,"red",obs_reward)
            specials.append(s_)
    return walls,specials;

with open('walls.pickle', 'wb') as f:
    pickle.dump(walls, f)
with open('specials.pickle', 'wb') as f:
    pickle.dump(specials, f)
cell_scores = {}

def try_move(dx, dy):
    global player, x, y, score, walk_reward, me, restart ,goal1_x,goal1_y,red_reward
    #if restart == True:
     #   restart_game()
    new_x = player[0] + dx
    new_y = player[1] + dy
    score += walk_reward
    if (new_x >= 0) and (new_x < x) and (new_y >= 0) and (new_y < y) and not ((new_x, new_y) in walls):
        board.coords(me, new_x*Width+Width*player_a/10, new_y*Width+Width*player_b/10, new_x*Width+Width*player_c/10, new_y*Width+Width*player_d/10)
        player = (new_x, new_y)

    for (i, j, c, w) in specials:
        if new_x == i and new_y == j:
            score -=walk_reward
            score += w
            if w > 0:
                restart = True
            else:
                restart = False
            return

def restart_game():
    global player, score, me, restart
    player = (0,y-1)
    score = 0
    restart = False
    board.coords(me, player[0]*Width+Width*player_a/10, player[1]*Width+Width*player_b/10, player[0]*Width+Width*player_c/10, player[1]*Width+Width*player_d/10)

########################################################################################################################
def create_triangle(i, j, action):
    if action == actions[0]:
        return board.create_polygon((i+0.5-triangle_size)*Width, (j+triangle_size)*Width,
                                    (i+0.5+triangle_size)*Width, (j+triangle_size)*Width,
                                    (i+0.5)*Width, j*Width,
                                    fill="white", width=1)
    elif action == actions[1]:
        return board.create_polygon((i+0.5-triangle_size)*Width, (j+1-triangle_size)*Width,
                                    (i+0.5+triangle_size)*Width, (j+1-triangle_size)*Width,
                                    (i+0.5)*Width, (j+1)*Width,
                                    fill="white", width=1)
    elif action == actions[2]:
        return board.create_polygon((i+triangle_size)*Width, (j+0.5-triangle_size)*Width,
                                    (i+triangle_size)*Width, (j+0.5+triangle_size)*Width,
                                    i*Width, (j+0.5)*Width,
                                    fill="white", width=1)
    elif action == actions[3]:
        return board.create_polygon((i+1-triangle_size)*Width, (j+0.5-triangle_size)*Width,
                                    (i+1-triangle_size)*Width, (j+0.5+triangle_size)*Width,
                                    (i+1)*Width, (j+0.5)*Width,
                                    fill="white", width=1)
def render_grid():
    global specials, walls, Width, x, y, player
    for i in range(x):
        for j in range(y):
            board.create_rectangle(i*Width, j*Width, (i+1)*Width, (j+1)*Width, fill="white", width=1) #width=0 ->grid off
            temp = {}
            for action in actions:
                temp[action] = create_triangle(i, j, action)
            cell_scores[(i,j)] = temp
    for (i, j, c, w) in specials:
        board.create_rectangle(i*Width, j*Width, (i+1)*Width, (j+1)*Width, fill=c, width=1)
    for (i, j) in walls:
        board.create_rectangle(i*Width, j*Width, (i+1)*Width, (j+1)*Width, fill="black", width=1)
render_grid()
def set_cell_score(state, action, val):
    global cell_score_min, cell_score_max
    triangle = cell_scores[state][action]
    green_dec = int(min(255, max(0, (val - cell_score_min) * 255.0 / (cell_score_max - cell_score_min))))
    green = hex(green_dec)[2:]
    red = hex(255-green_dec)[2:]
    if len(red) == 1:
        red += "0"
    if len(green) == 1:
        green += "0"
    color = "#" + red + green + "00"
    board.itemconfigure(triangle, fill=color)


def call_up(event):
    try_move(0, -1)
def call_down(event):
    try_move(0, 1)
def call_left(event):
    try_move(-1, 0)
def call_right(event):
    try_move(1, 0)
def has_restarted():
    return restart
master.bind("<Up>", call_up)
master.bind("<Down>", call_down)
master.bind("<Right>", call_right)
master.bind("<Left>", call_left)
me = board.create_rectangle(player[0]*Width+Width*player_a/10, player[1]*Width+Width*player_b/10,
                            player[0]*Width+Width*player_c/10, player[1]*Width+Width*player_d/10, fill="green", width=1, tag="me")
board.grid(row=0, column=0)
def start_game():
    master.mainloop()

