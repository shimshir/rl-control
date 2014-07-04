import helper


class Grid():
    def __init__(self, terminal_states=None, transition_model=None, reward_model=None, actions=None):
        self.terminal_states = terminal_states
        self.transition_model = transition_model
        self.reward_model = reward_model
        self.actions = actions
        self.default_reward = -20

    def init_sample_grid_world(self, dimensions=(4, 5)):
        self.terminal_states = [[(0, 1), -100], [(0, 2), -100], [(0, 3), -100], [(0, 4), 100], [(3, 2), -100],
                                [(2, 2), -100]]
        self.transition_model = ModelFunction([])
        self.reward_model = ModelFunction([])
        self.actions = ["N", "E", "S", "W"]
        m, n = dimensions[0], dimensions[1]
        for row in range(m):
            for column in range(n):
                for action in self.actions:
                    if action == "S":
                        if row == m - 1:
                            self.transition_model.add_model(Model((row, column), action, (row, column), 0.8))
                            self.reward_model.add_model(
                                Model((row, column), action, (row, column), self.default_reward))
                        else:
                            self.transition_model.add_model(Model((row, column), action, (row + 1, column), 0.8))
                            self.reward_model.add_model(
                                Model((row, column), action, (row + 1, column), self.default_reward))

                        if column == 0:
                            self.transition_model.add_model(Model((row, column), action, (row, column + 1), 0.2))
                            self.reward_model.add_model(
                                Model((row, column), action, (row, column + 1), self.default_reward))
                        elif column == n - 1:
                            self.transition_model.add_model(Model((row, column), action, (row, column - 1), 0.2))
                            self.reward_model.add_model(
                                Model((row, column), action, (row, column - 1), self.default_reward))
                        else:
                            self.transition_model.add_model(Model((row, column), action, (row, column + 1), 0.1))
                            self.reward_model.add_model(
                                Model((row, column), action, (row, column + 1), self.default_reward))
                            self.transition_model.add_model(Model((row, column), action, (row, column - 1), 0.1))
                            self.reward_model.add_model(
                                Model((row, column), action, (row, column - 1), self.default_reward))
                    elif action == "E":
                        if column == n - 1:
                            self.transition_model.add_model(Model((row, column), action, (row, column), 0.8))
                            self.reward_model.add_model(
                                Model((row, column), action, (row, column), self.default_reward))
                        else:
                            self.transition_model.add_model(Model((row, column), action, (row, column + 1), 0.8))
                            self.reward_model.add_model(
                                Model((row, column), action, (row, column + 1), self.default_reward))
                        if row == 0:
                            self.transition_model.add_model(Model((row, column), action, (row + 1, column), 0.2))
                            self.reward_model.add_model(
                                Model((row, column), action, (row + 1, column), self.default_reward))
                        elif row == m - 1:
                            self.transition_model.add_model(Model((row, column), action, (row - 1, column), 0.2))
                            self.reward_model.add_model(
                                Model((row, column), action, (row - 1, column), self.default_reward))
                        else:
                            self.transition_model.add_model(Model((row, column), action, (row + 1, column), 0.1))
                            self.reward_model.add_model(
                                Model((row, column), action, (row + 1, column), self.default_reward))
                            self.transition_model.add_model(Model((row, column), action, (row - 1, column), 0.1))
                            self.reward_model.add_model(
                                Model((row, column), action, (row - 1, column), self.default_reward))
                    elif action == "N":
                        if row == 0:
                            self.transition_model.add_model(Model((row, column), action, (row, column), 0.8))
                            self.reward_model.add_model(
                                Model((row, column), action, (row, column), self.default_reward))
                        else:
                            self.transition_model.add_model(Model((row, column), action, (row - 1, column), 0.8))
                            self.reward_model.add_model(
                                Model((row, column), action, (row - 1, column), self.default_reward))

                        if column == 0:
                            self.transition_model.add_model(Model((row, column), action, (row, column + 1), 0.2))
                            self.reward_model.add_model(
                                Model((row, column), action, (row, column + 1), self.default_reward))
                        elif column == n - 1:
                            self.transition_model.add_model(Model((row, column), action, (row, column - 1), 0.2))
                            self.reward_model.add_model(
                                Model((row, column), action, (row, column - 1), self.default_reward))
                        else:
                            self.transition_model.add_model(Model((row, column), action, (row, column + 1), 0.1))
                            self.reward_model.add_model(
                                Model((row, column), action, (row, column + 1), self.default_reward))
                            self.transition_model.add_model(Model((row, column), action, (row, column - 1), 0.1))
                            self.reward_model.add_model(
                                Model((row, column), action, (row, column - 1), self.default_reward))
                    else:
                        if column == 0:
                            self.transition_model.add_model(Model((row, column), action, (row, column), 0.8))
                            self.reward_model.add_model(
                                Model((row, column), action, (row, column), self.default_reward))
                        else:
                            self.transition_model.add_model(Model((row, column), action, (row, column - 1), 0.8))
                            self.reward_model.add_model(
                                Model((row, column), action, (row, column - 1), self.default_reward))
                        if row == 0:
                            self.transition_model.add_model(Model((row, column), action, (row + 1, column), 0.2))
                            self.reward_model.add_model(
                                Model((row, column), action, (row + 1, column), self.default_reward))
                        elif row == m - 1:
                            self.transition_model.add_model(Model((row, column), action, (row - 1, column), 0.2))
                            self.reward_model.add_model(
                                Model((row, column), action, (row - 1, column), self.default_reward))
                        else:
                            self.transition_model.add_model(Model((row, column), action, (row + 1, column), 0.1))
                            self.reward_model.add_model(
                                Model((row, column), action, (row + 1, column), self.default_reward))
                            self.transition_model.add_model(Model((row, column), action, (row - 1, column), 0.1))
                            self.reward_model.add_model(
                                Model((row, column), action, (row - 1, column), self.default_reward))

                    # adjust values for terminal states
                    if self.is_terminal_state((row, column)):
                        is_terminal, value = self.is_terminal_state((row, column))
                        for model in self.reward_model.models:
                            if model.s_k == (row, column):
                                model.set_value(value)

    def is_terminal_state(self, state):
        for ts in self.terminal_states:
            if state == ts[0]:
                return True, ts[1]
        return False

    def get_next_state(self, s_k, a_k):
        possible_transitions = [pt for pt in self.transition_model.models if pt.s_k == s_k and pt.a_k == a_k]
        chances = [transition.get_value() for transition in possible_transitions]
        next_state_index = helper.weighted_choice(chances)
        return possible_transitions[next_state_index].s_kk

    def get_reward(self, s_k, a_k, s_kk):
        if self.is_terminal_state(s_k):
            is_terminal, value = self.is_terminal_state(s_k)
            return value
        try:
            reward_value = [reward.get_value() for reward in self.reward_model.models if
                            reward.s_k == s_k and reward.a_k == a_k and reward.s_kk == s_kk][0]
        except IndexError:
            print("Unknown transition: " + str([s_k, a_k, s_kk]))
            return None

        return reward_value


class ModelFunction():
    def __init__(self, models):
        self.models = models

    def get_value(self, s_k, a_k, s_kk):
        for model in self.models:
            if s_k == model.s_k and a_k == model.a_k and s_kk == model.s_kk:
                return model.value
        return 0.0

    def set_value(self, s_k, a_k, s_kk, value):
        for model in self.models:
            if s_k == model.s_k and a_k == model.a_k and s_kk == model.s_kk:
                model.set_value(value)

    def add_model(self, model):
        self.models.append(model)


class Model():
    def __init__(self, s_k, a_k, s_kk, value):
        self.s_k = s_k
        self.a_k = a_k
        self.s_kk = s_kk
        self.value = value

    def get_value(self):
        return self.value

    def set_value(self, value):
        self.value = value

    def __str__(self):
        return str([self.s_k, self.a_k, self.s_kk, self.value])

    def __repr__(self):
        return self.__str__()


# grid = Grid()
# grid.init_sample_grid_world((4, 5))
# grid.get_reward((0, 0), "E", (123, 123))