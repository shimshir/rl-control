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

agent = rl.Agent(actions=np.linspace(-1, 1, 3), e_bins=np.linspace(-1, 1, 600),
                 de_bins=np.linspace(-2, 2, 6),
                 plant=plant.SimpleControlPlant.get_sample_plant(0.002), time_step=0.002)

agent.plant = plant.SimpleControlPlant.get_sample_plant(0.002)

for k in range(500000):
    agent.update_q_table(u[k % 1500])


# Validation
agent.plant.reset_states()
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

plt.plot(t, set_point, label="Zadata vrijednost")
plt.plot(t, y, label="Odziv sistema")
plt.legend(loc="upper right")
plt.title("Odziv sistema na step")
plt.grid()
plt.xlabel("t(s)")
plt.ylabel("Izlaz")

plt.show()