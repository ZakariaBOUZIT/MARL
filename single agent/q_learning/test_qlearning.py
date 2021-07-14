'''
Q-learning-test.
'''
import test_env as World
from icecream import ic
import threading
import time
import random
import pickle
random.seed(0)
states = []
actions = World.actions
with open('Q_qlearning.pickle', 'rb') as f:
    Q = pickle.load(f)
def do_action(action):
    s = World.player
    r = -World.score
    if action == actions[0]:
        World.try_move(0, -1)
    elif action == actions[1]:
        World.try_move(0, 1)
    elif action == actions[2]:
        World.try_move(-1, 0)
    elif action == actions[3]:
        World.try_move(1, 0)
    else:
        return
    s2 = World.player
    r += World.score
    return s, action, r, s2
def max_Q(s):
    q_val = None
    act = None
    for a, q in Q[s].items():
        if q_val is None or (q > q_val):
            q_val = q
            act = a
    return act, q_val
########################################################################################################################
def run():
    time.sleep(100)
    episodes=200
    for episode in range(episodes):
        steps = 0
        score = 0
        while not World.has_restarted():
            # greedy policy
            current_state = World.player
            action, max_q = max_Q(current_state)
            (current_state, action, r, next_state) = do_action(action)
            score += r
            World.set_cell_score(current_state, action, Q[current_state][action])
            steps += 1
            time.sleep(0.08)
            print(steps,episode)
        World.restart_game()
        time.sleep(0.000025)

t = threading.Thread(target=run)
t.daemon = True
t.start()
World.start_game()
