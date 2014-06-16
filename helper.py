import numpy


def get_q_indexes(policy, e, de, e_bins):
    if policy > 0:
        policy_index = 1
    else:
        policy_index = 0

    if e <= e_bins[0]:
        e_index = 0
    elif e >= e_bins[-1]:
        e_index = len(e_bins) - 1
    else:
        e_index = numpy.digitize([e], e_bins)[0] - 1

    if de <= -1:
        de_index = 0
    elif abs(de) < 1:
        de_index = 1
    elif de >= 1:
        de_index = 2

    return [policy_index, e_index, de_index]