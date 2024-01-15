import numpy as np

class bacteria:

    def __init__(self):

        self.looking_at = np.array([1., 0.], dtype = np.float64)
        self.pos = np.array([0., 0.], dtype = np.float64)

        self.mean_angle = 70 * np.pi / 180 # angle in rad
        self.mean_runtime = 1 # runtime in seconds
        self.velocity = 20 # velocity in micrometers / second

    def step(self):
        
        # draw random angle from normal distribution
        angle = np.random.normal(self.mean_angle)
        self.looking_at = np.array([[np.cos(angle), -np.sin(angle)],
                                    [np.sin(angle), np.cos(angle)]]) @ self.looking_at

        runtime = np.random.exponential(self.mean_runtime)
        self.pos += self.looking_at * runtime * self.velocity

