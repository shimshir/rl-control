import numpy as np
import helper
import random
import math


class Agent:
    def __init__(self, manual_exploration=False, **kwargs):
        self.iteration = 0
        self.e_k = 0
        self.e_kk = 0
        self.de_k = 0
        self.de_kk = 0
        self.alpha = 0
        self.manual_exploration = manual_exploration
        self.exploration_rate = 1
        # TODO: treba ovo fino napraviti
        self.actions = kwargs['actions']
        self.e_bins = kwargs['e_bins']
        self.de_bins = kwargs['de_bins']
        self.plant = kwargs['plant']
        self.time_step = kwargs['time_step']
        self.q = np.zeros((len(self.actions), len(self.e_bins), len(self.de_bins), 2))

    def update_q_table(self, set_point):
        state_indexes_k = helper.get_q_indexes(values=[self.e_k, self.de_k],
                                               bins=[self.e_bins, self.de_bins])
        if not self.manual_exploration:
            self.exploration_rate = 1000 / float(1000 + self.iteration)
        choice = helper.weighted_choice([self.exploration_rate, 1 - self.exploration_rate])
        if choice == 0:
            policy = random.sample(self.actions, 1)[0]
        else:
            argmax_a = np.argmax(self.q[:, state_indexes_k[0], state_indexes_k[1], 0])
            policy = self.actions[argmax_a]

        action_index = helper.get_q_indexes(values=[policy], bins=[self.actions])[0]
        q_k_value = self.q[action_index, state_indexes_k[0], state_indexes_k[1], 0]
        q_k_visited = self.q[action_index, state_indexes_k[0], state_indexes_k[1], 1]

        output = self.plant.get_output(policy)[0, 0]

        self.e_kk = set_point - output
        self.de_kk = (self.e_kk - self.e_k) / self.time_step

        state_indexes_kk = helper.get_q_indexes(values=[self.e_kk, self.de_kk],
                                                bins=[self.e_bins, self.de_bins])

        q_max = max(self.q[:, state_indexes_kk[0], state_indexes_kk[1], 0])

        abs_e_k = math.fabs(self.e_k)
        abs_e_kk = math.fabs(self.e_kk)
        if abs_e_kk < abs_e_k:
            r = 0.5
        else:
            r = 0

        self.alpha = 50 / (50 + q_k_visited)
        if self.iteration % 1000 == 0:
            print(str(self.exploration_rate) + " " + str(self.alpha))

        self.q[action_index, state_indexes_k[0], state_indexes_k[1], 0] = \
            (1 - self.alpha) * q_k_value + self.alpha * (r - abs_e_kk + 0.8 * q_max)

        self.q[action_index, state_indexes_k[0], state_indexes_k[1], 1] = q_k_visited + 1

        self.e_k = self.e_kk
        self.de_k = self.de_kk
        self.iteration += 1

    def get_policy(self, state_vector):
        state_indexes = helper.get_q_indexes(values=state_vector, bins=[self.e_bins, self.de_bins])
        argmax_a = np.argmax(self.q[:, state_indexes[0], state_indexes[1], 0])
        policy = self.actions[argmax_a]
        return policy
