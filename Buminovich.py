from matplotlib import pyplot as plt
from matplotlib import animation
import matplotlib.patches as mpatches
import matplotlib.axes as axes
import numpy as np
from scipy import optimize as op
from AbstractTable import AbstractTable as abT

class Buminovich(abT):
    """docstring for Buminovich."""
    def __init__(self, **kwargs):
        abT.__init__(self, **kwargs)
        self.parameters = kwargs
        self.length = 6
        self.height = 6
        self.minlinex = 0
        self.minliney = 0
        self.radius = self.height / 2
    
    def drawTable(self):
        self.fig, self.ax = plt.subplots()
        self.ax.set(xlim=[-(self.minlinex + self.radius + 0.5), (self.length + self.radius + 0.5)],
               ylim=[-(self.radius + 0.5), self.radius + 0.5])
        self.ax.axis('off')

        # x1 = np.array([0, self.length])
        # y1 = np.array([self.radius, self.radius])
        # x2 = np.array([0, self.length])
        # y2 = np.array([-self.radius, -self.radius])

        # table = ax.plot(x1, y1, 'k-', lw=1)
        # table = ax.plot(x2, y2, 'k-', lw=1)

        self.table = mpatches.Arc((0, 0), self.height, self.height, 0, 90, 270)
        plt.axis('equal')
        self.ax.add_patch(self.table)
        self.table = mpatches.Arc((self.length, 0), self.height, self.height, 0, 270, 450)
        plt.axis('equal')
        self.ax.add_patch(self.table)
        self.table = plt.hlines([-self.radius, self.radius], 0, self.length)

    def step(self, particle, dt):
        # self.state[:2] += dt * self.state[2:]
        # check for crossing boundary
        if particle.state[0] >= self.minlinex and particle.state[0] <= self.length:
            crossed_ymax = particle.state[1] > self.radius
            crossed_ymin = particle.state[1] < -self.radius
            if crossed_ymin:
                fun = lambda x: particle.state[3]/particle.state[2]*(x-particle.state[0])+particle.state[1] + self.radius
                root=op.brentq(fun, self.minlinex - 0.1, self.length + 0.1)
                particle.state[0]=root
                particle.state[1]=-self.radius
                particle.state[3]*=-1
            if crossed_ymax:
                fun = lambda x: particle.state[3]/particle.state[2]*(x-particle.state[0])+particle.state[1]-self.radius
                root=op.brentq(fun, self.minlinex - 0.1, self.length + 0.1)
                particle.state[0]=root
                particle.state[1]=self.radius
                particle.state[3]*=-1

        elif particle.state[0] < self.minlinex:
            if np.hypot(particle.state[0], particle.state[1]) > self.radius:
                if abs(particle.state[3] / particle.state[2]) <= 1:
                    m = particle.state[3] / particle.state[2]
                    intercept = m * -particle.state[0] + particle.state[1]

                    # discrimanant
                    b = 2 * m * intercept
                    a = m ** 2 + 1
                    c = -self.radius ** 2 + intercept ** 2

                    # choose root based on proximity with x
                    root = -b / (2 * a)
                    dis = (np.sqrt(abs(b ** 2 - 4 * a * c))) / (2 * a)
                    if abs(particle.state[0] - root - dis) < abs(particle.state[0] - root + dis):
                        root += dis
                    else:
                        root -= dis

                    particle.state[0] = root
                    particle.state[1] = m * root + intercept
                    # print((particle.state[0], particle.state[1]))

                    vel_norm = np.hypot(particle.state[0], particle.state[1])
                    dot = (particle.state[2] * particle.state[0] + particle.state[3] * particle.state[1]) / (vel_norm ** 2)
                    particle.state[2] = particle.state[2] - 2 * dot * particle.state[0]
                    particle.state[3] = particle.state[3] - 2 * dot * particle.state[1]

                    # particle.state[3] *= -1/2;
                    # particle.state[2] *= -1;
                    # print((particle.state[2], particle.state[3]))
                    #print((particle.state[0], particle.state[1]))

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
                    #print((particle.state[0], particle.state[1]))

        elif particle.state[0] > self.length:
            if np.hypot(particle.state[0] - self.length, particle.state[1]) > self.radius:
                #shift table so that centre of right circle is origin
                particle.state[0] = particle.state[0] - self.length
                if abs(particle.state[3] / particle.state[2]) <= 1:
                    m = particle.state[3] / particle.state[2]
                    intercept = m * -particle.state[0] + particle.state[1]

                    # discrimanant
                    b = 2 * m * intercept
                    a = m ** 2 + 1
                    c = -self.radius ** 2 + intercept ** 2

                    # choose root based on proximity with x
                    root = -b / (2 * a)
                    dis = (np.sqrt(abs(b ** 2 - 4 * a * c))) / (2 * a)
                    if abs(particle.state[0] - root - dis) < abs(particle.state[0] - root + dis):
                        root += dis
                    else:
                        root -= dis

                    particle.state[0] = root
                    particle.state[1] = m * root + intercept
                    # print((particle.state[0], particle.state[1]))

                    vel_norm = np.hypot(particle.state[0], particle.state[1])
                    dot = (particle.state[2] * particle.state[0] + particle.state[3] * particle.state[1]) / (vel_norm ** 2)
                    particle.state[2] = particle.state[2] - 2 * dot * particle.state[0]
                    particle.state[3] = particle.state[3] - 2 * dot * particle.state[1]

                    # particle.state[3] *= -1/2;
                    # particle.state[2] *= -1;
                    # print((particle.state[2], particle.state[3]))
                    #print((particle.state[0], particle.state[1]))

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
                    #print((particle.state[0], particle.state[1]))

                #reset table to original origin
                particle.state[0] = particle.state[0] + self.length


if __name__ == '__main__':
    table = Buminovich()
    table.main()
