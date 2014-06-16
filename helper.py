import numpy


def get_q_indexes(policy, x, dx, x_bins):
    if policy > 0:
        policy_index = 1
    else:
        policy_index = 0

    if x <= x_bins[0]:
        x_index = 0
    elif x >= x_bins[-1]:
        x_index = len(x_bins) - 1
    else:
        x_index = numpy.digitize([x], x_bins)[0] - 1

    knee_point = 0.75

    if dx <= -knee_point:
        dx_index = 0
    elif abs(dx) < knee_point:
        dx_index = 1
    elif dx >= knee_point:
        dx_index = 2

    return [policy_index, x_index, dx_index]