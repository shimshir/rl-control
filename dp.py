import numpy as np
import gridWorld


class DP():
    def __init__(self, dimensions=(4, 5)):
        self.gw = gridWorld.Grid()
        self.dimensions = dimensions
        self.gw.init_sample_grid_world(dimensions)
        self.v = np.zeros(shape=(dimensions[0], dimensions[1]))
        self.g = 0.8

    def learn(self):
        while True:
            delta = 0
            for row_k in range(self.dimensions[0]):
                for col_k in range(self.dimensions[1]):
                    v = self.v[row_k, col_k]
                    temp_sums = [0, 0, 0, 0]
                    for action_number in range(4):
                        for row_kk in range(self.dimensions[0]):
                            for col_kk in range(self.dimensions[1]):
                                prob = self.gw.transition_model.get_value((row_k, col_k),
                                                                          self.gw.actions[action_number],
                                                                          (row_kk, col_kk))
                                r = self.gw.reward_model.get_value((row_k, col_k), self.gw.actions[action_number],
                                                                   (row_kk, col_kk))
                                disc_v = self.g * self.v[row_kk, col_kk]
                                temp_sums[action_number] += prob * (r + disc_v)
                    if self.gw.is_terminal_state((row_k, col_k)):
                        is_terminal, value = self.gw.is_terminal_state((row_k, col_k))
                        self.v[row_k, col_k] = value
                    else:
                        self.v[row_k, col_k] = max(temp_sums)
                    delta = max([delta, abs(v - self.v[row_k, col_k])])
            if delta < 0.0001:
                break

    def get_policy(self, state):
        row_k = state[0]
        col_k = state[1]
        temp_sums = [0, 0, 0, 0]
        for action_number in range(4):
            for row_kk in range(self.dimensions[0]):
                for col_kk in range(self.dimensions[1]):
                    prob = self.gw.transition_model.get_value((row_k, col_k),
                                                              self.gw.actions[action_number],
                                                              (row_kk, col_kk))
                    r = self.gw.reward_model.get_value((row_k, col_k), self.gw.actions[action_number],
                                                       (row_kk, col_kk))
                    disc_v = self.g * self.v[row_kk, col_kk]
                    temp_sums[action_number] += prob * (r + disc_v)
        return self.gw.actions[np.argmax(temp_sums)]

    @staticmethod
    def is_online():
        return False

if __name__ == "__main__":
    dp = DP()
    dp.learn()
    for row in range(4):
        for col in range(5):
            print(row, col, dp.v[row, col])
