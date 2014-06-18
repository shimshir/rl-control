import numpy as np


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

    @staticmethod
    def get_sample_plant():
        # noinspection PyCallingNonCallable
        A = np.matrix([[0.98991884, -0.07855921],
                       [0.00198993, 0.99992131]])

        # noinspection PyCallingNonCallable
        B = np.matrix([[1.98992813e-03],
                       [1.99328853e-06]])

        # noinspection PyCallingNonCallable
        C = np.matrix([[0., 39.4784176]])

        return SimpleControlPlant(A, B, C)
