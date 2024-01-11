import numpy as np

class bacteria:

    def __init__(self):

        self.looking_at = np.array([1., 0., 0.], dtype = np.float64)
        self.pos = np.array([0., 0.], dtype = np.float64)

        self.mean_angle = 70 * np.pi / 180 # angle in rad
        self.mean_runtime = 1 # runtime in seconds
        self.velocity = 20 # velocity in micrometers / second

    def step():
        pass

