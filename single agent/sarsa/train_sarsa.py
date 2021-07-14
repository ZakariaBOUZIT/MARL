'''
sarsa using epsilon greedy policy.
decay for epsilon and learning rate per episode.
done ?
'''
import train_env as World
from icecream import ic
import numpy as np
import threading
import time
import random
import pickle
import csv
random.seed(0)
log = []
learning_rate=1
gama=1
epsilon=0.1
states = []
Q = {}
for i in range(World.x):
    for j in range(World.y):
        states.append((i, j))
actions = World.actions
for state in states:
    temp = {}
    for action in actions:
        temp[action] = 0
        World.set_cell_score(state, action, temp[action])
    Q[state] = temp
for (i, j, c, w) in World.specials:
    for action in actions:
        Q[(i, j)][action] = w
        World.set_cell_score((i, j), action, w)
def do_action(action):
    s = World.player
    r = -World.score #-1
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
def ep_greedy_action(s):
    if np.random.random()<(1-epsilon):
        action,_=max_Q(s)
    else:
        action=np.random.choice(actions,1)
        action=action[0]
    return action
def max_Q(s):
    q_val = None
    act = None
    for a, q in Q[s].items():
        if q_val is None or (q > q_val):
            q_val = q
            act = a
    return act, q_val
def update_q(current_state,next_state,action,next_action,r,gama,learning_rate):
    current_q = Q[current_state][action]
    next_q= Q[next_state][next_action]
    new_q = current_q + learning_rate * (r + gama * next_q - current_q)
    return new_q
def run():
    global gama
    global learning_rate
    global log
    global epsilon
    time.sleep(1)
    episodes=50
    epsilon_decay=0.001
    t = 1.0
    for episode in range(episodes):
        steps = 0
        score = 0
        learning_rate = pow(t, -0.1)
        t += 1.0
        if epsilon > 0:
            epsilon -= epsilon_decay
            if epsilon < 0:
                epsilon += epsilon_decay
        if episode%50==0:
            print("learning rate : {} in episode {}".format(learning_rate, episode))
            print("epsilon : {} in episode {}".format(epsilon, episode))
        while not World.has_restarted():
            current_state = World.player
            action=ep_greedy_action(current_state)
            (current_state, action, r, next_state) = do_action(action)
            next_action = ep_greedy_action(next_state)
            Q[current_state][action]=update_q(current_state,next_state,action,next_action,r,gama,learning_rate)
            World.set_cell_score(current_state, action, Q[current_state][action])
            steps += 1
            score += r
            if steps%30==0:
                print("step : {} , episode: {}".format(steps,episode))
            if episode < (700):
                time.sleep(0.00000000005)
            if episode > (700):
                time.sleep(0.00005)
                print("Save done **********************************************************")
                with open('Q_sarsa.pickle', 'wb') as f:
                    pickle.dump(Q, f)
                    break
        World.restart_game()
        log.append({'episode': episode, 'score': score, 'steps': steps, 'learning_rate': learning_rate, 'epsilon': epsilon})
        time.sleep(0.0001)

    with open('C:/Users/zakar/Desktop/single rl code/Q-learning-gridworld/data/log_train_sarsa.csv', 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=['episode', 'score', 'steps', 'learning_rate', 'epsilon'])
        writer.writeheader()
        for episode in log:
            writer.writerow(episode)
    print('Logged')
t = threading.Thread(target=run)
t.daemon = True
t.start()
World.start_game()
