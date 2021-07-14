'''
test env.
'''
from tkinter import *
import pickle
import random
'''
with open('walls.pickle', 'rb') as f:
    walls = pickle.load(f)
with open('specials.pickle', 'rb') as f:
    specials = pickle.load(f)
    '''
cell_scores = {}
master = Tk()
triangle_size = 0.001
cell_score_min = -1
cell_score_max = 1
player_a,player_b,player_c,player_d=[2,2,8,8] #agent dim
actions = ["up", "down", "left", "right"]
score = 1
restart = False
walk_reward = -0.04
obs_reward=-10
cell_scores = {}
########################################################################################################################
(x, y) = (29,35)
Width = 20
board = Canvas(master, width=x*Width, height=y*Width)
player_x=14
player_y=34
player=(player_x,player_y)
goal_x=14
goal_y=0

with open('walls.pickle', 'rb') as f:
    walls=pickle.load(f)
specials = [(goal_x, goal_y, "green", 50),]

def try_move(dx, dy):
    global player, x, y, score, walk_reward, me, restart
    if restart == True:
        restart_game()
    new_x = player[0] + dx
    new_y = player[1] + dy
    score += walk_reward
    if (new_x >= 0) and (new_x < x) and (new_y >= 0) and (new_y < y) and not ((new_x, new_y) in walls):
        board.coords(me, new_x*Width+Width*player_a/10, new_y*Width+Width*player_b/10, new_x*Width+Width*player_c/10, new_y*Width+Width*player_d/10)
        player = (new_x, new_y)
    for (i, j, c, w) in specials:
        if new_x == i and new_y == j:
            score -= walk_reward
            score += w
            #need improvement : make "Success just when we get goal"
            if score>0 :
                print("Success! score: ", score)
            else:
                print("Fail! score: ", score)
            restart = True
            return
def restart_game():
    global player, score, me, restart
    player = (14,34)
    score = 1
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

