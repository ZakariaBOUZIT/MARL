'''
JAL q learning. n=2.
'''
import env as World
from icecream import ic
import threading
import time
import random
import pickle

random.seed(0)
learning_rate = 1
gama = 0.3
states = []
Q = {}

# get states
for i in range(World.x):
    for j in range(World.y):
        states.append((i, j))

# initialize Q table.
actions=World.actions
for state in states:
    temp = {}
    for action in actions:
        temp[action] = 0 #Q[state]: {'down': 0.1, 'left': 0.1, 'right': 0.1, 'up': 0.1}
        World.set_cell_score(state, action, temp[action])
    Q[state] = temp
Q1={'1':Q,'2':Q, '3':Q,'4':Q} #{'1': {(0, 0): {'up': 0, 'down': 0, 'left': 0, 'right': 0}, (0, 1): {'up': 0, 'down': 0, 'left': 0, 'right': 0}, (0, 2): {'up': 0, 'down': 0, 'left': 0, 'right': 0}, (0, 3): {'up': 0, 'down': 0, 'left': 0, 'right': 0}, (0, 4): {'up': 0, 'down': 0, 'left': 0, 'right': 0}, (0, 5): {'up': 0, 'down': 0, 'left': 0, 'right': 0}, (0, 6): {'up': 0, 'down': 0, 'left': 0, 'right': 0}, (1, 0): {'up': 0, 'down': 0, 'left': 0, 'right': 0}, (1, 1): {'up': 0, 'down': 0, 'left': 0, 'right': 0}, (1, 2): {'up': 0, 'down': 0, 'left': 0, 'right': 0}, (1, 3): {'up': 0, 'down': 0, 'left': 0, 'right': 0}, (1, 4): {'up': 0, 'down': 0, 'left': 0, 'right': 0}, (1, 5): {'up': 0, 'down': 0, 'left': 0, 'right': 0}, (1, 6): {'up': 0, 'down': 0, 'left': 0, 'right': 0}, (2, 0): {'up': 0, 'down': 0, 'left': 0, 'right': 0}, (2, 1): {'up': 0, 'down': 0, 'left': 0, 'right': 0}, (2, 2): {'up': 0, 'down': 0, 'left': 0, 'right': 0}, (2, 3): {'up': 0, 'down': 0, 'left': 0, 'right': 0}, (2, 4): {'up': 0, 'down': 0, 'left': 0, 'right': 0}, (2, 5): {'up': 0, 'down': 0, 'left': 0, 'right': 0}, (2, 6): {'up': 0, 'down': 0, 'left': 0, 'right': 0}, (3, 0): {'up': 0, 'down': 0, 'left': 0, 'right': 0}, (3, 1): {'up': 0, 'down': 0, 'left': 0, 'right': 0}, (3, 2): {'up': 0, 'down': 0, 'left': 0, 'right': 0}, (3, 3): {'up': 0, 'down': 0, 'left': 0, 'right': 0}, (3, 4): {'up': 0, 'down': 0, 'left': 0, 'right': 0}, (3, 5): {'up': 0, 'down': 0, 'left': 0, 'right': 0}, (3, 6): {'up': 0, 'down': 0, 'left': 0, 'right': 0}, (4, 0): {'up': 0, 'down': 0, 'left': 0, 'right': 0}, (4, 1): {'up': 0, 'down': 0, 'left': 0, 'right': 0}, (4, 2): {'up': 0, 'down': 0, 'left': 0, 'right': 0}, (4, 3): {'up': 0, 'down': 0, 'left': 0, 'right': 0}, (4, 4): {'up': 0, 'down': 0, 'left': 0, 'right': 0}, (4, 5): {'up': 0, 'down': 0, 'left': 0, 'right': 0}, (4, 6): {'up': 0, 'down': 0, 'left': 0, 'right': 0}, (5, 0): {'up': 0, 'down': 0, 'left': 0, 'right': 0}, (5, 1): {'up': 0, 'down': 0, 'left': 0, 'right': 0}, (5, 2): {'up': 0, 'down': 0, 'left': 0, 'right': 0}, (5, 3): {'up': 0, 'down': 0, 'left': 0, 'right': 0}, (5, 4): {'up': 0, 'down': 0, 'left': 0, 'right': 0}, (5, 5): {'up': 0, 'down': 0, 'left': 0, 'right': 0}, (5, 6): {'up': 0, 'down': 0, 'left': 0, 'right': 0}, (6, 0): {'up': 0, 'down': 0, 'left': 0, 'right': 0}, (6, 1): {'up': 0, 'down': 0, 'left': 0, 'right': 0}, (6, 2): {'up': 0, 'down': 0, 'left': 0, 'right': 0}, (6, 3): {'up': 0, 'down': 0, 'left': 0, 'right': 0}, (6, 4): {'up': 0, 'down': 0, 'left': 0, 'right': 0}, (6, 5): {'up': 0, 'down': 0, 'left': 0, 'right': 0}, (6, 6): {'up': 0, 'down': 0, 'left': 0, 'right': 0}}, '2': {(0, 0): {'up': 0, 'down': 0, 'left': 0, 'right': 0}, (0, 1): {'up': 0, 'down': 0, 'left': 0, 'right': 0}, (0, 2): {'up': 0, 'down': 0, 'left': 0, 'right': 0}, (0, 3): {'up': 0, 'down': 0, 'left': 0, 'right': 0}, (0, 4): {'up': 0, 'down': 0, 'left': 0, 'right': 0}, (0, 5): {'up': 0, 'down': 0, 'left': 0, 'right': 0}, (0, 6): {'up': 0, 'down': 0, 'left': 0, 'right': 0}, (1, 0): {'up': 0, 'down': 0, 'left': 0, 'right': 0}, (1, 1): {'up': 0, 'down': 0, 'left': 0, 'right': 0}, (1, 2): {'up': 0, 'down': 0, 'left': 0, 'right': 0}, (1, 3): {'up': 0, 'down': 0, 'left': 0, 'right': 0}, (1, 4): {'up': 0, 'down': 0, 'left': 0, 'right': 0}, (1, 5): {'up': 0, 'down': 0, 'left': 0, 'right': 0}, (1, 6): {'up': 0, 'down': 0, 'left': 0, 'right': 0}, (2, 0): {'up': 0, 'down': 0, 'left': 0, 'right': 0}, (2, 1): {'up': 0, 'down': 0, 'left': 0, 'right': 0}, (2, 2): {'up': 0, 'down': 0, 'left': 0, 'right': 0}, (2, 3): {'up': 0, 'down': 0, 'left': 0, 'right': 0}, (2, 4): {'up': 0, 'down': 0, 'left': 0, 'right': 0}, (2, 5): {'up': 0, 'down': 0, 'left': 0, 'right': 0}, (2, 6): {'up': 0, 'down': 0, 'left': 0, 'right': 0}, (3, 0): {'up': 0, 'down': 0, 'left': 0, 'right': 0}, (3, 1): {'up': 0, 'down': 0, 'left': 0, 'right': 0}, (3, 2): {'up': 0, 'down': 0, 'left': 0, 'right': 0}, (3, 3): {'up': 0, 'down': 0, 'left': 0, 'right': 0}, (3, 4): {'up': 0, 'down': 0, 'left': 0, 'right': 0}, (3, 5): {'up': 0, 'down': 0, 'left': 0, 'right': 0}, (3, 6): {'up': 0, 'down': 0, 'left': 0, 'right': 0}, (4, 0): {'up': 0, 'down': 0, 'left': 0, 'right': 0}, (4, 1): {'up': 0, 'down': 0, 'left': 0, 'right': 0}, (4, 2): {'up': 0, 'down': 0, 'left': 0, 'right': 0}, (4, 3): {'up': 0, 'down': 0, 'left': 0, 'right': 0}, (4, 4): {'up': 0, 'down': 0, 'left': 0, 'right': 0}, (4, 5): {'up': 0, 'down': 0, 'left': 0, 'right': 0}, (4, 6): {'up': 0, 'down': 0, 'left': 0, 'right': 0}, (5, 0): {'up': 0, 'down': 0, 'left': 0, 'right': 0}, (5, 1): {'up': 0, 'down': 0, 'left': 0, 'right': 0}, (5, 2): {'up': 0, 'down': 0, 'left': 0, 'right': 0}, (5, 3): {'up': 0, 'down': 0, 'left': 0, 'right': 0}, (5, 4): {'up': 0, 'down': 0, 'left': 0, 'right': 0}, (5, 5): {'up': 0, 'down': 0, 'left': 0, 'right': 0}, (5, 6): {'up': 0, 'down': 0, 'left': 0, 'right': 0}, (6, 0): {'up': 0, 'down': 0, 'left': 0, 'right': 0}, (6, 1): {'up': 0, 'down': 0, 'left': 0, 'right': 0}, (6, 2): {'up': 0, 'down': 0, 'left': 0, 'right': 0}, (6, 3): {'up': 0, 'down': 0, 'left': 0, 'right': 0}, (6, 4): {'up': 0, 'down': 0, 'left': 0, 'right': 0}, (6, 5): {'up': 0, 'down': 0, 'left': 0, 'right': 0}, (6, 6): {'up': 0, 'down': 0, 'left': 0, 'right': 0}}, '3': {(0, 0): {'up': 0, 'down': 0, 'left': 0, 'right': 0}, (0, 1): {'up': 0, 'down': 0, 'left': 0, 'right': 0}, (0, 2): {'up': 0, 'down': 0, 'left': 0, 'right': 0}, (0, 3): {'up': 0, 'down': 0, 'left': 0, 'right': 0}, (0, 4): {'up': 0, 'down': 0, 'left': 0, 'right': 0}, (0, 5): {'up': 0, 'down': 0, 'left': 0, 'right': 0}, (0, 6): {'up': 0, 'down': 0, 'left': 0, 'right': 0}, (1, 0): {'up': 0, 'down': 0, 'left': 0, 'right': 0}, (1, 1): {'up': 0, 'down': 0, 'left': 0, 'right': 0}, (1, 2): {'up': 0, 'down': 0, 'left': 0, 'right': 0}, (1, 3): {'up': 0, 'down': 0, 'left': 0, 'right': 0}, (1, 4): {'up': 0, 'down': 0, 'left': 0, 'right': 0}, (1, 5): {'up': 0, 'down': 0, 'left': 0, 'right': 0}, (1, 6): {'up': 0, 'down': 0, 'left': 0, 'right': 0}, (2, 0): {'up': 0, 'down': 0, 'left': 0, 'right': 0}, (2, 1): {'up': 0, 'down': 0, 'left': 0, 'right': 0}, (2, 2): {'up': 0, 'down': 0, 'left': 0, 'right': 0}, (2, 3): {'up': 0, 'down': 0, 'left': 0, 'right': 0}, (2, 4): {'up': 0, 'down': 0, 'left': 0, 'right': 0}, (2, 5): {'up': 0, 'down': 0, 'left': 0, 'right': 0}, (2, 6): {'up': 0, 'down': 0, 'left': 0, 'right': 0}, (3, 0): {'up': 0, 'down': 0, 'left': 0, 'right': 0}, (3, 1): {'up': 0, 'down': 0, 'left': 0, 'right': 0}, (3, 2): {'up': 0, 'down': 0, 'left': 0, 'right': 0}, (3, 3): {'up': 0, 'down': 0, 'left': 0, 'right': 0}, (3, 4): {'up': 0, 'down': 0, 'left': 0, 'right': 0}, (3, 5): {'up': 0, 'down': 0, 'left': 0, 'right': 0}, (3, 6): {'up': 0, 'down': 0, 'left': 0, 'right': 0}, (4, 0): {'up': 0, 'down': 0, 'left': 0, 'right': 0}, (4, 1): {'up': 0, 'down': 0, 'left': 0, 'right': 0}, (4, 2): {'up': 0, 'down': 0, 'left': 0, 'right': 0}, (4, 3): {'up': 0, 'down': 0, 'left': 0, 'right': 0}, (4, 4): {'up': 0, 'down': 0, 'left': 0, 'right': 0}, (4, 5): {'up': 0, 'down': 0, 'left': 0, 'right': 0}, (4, 6): {'up': 0, 'down': 0, 'left': 0, 'right': 0}, (5, 0): {'up': 0, 'down': 0, 'left': 0, 'right': 0}, (5, 1): {'up': 0, 'down': 0, 'left': 0, 'right': 0}, (5, 2): {'up': 0, 'down': 0, 'left': 0, 'right': 0}, (5, 3): {'up': 0, 'down': 0, 'left': 0, 'right': 0}, (5, 4): {'up': 0, 'down': 0, 'left': 0, 'right': 0}, (5, 5): {'up': 0, 'down': 0, 'left': 0, 'right': 0}, (5, 6): {'up': 0, 'down': 0, 'left': 0, 'right': 0}, (6, 0): {'up': 0, 'down': 0, 'left': 0, 'right': 0}, (6, 1): {'up': 0, 'down': 0, 'left': 0, 'right': 0}, (6, 2): {'up': 0, 'down': 0, 'left': 0, 'right': 0}, (6, 3): {'up': 0, 'down': 0, 'left': 0, 'right': 0}, (6, 4): {'up': 0, 'down': 0, 'left': 0, 'right': 0}, (6, 5): {'up': 0, 'down': 0, 'left': 0, 'right': 0}, (6, 6): {'up': 0, 'down': 0, 'left': 0, 'right': 0}}, '4': {(0, 0): {'up': 0, 'down': 0, 'left': 0, 'right': 0}, (0, 1): {'up': 0, 'down': 0, 'left': 0, 'right': 0}, (0, 2): {'up': 0, 'down': 0, 'left': 0, 'right': 0}, (0, 3): {'up': 0, 'down': 0, 'left': 0, 'right': 0}, (0, 4): {'up': 0, 'down': 0, 'left': 0, 'right': 0}, (0, 5): {'up': 0, 'down': 0, 'left': 0, 'right': 0}, (0, 6): {'up': 0, 'down': 0, 'left': 0, 'right': 0}, (1, 0): {'up': 0, 'down': 0, 'left': 0, 'right': 0}, (1, 1): {'up': 0, 'down': 0, 'left': 0, 'right': 0}, (1, 2): {'up': 0, 'down': 0, 'left': 0, 'right': 0}, (1, 3): {'up': 0, 'down': 0, 'left': 0, 'right': 0}, (1, 4): {'up': 0, 'down': 0, 'left': 0, 'right': 0}, (1, 5): {'up': 0, 'down': 0, 'left': 0, 'right': 0}, (1, 6): {'up': 0, 'down': 0, 'left': 0, 'right': 0}, (2, 0): {'up': 0, 'down': 0, 'left': 0, 'right': 0}, (2, 1): {'up': 0, 'down': 0, 'left': 0, 'right': 0}, (2, 2): {'up': 0, 'down': 0, 'left': 0, 'right': 0}, (2, 3): {'up': 0, 'down': 0, 'left': 0, 'right': 0}, (2, 4): {'up': 0, 'down': 0, 'left': 0, 'right': 0}, (2, 5): {'up': 0, 'down': 0, 'left': 0, 'right': 0}, (2, 6): {'up': 0, 'down': 0, 'left': 0, 'right': 0}, (3, 0): {'up': 0, 'down': 0, 'left': 0, 'right': 0}, (3, 1): {'up': 0, 'down': 0, 'left': 0, 'right': 0}, (3, 2): {'up': 0, 'down': 0, 'left': 0, 'right': 0}, (3, 3): {'up': 0, 'down': 0, 'left': 0, 'right': 0}, (3, 4): {'up': 0, 'down': 0, 'left': 0, 'right': 0}, (3, 5): {'up': 0, 'down': 0, 'left': 0, 'right': 0}, (3, 6): {'up': 0, 'down': 0, 'left': 0, 'right': 0}, (4, 0): {'up': 0, 'down': 0, 'left': 0, 'right': 0}, (4, 1): {'up': 0, 'down': 0, 'left': 0, 'right': 0}, (4, 2): {'up': 0, 'down': 0, 'left': 0, 'right': 0}, (4, 3): {'up': 0, 'down': 0, 'left': 0, 'right': 0}, (4, 4): {'up': 0, 'down': 0, 'left': 0, 'right': 0}, (4, 5): {'up': 0, 'down': 0, 'left': 0, 'right': 0}, (4, 6): {'up': 0, 'down': 0, 'left': 0, 'right': 0}, (5, 0): {'up': 0, 'down': 0, 'left': 0, 'right': 0}, (5, 1): {'up': 0, 'down': 0, 'left': 0, 'right': 0}, (5, 2): {'up': 0, 'down': 0, 'left': 0, 'right': 0}, (5, 3): {'up': 0, 'down': 0, 'left': 0, 'right': 0}, (5, 4): {'up': 0, 'down': 0, 'left': 0, 'right': 0}, (5, 5): {'up': 0, 'down': 0, 'left': 0, 'right': 0}, (5, 6): {'up': 0, 'down': 0, 'left': 0, 'right': 0}, (6, 0): {'up': 0, 'down': 0, 'left': 0, 'right': 0}, (6, 1): {'up': 0, 'down': 0, 'left': 0, 'right': 0}, (6, 2): {'up': 0, 'down': 0, 'left': 0, 'right': 0}, (6, 3): {'up': 0, 'down': 0, 'left': 0, 'right': 0}, (6, 4): {'up': 0, 'down': 0, 'left': 0, 'right': 0}, (6, 5): {'up': 0, 'down': 0, 'left': 0, 'right': 0}, (6, 6): {'up': 0, 'down': 0, 'left': 0, 'right': 0}}}


# set reward for specials
for (i, j, c, w) in World.specials:
    for action in actions:
        #Q[(i, j)][action] = w
        World.set_cell_score((i, j), action, w)


def do_action1(action):
    s = World.player1
    r = 0
    if action == actions[0]:
        World.try_move1(0, -1)
    elif action == actions[1]:
        World.try_move1(0, 1)
    elif action == actions[2]:
        World.try_move1(-1, 0)
    elif action == actions[3]:
        World.try_move1(1, 0)
    else:
        return
    s2 = World.player1
    r += World.score1
    return s, action, r, s2

def do_action2(action):
    s = World.player2
    r = 0
    if action == actions[0]:
        World.try_move2(0, -1)
    elif action == actions[1]:
        World.try_move2(0, 1)
    elif action == actions[2]:
        World.try_move2(-1, 0)
    elif action == actions[3]:
        World.try_move2(1, 0)
    else:
        return
    s2 = World.player2
    r += World.score2
    return s, action, r, s2


def max_Q(s,n):
    q_val = None
    act = None
    a_subset=Q1[n][s]
    for a, q in a_subset.items():
        if q_val is None or (q > q_val):
            q_val = q
            act = a
    return act, q_val


def update_q(s, a, r, gama, learning_rate, max_val):
    current_q = Q[s][a]
    new_q = current_q + learning_rate * (r + gama * max_val - current_q)
    return new_q


def run():
    global gama
    global learning_rate
    global log
    time.sleep(1)
    episodes = 300
    t=0
    for episode in range(episodes):
        steps = 0
        score1 = 0
        score2 = 0
        while not World.has_restarted():
            # Pick the right action
            current_state1 = World.player1
            current_state2 = World.player2
            if steps == 0:
                #choose random action from 1,2,3,4 ; i chooses 1
                n1="1"
                action1,max_q1=max_Q(current_state1,n1)
                if action1=='up':
                    n="1"
                if action1=='down':
                    n="2"
                if action1=='left':
                    n="3"
                if action1=='right':
                    n="4"
                #choose action2 according to action1
                n2=n
                action2, max_q2 = max_Q(current_state2, n2)

                (current_state1, action1, r1, next_state1) = do_action1(action1)
                score1 += r1
                (current_state2, action2, r2, next_state2) = do_action2(action2)
                score2 += r2

                next_action1, max_futur_q1 = max_Q(next_state1,n2)  # "n" or "1" idk it's just a guess !!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                new_Q1 = update_q(current_state1, action1, r1, gama, learning_rate, max_futur_q1)
                Q1[n2][current_state1][action1] = new_Q1
                World.set_cell_score(current_state1, action1, new_Q1)

                next_action2, max_futur_q2 = max_Q(next_state2,n1)  # idk it's just a guess !!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                new_Q2 = update_q(current_state2, action2, r2, gama, learning_rate, max_futur_q2)
                Q1[n1][current_state2][action2] = new_Q2
                World.set_cell_score(current_state2, action2, new_Q2)


            else: #others steps
                if action2=='up':
                    n1="1"
                if action2=='down':
                    n1="2"
                if action2=='left':
                    n1="3"
                if action2=='right':
                    n1="4"
                action1, max_q1 = max_Q(current_state1, n1)

                if action1=='up':
                    n2="1"
                if action1=='down':
                    n2="2"
                if action1=='left':
                    n2="3"
                if action1=='right':
                    n2="4"
                action2, max_q2 = max_Q(current_state2, n2)

                (current_state1, action1, r1, next_state1) = do_action1(action1)
                score1 += r1
                (current_state2, action2, r2, next_state2) = do_action2(action2)
                score2 += r2

                next_action1, max_futur_q1 = max_Q(next_state1,n2)  # "n1" or "n2" ?idk it's just a guess !!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                new_Q1 = update_q(current_state1, action1, r1, gama, learning_rate, max_futur_q1)
                Q1[n2][current_state1][action1] = new_Q1
                World.set_cell_score(current_state1, action1, new_Q1)

                next_action2, max_futur_q2 = max_Q(next_state2,n1)  # "n1" or "n2" ?idk it's just a guess !!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                new_Q2 = update_q(current_state2, action2, r2, gama, learning_rate, max_futur_q2)
                Q1[n1][current_state2][action2] = new_Q2
                World.set_cell_score(current_state2, action2, new_Q2)

            t += 1.0
            if steps>200:
                break
            steps += 1
            # Update the learning rate
            learning_rate = pow(t, -0.1)
            # time.sleep(0.0000000005)
            ic(episode)
            if episode < (5):
                time.sleep(0.0001)
            else:
                time.sleep(0.1)

        World.restart_game()
        print('restart')
        time.sleep(0.0001)



t = threading.Thread(target=run)
t.daemon = True
t.start()
World.start_game()
