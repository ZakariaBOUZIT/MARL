'''
Q-learning with epsilon greedy policy. train.
decay for epsilon and learning rate per episode.
done.
'''
import train_env as World
from icecream import ic
import threading
import time
import random
import pickle
import csv
import numpy as np
log = []
random.seed(0)
learning_rate=1
gama=1
states = []
Q = {}
epsilon=0.1
for i in range(World.x):
    for j in range(World.y):
        states.append((i, j))
actions = World.actions
for state in states:
    temp = {}
    for action in actions:
        temp[action] = 10
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
def max_Q(s):
    q_val = None
    act = None
    for a, q in Q[s].items():
        if q_val is None or (q > q_val):
            q_val = q
            act = a
    return act, q_val
def update_q(s,a,r,gama,learning_rate,max_val):
    current_q = Q[s][a]
    new_q = current_q + learning_rate * (r + gama * max_val - current_q)
    return new_q
def epsilon_greedy(s):
    q_val= None
    act = None
    n=random.random()
    for a, q in Q[s].items():
        if n<epsilon:
            act= np.random.choice(actions)
            q_val= Q[s][act]
            break
        else:
            if q_val is None or (q > q_val):
                act=a
                q_val=q
    return act,q_val
def run():
    global gama
    global learning_rate
    global log
    global epsilon
    time.sleep(1)
    episodes=2000
    epsilon_decay=0.0001
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
            #action, max_q = max_Q(current_state) #for greedy policy
            action, max_q = epsilon_greedy(current_state) #for epsilon greedy policy
            (current_state, action, r, next_state) = do_action(action)
            next_action, max_futur_q = max_Q(next_state) #max action for next state to get max_futur_q
            Q[current_state][action]=update_q(current_state,action,r,gama,learning_rate,max_futur_q)
            World.set_cell_score(current_state, action, Q[current_state][action])
            steps += 1
            score+=r
            if steps%30==0:
                print("step : {} , episode: {}".format(steps,episode))
            if steps>2000:
                break

        World.restart_game()
        log.append({'episode': episode, 'score': score})
        #log.append({'episode': episode, 'score': score, 'steps': steps, 'learning_rate': learning_rate, 'epsilon': 0})
        time.sleep(0.005)

    with open('log.pickle', 'wb') as f:
        pickle.dump(log, f)

    with open('C:/Users/zakar/Desktop/single rl code/Q-learning-gridworld/data/log_qlearning.csv', 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=['episode', 'score'])
        writer.writeheader()
        for episode in log:
            writer.writerow(episode)
    print('Logged')
t = threading.Thread(target=run)
t.daemon = True
t.start()
World.start_game()
