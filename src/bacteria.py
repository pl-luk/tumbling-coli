import numpy as np

class bacteria:

    def __init__(self, v = 20, alpha = np.deg2rad(70), tau = 1):

        self.looking_at = np.array([1., 0.], dtype = np.float64)
        self.pos = np.array([0., 0.], dtype = np.float64)
        self.total_runtime = 0

        self.mean_angle = alpha # angle in rad
        self.mean_runtime = tau # runtime in seconds
        self.velocity = v # velocity in micrometers / second

    def step(self):
        
        # draw random angle from normal distribution
        angle = np.random.normal(self.mean_angle)
        self.looking_at = np.array([[np.cos(angle), -np.sin(angle)],
                                    [np.sin(angle), np.cos(angle)]]) @ self.looking_at

        runtime = np.random.exponential(self.mean_runtime)
        self.pos += self.looking_at * runtime * self.velocity
        self.total_runtime += runtime

