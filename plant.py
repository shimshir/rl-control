import numpy as np
import scipy.signal


class SimpleControlPlant():
    def __init__(self, A, B, C, D=None, x_0=None):
        self.A = A
        self.B = B
        self.C = C
        self.D = D

        if x_0 is None:
            self.x = np.matrix(np.zeros(shape=(A.shape[0], 1)))

        if D is None:
            self.D = np.matrix(np.zeros(shape=(C.shape[0], B.shape[1])))

        self.y = C * self.x

    def get_output(self, u):
        self.x = self.A * self.x + self.B * u
        self.y = self.C * self.x + self.D * u
        return self.y

    def get_current_output(self):
        return self.y

    def reset_states(self):
        self.x = np.matrix(np.zeros(shape=(self.A.shape[0], 1)))
        self.y = self.C * self.x

    @staticmethod
    def get_sample_plant(sampling_time):
        z = 0.4
        wn = (2 * scipy.pi)
        c_sys = scipy.signal.tf2ss(wn ** 2, [1, (2 * z * wn), wn ** 2])
        d_sys = scipy.signal.cont2discrete(c_sys, sampling_time)

        return SimpleControlPlant(np.matrix(d_sys[0]), np.matrix(d_sys[1]), np.matrix(d_sys[2]))
