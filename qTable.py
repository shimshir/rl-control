import numpy as np
from matplotlib import pyplot as plt
from random import sample
import helper
import random
import time
import math
# noinspection PyCallingNonCallable
A = np.matrix([[0.98991884, -0.07855921],
               [0.00198993, 0.99992131]])

# noinspection PyCallingNonCallable
B = np.matrix([[1.98992813e-03],
               [1.99328853e-06]])

# noinspection PyCallingNonCallable
C = np.matrix([[0., 39.4784176]])

time_step = 1 / float(1200)

u = []

# Generating input signal

# for k00 in range(50):
#     u.append(k00 * (0.5 / 50))
#
# for k0 in range(617):
#     u.append(0.5)
#
# for k01 in range(50):
#     u.append((-0.5 / 50) * k01 + 0.5)
#
# for k1 in range(616):
#     u.append(0)
#
# for k12 in range(50):
#     u.append((-0.5 / 50) * k12)
#
# for k2 in range(567):
#     u.append(-0.5)
#
# for k22 in range(50):
#     u.append((0.5 / 50) * k22 - 0.5)

for k0 in range(667):
    u.append(0.5)

for k1 in range(666):
    u.append(0)

for k2 in range(667):
    u.append(-0.5)

# u = []
# for kaka in range(2000):
# u.append(math.sin(kaka * time_step * math.pi / 2))

e_bins = np.linspace(-2, 2, 100)
de_bins = np.linspace(-4, 4, 5)

Q = np.zeros((2, len(e_bins), len(de_bins)))
# noinspection PyCallingNonCallable
x_k = np.matrix([[0],
                 [0]])
y_k = (C * x_k)[0, 0]
set_point_k = u[0]
e_k = set_point_k - y_k
de_k = abs(random.gauss(0, 0.02))
timeo = time.time()
for k in range(1000000):
    rangelo = k / 10000
    alpha = 100000 / float(100000 + k)
    if k % 10000 == 0:
        # noinspection PyCallingNonCallable
        x_k = x_k + np.matrix([[random.gauss(0, 0.01)],
                               [random.gauss(0, 0.01)]])
        y_k = (C * x_k)[0, 0]
        set_point_k = u[0]
        e_k = set_point_k - y_k
        de_k = 0
        print(str(rangelo) + " " + str(alpha) + " " + str(time.time() - timeo))
        timeo = time.time()

    temp = sample(range(rangelo + 1), 1)[0]
    if temp == 0:
        policy = sample([-1, 1], 1)[0]
    else:
        indexes_0 = helper.get_q_indexes(-1, e_k, de_k, e_bins, de_bins)
        indexes_1 = helper.get_q_indexes(1, e_k, de_k, e_bins, de_bins)
        if Q[indexes_0[0], indexes_0[1], indexes_0[2]] >= Q[indexes_1[0], indexes_1[1], indexes_1[2]]:
            policy = -1
        else:
            policy = 1

    indexes_k = helper.get_q_indexes(policy, e_k, de_k, e_bins, de_bins)

    Qk = Q[indexes_k[0], indexes_k[1], indexes_k[2]]

    x_kk = A * x_k + B * policy
    y_kk = (C * x_kk)[0, 0]
    dy_kk = (y_kk - y_k) / time_step
    set_point_kk = u[(k + 1) % 2000]
    e_kk = set_point_kk - y_kk
    de_kk = (e_kk - e_k) / time_step
    # if abs(de_kk) > 10:
    # de_kk = de_k

    indexes_kk_0 = helper.get_q_indexes(-1, e_kk, de_kk, e_bins, de_bins)
    indexes_kk_1 = helper.get_q_indexes(1, e_kk, de_kk, e_bins, de_bins)

    Qmax = max([Q[indexes_kk_0[0], indexes_kk_0[1], indexes_kk_0[2]],
                Q[indexes_kk_1[0], indexes_kk_1[1], indexes_kk_1[2]]])

    # if abs(e_kk) < 0.005 and abs(de_kk) < 0.05:
    #     r = 5

    abs_e_kk = math.fabs(e_kk)
    if abs_e_kk < math.fabs(e_k):
        r = 3
    else:
        r = 0

    Q[indexes_k[0], indexes_k[1], indexes_k[2]] = (1 - alpha) * Qk + alpha * (r - abs_e_kk + 0.8 * Qmax)

    x_k = x_kk
    y_k = y_kk
    set_point_k = set_point_kk
    e_k = e_kk
    de_k = de_kk

# Validation
t = []
# noinspection PyCallingNonCallable
x = [np.matrix([[0],
                [0]])]
y = [(C * x[0])[0, 0]]
set_point = [u[0]]
e = [set_point[0] - y[0]]
de = [0]
cs = []

# u = []
# for kaka in range(2000):
# u.append(math.sin(kaka * time_step * math.pi / 2))

for k in range(6000):
    t.append(k * time_step)

    indexes_0 = helper.get_q_indexes(-1, e[k], de[k], e_bins, de_bins)
    indexes_1 = helper.get_q_indexes(1, e[k], de[k], e_bins, de_bins)
    if Q[indexes_0[0], indexes_0[1], indexes_0[2]] > Q[indexes_1[0], indexes_1[1], indexes_1[2]]:
        policy = -1
    else:
        policy = 1

    x.append(A * x[k] + B * policy)
    y.append((C * x[k + 1])[0, 0])
    cs.append(policy)
    set_point.append(u[(k + 1) % 2000])
    e.append(set_point[k + 1] - y[k + 1])
    de_kk = (e[k + 1] - e[k]) / time_step
    # if abs(de_kk) > 10:
    # de_kk = de[k]
    de.append(de_kk)

del y[-1]
del set_point[-1]
del e[-1]
del de[-1]

# f, axarr = plt.subplots(2, sharex=True)
# axarr[0].plot(t, set_point, t, y)
# axarr[1].plot(t, e)
#
# for axis in axarr:
#     axis.grid()

plt.plot(t, set_point, t, y)
plt.grid()

plt.show()