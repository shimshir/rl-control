from matplotlib import pyplot as plt
import rl
import numpy as np
import plant

u = []

for k0 in range(500):
    u.append(0.5)

for k1 in range(500):
    u.append(0)

for k2 in range(500):
    u.append(-0.5)

agent = rl.Agent(actions=np.linspace(-1, 1, 5), e_bins=np.linspace(-1, 1, 200), de_bins=np.linspace(-2, 2, 10),
                 plant=plant.SimpleControlPlant.get_sample_plant(0.002), time_step=0.002)

agent.plant = plant.SimpleControlPlant.get_sample_plant(0.002)

for keks in range(5000):
    agent.update_q_table(u[keks % 1500])


# Validation
t = []
set_point = [u[0]]
y = [0]
e = [set_point[0] - y[0]]
de = [0]
cs = []
for k in range(1500 * 3):
    t.append(k * agent.time_step)
    policy = agent.get_policy([e[k], de[k]])

    y.append(agent.plant.get_output(policy)[0, 0])
    cs.append(policy)
    set_point.append(u[(k + 1) % 1500])
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

plt.plot(t, set_point, label="Zadata vrijednost")
plt.plot(t, y, label="Odziv sistema")
plt.legend(loc="upper right")
plt.title("Odziv sistema na step")
plt.grid()
plt.xlabel("t(s)")
plt.ylabel("Izlaz")

plt.show()