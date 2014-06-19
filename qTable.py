from matplotlib import pyplot as plt
import rl
import numpy as np
import plant

u = []

for k0 in range(30):
    u.append(0.5)

for k1 in range(30):
    u.append(0)

for k2 in range(29):
    u.append(-0.5)

agent = rl.Agent(e_bins=np.linspace(-2, 2, 100), de_bins=np.linspace(-3, 3, 100),
                 plant=plant.SimpleControlPlant.get_sample_plant(), time_step=0.03)

agent.plant = plant.SimpleControlPlant.get_sample_plant()

for keks in range(500000):
    agent.update_q_table(u[keks % 89])


# Validation
t = []
set_point = [u[0]]
y = [0]
e = [set_point[0] - y[0]]
de = [0]
cs = []
for k in range(89 * 3):
    t.append(k * agent.time_step)
    policy = agent.get_policy([e[k], de[k]])

    y.append(agent.plant.get_output(policy)[0, 0])
    cs.append(policy)
    set_point.append(u[(k + 1) % 89])
    e.append(set_point[k + 1] - y[k + 1])
    de_kk = (e[k + 1] - e[k]) / agent.time_step
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
# axis.grid()

plt.plot(t, set_point, t, y)
plt.grid()

plt.show()