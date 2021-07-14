from tkinter import *
import  random
master = Tk()
triangle_size = 0.001
cell_score_min = -1
cell_score_max = 1
Width = 10
(x, y) = (6,6)
actions=["up","down","left","right"]
board = Canvas(master, width=x*Width, height=y*Width)
player1 = (1,3)
player2 = (4,3)
score1 = 0
score2 = 0
restart = False
walk_reward = -0.04
positive_reward=5
specials=[]
walls=[]
cell_scores = {}
def create_triangle(i, j, action):
    if action == actions[0]: #up
        return board.create_polygon((i+0.5-triangle_size)*Width, (j+triangle_size)*Width,
                                    (i+0.5+triangle_size)*Width, (j+triangle_size)*Width,
                                    (i+0.5)*Width, j*Width,
                                    fill="white", width=1)
    elif action == actions[1]: #down
        return board.create_polygon((i+0.5-triangle_size)*Width, (j+1-triangle_size)*Width,
                                    (i+0.5+triangle_size)*Width, (j+1-triangle_size)*Width,
                                    (i+0.5)*Width, (j+1)*Width,
                                    fill="white", width=1)
    elif action == actions[2]: #left
        return board.create_polygon((i+triangle_size)*Width, (j+0.5-triangle_size)*Width,
                                    (i+triangle_size)*Width, (j+0.5+triangle_size)*Width,
                                    i*Width, (j+0.5)*Width,
                                    fill="white", width=1)
    elif action == actions[3]: #right
        return board.create_polygon((i+1-triangle_size)*Width, (j+0.5-triangle_size)*Width,
                                    (i+1-triangle_size)*Width, (j+0.5+triangle_size)*Width,
                                    (i+1)*Width, (j+0.5)*Width,
                                    fill="white", width=1)
def render_grid():
    global specials, walls, Width, x, y, player
    for i in range(x):
        for j in range(y):
            board.create_rectangle(i*Width, j*Width, (i+1)*Width, (j+1)*Width, fill="white", width=1)
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
def try_move1(dx, dy):
    global player1, player2, x, y, score1, walk_reward, positive_reward, me1, restart
    new_x = player1[0] + dx
    new_y = player1[1] + dy
    score1 += walk_reward
    if (new_x >= 0) and (new_x < x) and (new_y >= 0) and (new_y < y) and not ((new_x, new_y) in walls):
        board.coords(me1, new_x*Width+Width*2/10, new_y*Width+Width*2/10, new_x*Width+Width*8/10, new_y*Width+Width*8/10)
        player1 = (new_x, new_y)
        if (player2[0] - player1[0] == 1) and (player1[1] == player2[1]):
            print(player1, player2)
            score1-=walk_reward
            score1+=positive_reward

def try_move2(dx, dy):
    global player2, player1, x, y, score2, walk_reward, positive_reward, me2, restart
    new_x = player2[0] + dx
    new_y = player2[1] + dy
    score2 += walk_reward
    if (new_x >= 0) and (new_x < x) and (new_y >= 0) and (new_y < y) and not ((new_x, new_y) in walls):
        board.coords(me2, new_x*Width+Width*2/10, new_y*Width+Width*2/10, new_x*Width+Width*8/10, new_y*Width+Width*8/10)
        player2 = (new_x, new_y)
        if (player2[0] - player1[0] == 1) and (player1[1] == player2[1]):
            print(player1,player2)
            score2-=walk_reward
            score2+=positive_reward





def restart_game():
    global player1, player2, score1, score2 , me1, me2, restart
    player1 = (1,3)
    player2 = (4,3)
    score1 = 0
    score2 = 0
    restart = False
    board.coords(me1, player1[0]*Width+Width*2/10, player1[1]*Width+Width*2/10, player1[0]*Width+Width*8/10, player1[1]*Width+Width*8/10)
    board.coords(me2, player2[0]*Width+Width*2/10,
                 player2[1] * Width + Width * 2 / 10,player2[0] * Width + Width * 8 / 10, player2[1] * Width + Width * 8 / 10)

def has_restarted():
    return restart

me1 = board.create_rectangle(player1[0]*Width+Width*2/10, player1[1]*Width+Width*2/10,
                            player1[0]*Width+Width*8/10, player1[1]*Width+Width*8/10, fill="orange", width=1, tag="me")
me2 = board.create_rectangle(player2[0]*Width+Width*2/10, player2[1]*Width+Width*2/10,
                            player2[0]*Width+Width*8/10, player2[1]*Width+Width*8/10, fill="blue", width=1, tag="me")


board.grid(row=0, column=0)


def start_game():
    master.mainloop()
