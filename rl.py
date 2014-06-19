import numpy as np
import helper
import random
import math


class Agent:
    def __init__(self, **kwargs):
        self.iteration = 0
        self.e_k = 0
        self.e_kk = 0
        self.de_k = 0
        self.de_kk = 0
        self.alpha = 0
        # TODO: treba ovo fino napraviti
        self.e_bins = kwargs['e_bins']
        self.de_bins = kwargs['de_bins']
        self.plant = kwargs['plant']
        self.time_step = kwargs['time_step']
        self.q = np.zeros((2, len(self.e_bins), len(self.de_bins), 2))

    def update_q_table(self, set_point_s):
        rangelo = self.iteration / 1000
        indexes_k = helper.get_q_indexes(self.e_k, self.de_k, self.e_bins, self.de_bins)

        temp = random.sample(range(rangelo + 1), 1)[0]
        if temp == 0:
            policy_s = random.sample([-1, 1], 1)[0]
        else:
            if self.q[0, indexes_k[0], indexes_k[1], 0] >= self.q[1, indexes_k[0], indexes_k[1], 0]:
                policy_s = -1
            else:
                policy_s = 1

        q_k_value = self.q[(policy_s + 1) / 2, indexes_k[0], indexes_k[1], 0]
        q_k_visited = self.q[(policy_s + 1) / 2, indexes_k[0], indexes_k[1], 1]

        output = self.plant.get_output(policy_s)[0, 0]

        self.e_kk = set_point_s - output
        self.de_kk = (self.e_kk - self.e_k) / self.time_step

        indexes_kk = helper.get_q_indexes(self.e_kk, self.de_kk, self.e_bins, self.de_bins)

        q_max = max([self.q[0, indexes_kk[0], indexes_kk[1], 0], self.q[1, indexes_kk[0], indexes_kk[1], 0]])
        abs_e_kk = math.fabs(self.e_kk)
        if abs_e_kk < math.fabs(self.e_k):
            r = 3
        else:
            r = 0

        self.alpha = 50 / (50 + q_k_visited)
        self.q[(policy_s + 1) / 2, indexes_k[0], indexes_k[1], 0] = (1 - self.alpha) * q_k_value + self.alpha * (
            r - abs_e_kk + 0.8 * q_max)

        self.q[(policy_s + 1) / 2, indexes_k[0], indexes_k[1], 1] = q_k_visited + 1

        self.e_k = self.e_kk
        self.de_k = self.de_kk
        self.iteration += 1

    def get_policy(self, state_vector):
        indexes = helper.get_q_indexes(state_vector[0], state_vector[1], self.e_bins, self.de_bins)
        if self.q[0, indexes[0], indexes[1], 0] >= self.q[1, indexes[0], indexes[1], 0]:
            policy = -1
        else:
            policy = 1
        return policy
