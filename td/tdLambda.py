import random
import numpy as np
import os
parent_directory = os.path.abspath(os.path.join(os.getcwd(), os.pardir))
import sys
sys.path.insert(0, parent_directory)
import grid.gridWorld

gw = grid.gridWorld.Grid()
gw.init_sample_grid_world((3, 5))

q = np.zeros(shape=(3, 5, 4))
e = np.zeros(shape=(3, 5, 4))
actions = ["N", "E", "S", "W"]
g = 0.8
l = 0.7
terminal_states = [[(0, 1), -100], [(0, 2), -100], [(0, 3), -100], [(0, 4), 100]]

for action_number in range(4):
    for ts in terminal_states:
        q[ts[0][0], ts[0][1], action_number] = ts[1]

for i in range(5000):
    s_k = (0, 0)
    alpha = 500 / float(i + 500)
    is_terminal = False
    while True:
        # argmax_a = np.argmax([q[s_k[0], s_k[1], :]])
        policy = random.sample([0, 1, 2, 3], 1)[0]
        a_k = actions[policy]
        s_kk = gw.get_next_state(s_k, a_k)

        r = gw.get_reward(s_k, a_k, s_kk)
        delta = r + g * max(q[s_kk[0], s_kk[1], :]) - q[s_k[0], s_k[1], policy]
        e[s_k[0], s_k[1], policy] += 1
        m, n, a = q.shape
        for x in range(m):
            for y in range(n):
                for action_number in range(a):
                    q[x, y, action_number] += alpha * delta * e[x, y, action_number]
                    e[x, y, action_number] *= g * l
        s_k = s_kk
        for ts in terminal_states:
            if s_k == ts[0]:
                is_terminal = True
        if is_terminal:
            break

m, n, a = q.shape
for x in range(m):
    for y in range(n):
        argmax_a = np.argmax([q[x, y, :]])
        a_k = actions[argmax_a]
        print(x, y, a_k)