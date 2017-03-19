from matplotlib import pyplot as plt
from matplotlib import animation
import matplotlib.patches as mpatches
import matplotlib.axes as axes
import numpy as np
from scipy import optimize as op

class Buminovich(object):
    """docstring for Buminovich."""
    def __init__(self, **kwargs):
        super().__init__()
        self.parameters = kwargs
        self.length = 4
        self.height = 4
        self.minlinex = 0
        self.minliney = 0
        self.radius = self.height / 2

    def step(self, dt):
        self.state[:2] += dt * self.state[2:]
        # check for crossing boundary
        if self.state[0] >= self.minlinex and self.state[0] <= self.length:
            crossed_ymax = self.state[1] > self.radius
            crossed_ymin = self.state[1] < -self.radius
            if crossed_ymin:
                fun = lambda x: self.state[3]/self.state[2]*(x-self.state[0])+self.state[1] + self.radius
                root=op.brentq(fun, self.minlinex - 0.1, self.length + 0.1)
                self.state[0]=root
                self.state[1]=-self.radius
                self.state[3]*=-1
            if crossed_ymax:
                fun = lambda x: self.state[3]/self.state[2]*(x-self.state[0])+self.state[1]-self.radius
                root=op.brentq(fun, self.minlinex - 0.1, self.length + 0.1)
                self.state[0]=root
                self.state[1]=self.radius
                self.state[3]*=-1

        elif self.state[0] < self.minlinex:
            if np.hypot(self.state[0], self.state[1]) > self.radius:
                if abs(self.state[3] / self.state[2]) <= 1:
                    m = self.state[3] / self.state[2]
                    intercept = m * -self.state[0] + self.state[1]

                    # discrimanant
                    b = 2 * m * intercept
                    a = m ** 2 + 1
                    c = -self.radius ** 2 + intercept ** 2

                    # choose root based on proximity with x
                    root = -b / (2 * a)
                    dis = (np.sqrt(abs(b ** 2 - 4 * a * c))) / (2 * a)
                    if abs(self.state[0] - root - dis) < abs(self.state[0] - root + dis):
                        root += dis
                    else:
                        root -= dis

                    self.state[0] = root
                    self.state[1] = m * root + intercept
                    # print((self.state[0], self.state[1]))

                    vel_norm = np.hypot(self.state[0], self.state[1])
                    dot = (self.state[2] * self.state[0] + self.state[3] * self.state[1]) / (vel_norm ** 2)
                    self.state[2] = self.state[2] - 2 * dot * self.state[0]
                    self.state[3] = self.state[3] - 2 * dot * self.state[1]

                    # self.state[3] *= -1/2;
                    # self.state[2] *= -1;
                    # print((self.state[2], self.state[3]))
                    #print((self.state[0], self.state[1]))

                elif abs(self.state[2] / self.state[3]) <= 1:
                    m = self.state[2] / self.state[3]
                    intercept = m * -self.state[1] + self.state[0]
                    # discriminant
                    b = 2 * m * intercept
                    a = m ** 2 + 1
                    c = -self.radius ** 2 + intercept ** 2

                    # choose root based on proximity with current y
                    root = -b / (2 * a)
                    dis = (np.sqrt(abs(b ** 2 - 4 * a * c))) / (2 * a)
                    if abs(self.state[1] - root - dis) < abs(self.state[1] - root + dis):
                        root += dis
                    else:
                        root -= dis
                    # vel = [self.state[0], self.state[1]] / vel_norm

                    self.state[0] = m * root + intercept
                    self.state[1] = root
                    # print((self.state[0], self.state[1]))

                    # update velocity based on r = d - 2(r.n)r
                    vel_norm = np.hypot(self.state[0], self.state[1])
                    dot = (self.state[2] * self.state[0] + self.state[3] * self.state[1]) / (vel_norm ** 2)
                    self.state[2] = self.state[2] - 2 * dot * self.state[0]
                    self.state[3] = self.state[3] - 2 * dot * self.state[1]
                    # print((self.state[2], self.state[3]))
                    #print((self.state[0], self.state[1]))

        elif self.state[0] > self.length:
            if np.hypot(self.state[0] - self.length, self.state[1]) > self.radius:
                #shift table so that centre of right circle is origin
                self.state[0] = self.state[0] - self.length
                if abs(self.state[3] / self.state[2]) <= 1:
                    m = self.state[3] / self.state[2]
                    intercept = m * -self.state[0] + self.state[1]

                    # discrimanant
                    b = 2 * m * intercept
                    a = m ** 2 + 1
                    c = -self.radius ** 2 + intercept ** 2

                    # choose root based on proximity with x
                    root = -b / (2 * a)
                    dis = (np.sqrt(abs(b ** 2 - 4 * a * c))) / (2 * a)
                    if abs(self.state[0] - root - dis) < abs(self.state[0] - root + dis):
                        root += dis
                    else:
                        root -= dis

                    self.state[0] = root
                    self.state[1] = m * root + intercept
                    # print((self.state[0], self.state[1]))

                    vel_norm = np.hypot(self.state[0], self.state[1])
                    dot = (self.state[2] * self.state[0] + self.state[3] * self.state[1]) / (vel_norm ** 2)
                    self.state[2] = self.state[2] - 2 * dot * self.state[0]
                    self.state[3] = self.state[3] - 2 * dot * self.state[1]

                    # self.state[3] *= -1/2;
                    # self.state[2] *= -1;
                    # print((self.state[2], self.state[3]))
                    #print((self.state[0], self.state[1]))

                elif abs(self.state[2] / self.state[3]) <= 1:
                    m = self.state[2] / self.state[3]
                    intercept = m * -self.state[1] + self.state[0]
                    # discriminant
                    b = 2 * m * intercept
                    a = m ** 2 + 1
                    c = -self.radius ** 2 + intercept ** 2

                    # choose root based on proximity with current y
                    root = -b / (2 * a)
                    dis = (np.sqrt(abs(b ** 2 - 4 * a * c))) / (2 * a)
                    if abs(self.state[1] - root - dis) < abs(self.state[1] - root + dis):
                        root += dis
                    else:
                        root -= dis
                    # vel = [self.state[0], self.state[1]] / vel_norm

                    self.state[0] = m * root + intercept
                    self.state[1] = root
                    # print((self.state[0], self.state[1]))

                    # update velocity based on r = d - 2(r.n)r
                    vel_norm = np.hypot(self.state[0], self.state[1])
                    dot = (self.state[2] * self.state[0] + self.state[3] * self.state[1]) / (vel_norm ** 2)
                    self.state[2] = self.state[2] - 2 * dot * self.state[0]
                    self.state[3] = self.state[3] - 2 * dot * self.state[1]
                    # print((self.state[2], self.state[3]))
                    #print((self.state[0], self.state[1]))

                #reset table to original origin
                self.state[0] = self.state[0] + self.length

    def main(self):
        fig, ax=plt.subplots()
        ax.set(xlim=[-(self.minlinex + self.radius + 0.5),(self.length + self.radius + 0.5)],ylim=[-(self.radius + 0.5),self.radius + 0.5])
        ax.axis('off')

        #x1 = np.array([0, self.length])
        #y1 = np.array([self.radius, self.radius])
        #x2 = np.array([0, self.length])
        #y2 = np.array([-self.radius, -self.radius])

        #table = ax.plot(x1, y1, 'k-', lw=1)
        #table = ax.plot(x2, y2, 'k-', lw=1)

        table = mpatches.Arc((0, 0), self.height, self.height, 0, 90, 270)
        plt.axis('equal')
        ax.add_patch(table)
        table = mpatches.Arc((self.length, 0), self.height, self.height, 0, 270, 450)
        plt.axis('equal')
        ax.add_patch(table)
        table = plt.hlines([-self.radius, self.radius], 0, self.length)

        particle, = ax.plot([], [], 'ro', ms=6)
        path, = ax.plot([],[], 'r-',lw=1)

        dt = 1/30
        self.state = np.array([self.parameters['initX'],self.parameters['initY'],
                self.parameters['initXVel'],self.parameters['initYVel']])
        self.pathx=np.array([])
        self.pathy=np.array([])

        def init():
            """initialize animation"""
            particle.set_data([], [])
            table.set_edgecolor('none')
            path.set_data([], [])
            return particle, table, path

        def animate(i):
            """perform animation step"""
            if self.parameters['trace']:
                self.pathx = np.append(self.pathx, self.state[0])
                self.pathy = np.append(self.pathy, self.state[1])
            self.step(dt)
            # update pieces of the animation
            table.set_edgecolor('k')
            particle.set_data(self.state[0], self.state[1])
            path.set_data(self.pathx, self.pathy)
            return particle, table, path

        ani = animation.FuncAnimation(fig, animate, frames=600,
                                      interval=0.001, blit=True, init_func=init)

        plt.show()


if __name__ == '__main__':
    table = Buminovich()
    table.main()
