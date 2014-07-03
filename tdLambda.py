import random
import numpy as np
import gridWorld


class TDLambda():
    def __init__(self, dimensions=(3, 5)):
        self.gw = gridWorld.Grid()
        self.gw.init_sample_grid_world(dimensions)
        self.episodes_run = 0
        self.q = np.zeros(shape=(dimensions[0], dimensions[1], 4))
        self.e = np.zeros(shape=(dimensions[0], dimensions[1], 4))
        self.actions = ["N", "E", "S", "W"]
        self.g = 0.8
        self.l = 0.7
        self.terminal_states = [[(0, 1), -100], [(0, 2), -100], [(0, 3), -100], [(0, 4), 100], [(3, 2), -100]]
        for ts in self.terminal_states:
            for action_number in range(4):
                self.q[ts[0][0], ts[0][1], action_number] = ts[1]

    def run_episode(self):
        s_k = (0, 0)
        while True:
            alpha = 50 / float(self.episodes_run + 50)
            policy = random.sample([0, 1, 2, 3], 1)[0]
            a_k = self.actions[policy]
            s_kk = self.gw.get_next_state(s_k, a_k)

            r = self.gw.get_reward(s_k, a_k, s_kk)
            delta = r + self.g * max(self.q[s_kk[0], s_kk[1], :]) - self.q[s_k[0], s_k[1], policy]
            self.e[s_k[0], s_k[1], policy] += 1
            m, n, a = self.q.shape
            for x in range(m):
                for y in range(n):
                    for action_number in range(a):
                        self.q[x, y, action_number] += alpha * delta * self.e[x, y, action_number]
                        self.e[x, y, action_number] *= self.g * self.l
            s_k = s_kk
            if self.is_terminal_state(s_k):
                break
        self.episodes_run += 1

    def is_terminal_state(self, state):
        for ts in self.terminal_states:
            if state == ts[0]:
                return True, ts[1]
        return False


if __name__ == "__main__":
    td = TDLambda()
    for k in range(500):
        td.run_episode()

    mc, nc, ac = td.q.shape
    for xc in range(mc):
        for yc in range(nc):
            argmax_a = np.argmax(td.q[xc, yc, :])
            ac = td.actions[argmax_a]
            print(xc, yc, ac)