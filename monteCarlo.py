import random
import numpy as np
import gridWorld
import helper


class MonteCarlo():
    def __init__(self, dimensions=(4, 5)):
        self.gw = gridWorld.Grid()
        self.dimensions = dimensions
        self.gw.init_sample_grid_world(dimensions)
        self.q = np.zeros(shape=(dimensions[0], dimensions[1], 4))
        self.returns = np.zeros(shape=(dimensions[0], dimensions[1], 4, 2))
        self.policy = np.zeros(shape=(dimensions[0], dimensions[1], 4))
        self.policy[:, :, :] = 0.25

    def learn(self):
        s_k = (random.sample(range(self.dimensions[0]), 1)[0], random.sample(range(self.dimensions[1]), 1)[0])
        if self.is_terminal_state(s_k):
            return
        # (a)
        occurrences = []
        while True:
            policy = self.get_behaviour_policy(s_k)
            a_k = self.gw.actions[policy]
            s_kk = self.gw.get_next_state(s_k, a_k)
            occurrences.append([s_k, policy, self.gw.get_reward(s_k, a_k, s_kk)])
            a_k = self.gw.actions[policy]
            s_k = self.gw.get_next_state(s_k, a_k)
            if self.is_terminal_state(s_k):
                occurrences.append([s_k, policy, self.gw.get_reward(s_k, a_k, s_kk)])
                break

        # (b)
        computed_state_actions = []
        for i in range(len(occurrences)):
            if (occurrences[i][0], occurrences[i][1]) in computed_state_actions:
                continue
            for j in np.arange(i, len(occurrences)):
                self.returns[occurrences[i][0][0], occurrences[i][0][1], occurrences[i][1], 0] += occurrences[j][2]

            self.returns[occurrences[i][0][0], occurrences[i][0][1], occurrences[i][1], 1] += 1
            total_R = self.returns[occurrences[i][0][0], occurrences[i][0][1], occurrences[i][1], 0]
            number_of_Rs = self.returns[occurrences[i][0][0], occurrences[i][0][1], occurrences[i][1], 1]
            self.q[occurrences[i][0][0], occurrences[i][0][1], occurrences[i][1]] = total_R / float(number_of_Rs)
            computed_state_actions.append((occurrences[i][0], occurrences[i][1]))

        # (c)
        computed_states = []
        for occurrence in occurrences:
            state = occurrence[0]
            if state in computed_states:
                continue
            opt_action = np.argmax(self.q[state[0], state[1], :])
            for action_number in range(4):
                if action_number == opt_action:
                    self.policy[state[0], state[1], action_number] = 0.7
                else:
                    self.policy[state[0], state[1], action_number] = 0.1
            computed_states.append(state)

    def get_policy(self, state):
        argmax_a = np.argmax(self.q[state[0], state[1], :])
        return self.gw.actions[argmax_a]

    def get_behaviour_policy(self, state):
        weights = []
        for action_number in range(4):
            weights.append(self.policy[state[0], state[1], action_number])
        return helper.weighted_choice(weights)

    def is_terminal_state(self, state):
        for ts in self.gw.terminal_states:
            if state == ts[0]:
                return True, ts[1]
        return False

    @staticmethod
    def is_online():
        return True


if __name__ == "__main__":
    mc = MonteCarlo()
    for it in range(5000):
        mc.learn()
    for row in range(4):
        for col in range(5):
            print(row, col, mc.gw.actions[np.argmax(mc.q[row, col, :])])