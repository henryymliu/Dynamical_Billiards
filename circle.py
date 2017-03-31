import numpy as np
from matplotlib import animation
from matplotlib import pyplot as plt
from AbstractTable import AbstractTable as abT

class CircleTable(abT):
    """
    subclass of AbstractTable for the Circle table
    """

    def __init__(self, **kwargs):
        super(CircleTable,self).__init__(**kwargs)
        self.radius = 2

    def drawTable(self,ec='none'):
        """
        makes a fig and axes and adds the table as a patch.
        ec should be set to 'k' when generating a preview
        """
        self.fig, self.ax = plt.subplots(figsize=(10,10))
        self.fig.canvas.set_window_title('Circle Billiards Simulation')
        self.ax.set(xlim=[-2, 2], ylim=[-2, 2])
        self.ax.axis('off')
        # make table
        self.table = plt.Circle((0, 0), self.radius, fc='none',ec=ec)
        plt.axis('equal')
        self.ax.add_patch(self.table)

    def step(self, particle, dt):
        """
        checks for collissions and updates velocities accordinly for one
        particle
        """
        # check for crossing boundary
        if np.hypot(particle.state[0], particle.state[1]) > 2:

            if particle.state[2] != 0 and abs(particle.state[3] / particle.state[2]) <= 1:
                m = particle.state[3] / particle.state[2]
                intercept = m * -particle.state[0] + particle.state[1]

                # discrimanant
                b = 2 * m * intercept
                a = m ** 2 + 1
                c = -self.radius ** 2 + intercept ** 2

                # choose root based on proximity with x
                root = -b / (2 * a)
                dis = (np.sqrt(np.fabs(b ** 2 - 4 * a * c))) / (2 * a)
                if abs(particle.state[0] - root - dis) < abs(particle.state[0]\
                    - root + dis):
                    root += dis
                else:
                    root -= dis

                particle.state[0] = root
                particle.state[1] = m * root + intercept
                # print((particle.state[0], particle.state[1]))

                vel_norm = np.hypot(particle.state[0], particle.state[1])
                dot = (particle.state[2] * particle.state[0] +\
                    particle.state[3] * particle.state[1]) / (vel_norm ** 2)
                particle.state[2] = particle.state[2] - 2 * dot *\
                    particle.state[0]
                particle.state[3] = particle.state[3] - 2 * dot *\
                    particle.state[1]

                # print((particle.state[2], particle.state[3]))
                # print((particle.state[0], particle.state[1]))
                # print(np.hypot(particle.state[2], particle.state[3]))

            elif abs(particle.state[2] / particle.state[3]) <= 1:
                m = particle.state[2] / particle.state[3]
                intercept = m * -particle.state[1] + particle.state[0]
                # discriminant
                b = 2 * m * intercept
                a = m ** 2 + 1
                c = -self.radius ** 2 + intercept ** 2

                # choose root based on proximity with current y
                root = -b / (2 * a)
                dis = (np.sqrt(abs(b ** 2 - 4 * a * c))) / (2 * a)
                if abs(particle.state[1] - root - dis) < abs(particle.state[1] - root + dis):
                    root += dis
                else:
                    root -= dis
                # vel = [particle.state[0], particle.state[1]] / vel_norm

                particle.state[0] = m * root + intercept
                particle.state[1] = root
                # print((particle.state[0], particle.state[1]))

                # update velocity based on r = d - 2(r.n)r
                vel_norm = np.hypot(particle.state[0], particle.state[1])
                dot = (particle.state[2] * particle.state[0] + particle.state[3] * particle.state[1]) / (vel_norm ** 2)
                particle.state[2] = particle.state[2] - 2 * dot * particle.state[0]
                particle.state[3] = particle.state[3] - 2 * dot * particle.state[1]
                # print((particle.state[2], particle.state[3]))
                # print((particle.state[0], particle.state[1]))
                # print(np.hypot(particle.state[2], particle.state[3]))

if __name__ == '__main__':
    table = CircleTable()
    table.main()
