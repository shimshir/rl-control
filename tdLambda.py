import random
import numpy as np
import gridWorld


class TDLambda():
    def __init__(self, dimensions=(4, 5)):
        self.gw = gridWorld.Grid()
        self.dimensions = dimensions
        self.gw.init_sample_grid_world(dimensions)
        self.episodes_run = 0
        self.q = np.zeros(shape=(dimensions[0], dimensions[1], 4))
        self.e = np.zeros(shape=(dimensions[0], dimensions[1], 4))
        self.g = 0.8
        self.l = 0.7
        for ts in self.gw.terminal_states:
            for action_number in range(4):
                self.q[ts[0][0], ts[0][1], action_number] = ts[1]

    def learn(self):
        # s_k = (0, 0)
        s_k = (random.sample(range(self.dimensions[0]), 1)[0], random.sample(range(self.dimensions[1]), 1)[0])
        if self.is_terminal_state(s_k):
            return
        while True:
            alpha = 100 / float(self.episodes_run + 100)
            policy = random.sample([0, 1, 2, 3], 1)[0]
            a_k = self.gw.actions[policy]
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

    def get_policy(self, state):
        argmax_a = np.argmax(self.q[state[0], state[1], :])
        return self.gw.actions[argmax_a]

    def is_terminal_state(self, state):
        for ts in self.gw.terminal_states:
            if state == ts[0]:
                return True, ts[1]
        return False

    @staticmethod
    def is_online():
        return True


if __name__ == "__main__":
    td = TDLambda()
    for i in range(500):
        td.learn()
    for row in range(4):
        for col in range(5):
            print(row, col, td.gw.actions[np.argmax(td.q[row, col, :])])