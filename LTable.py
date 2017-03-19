import numpy as np
from matplotlib import animation
from matplotlib import pyplot as plt
from scipy import optimize as op

#TODO add option for more balls
#TODO get working in GUI

class LTable(object):
    """docstring for LTable."""

    def __init__(self, **kwargs):
        super().__init__()
        self.parameters = kwargs

    def step(self, dt):
        old_state = np.array(self.state[:2])
        self.state[:2] += dt * self.state[2:]
        

        # check for crossing boundary
        crossed_x1 = self.state[0] < self.Lwidth[0]
        crossed_x2 = (self.state[0] > self.Lwidth[1] and self.state[1] >= self.Lheight[1] and old_state[0] <= self.Lwidth[1])
        crossed_x3 = (self.state[0] > self.Lwidth[2] and self.state[1] < self.Lheight[1])
        crossed_y1 = self.state[1] < self.Lheight[0]
        crossed_y2 = (self.state[0] >= self.Lwidth[1] and self.state[1] > self.Lheight[1] and old_state[0] >= self.Lwidth[1])
        crossed_y3 = (self.state[0] < self.Lwidth[1] and self.state[1] > self.Lheight[2])

        if crossed_x1:
            fun = lambda y: self.state[2] / self.state[3] * (y - self.state[1]) + self.state[0]
            root = op.brentq(fun, -0.1 + self.Lheight[0], self.Lheight[2] + 0.1)
            self.state[0] = self.Lwidth[0]
            self.state[1] = root
            self.state[2] *= -1
            # print('crossed_x1', old_state[:2], self.state[:2], dt)
        elif crossed_x2:
            fun = lambda y: self.state[2] / self.state[3] * (y - self.state[1]) + self.state[0] - self.Lwidth[1]
            root = op.brentq(fun, -0.1 + self.Lheight[1], self.Lheight[2] + 0.1)
            self.state[0] = self.Lwidth[1]
            self.state[1] = root
            self.state[2] *= -1
            # print('crossed_x2', old_state[:2], self.state[:2], dt)
        elif crossed_x3:
            fun = lambda y: self.state[2] / self.state[3] * (y - self.state[1]) + self.state[0] - self.Lwidth[2]
            root = op.brentq(fun, -0.1 + self.Lheight[0], self.Lheight[1] + 0.1)
            self.state[0] = self.Lwidth[2]
            self.state[1] = root
            self.state[2] *= -1
            # print('crossed_x3', old_state[:2], self.state[:2], dt)
        elif crossed_y1:
            fun = lambda x: self.state[3] / self.state[2] * (x - self.state[0]) + self.state[1]
            root = op.brentq(fun, -0.1 + self.Lwidth[0], self.Lwidth[2] + 0.1)
            self.state[0] = root
            self.state[1] = self.Lheight[0]
            self.state[3] *= -1
            # print('crossed_x1', old_state[:2], self.state[:2], dt)
        elif crossed_y2:
            fun = lambda x: self.state[3] / self.state[2] * (x - self.state[0]) + self.state[1] - self.Lheight[1]
            root = op.brentq(fun, -0.1 + self.Lwidth[1], self.Lwidth[2] + 0.1)
            self.state[0] = root
            self.state[1] = self.Lheight[1]
            self.state[3] *= -1
            # print('crossed_y2', old_state[:2], self.state[:2], dt)
        elif crossed_y3:
            fun = lambda x: self.state[3] / self.state[2] * (x - self.state[0]) + self.state[1] - self.Lheight[2]
            root = op.brentq(fun, -0.1 + self.Lwidth[0], self.Lwidth[1] + 0.1)
            self.state[0] = root
            self.state[1] = self.Lheight[2]
            self.state[3] *= -1
            # print('crossed_y3', old_state[:2], self.state[:2], dt)

    def main(self):
        xlines = np.array([0, 4, 4, 2, 2, 0, 0])
        ylines = np.array([0, 0, 2, 2, 6, 6, 0])
        #use this to change the size of the L
        self.Lwidth = np.array([0,2,4])
        self.Lheight =np.array([0,2,6])

        fig, ax = plt.subplots()
        ax.set(xlim=[-0.4, 5], ylim=[-0.4, 7])
        ax.axis('off')
        table, = ax.plot(xlines, ylines, 'k-', lw=1)

        particle, = ax.plot([], [], 'ro', ms=6)
        path, = ax.plot([], [], 'r-', lw=1)

        dt = 1 / 1000
        self.state = np.array([self.parameters['initX'], self.parameters['initY'],
                               self.parameters['initXVel'], self.parameters['initYVel']])
        self.pathx = np.array([])
        self.pathy = np.array([])

        def init():
            """initialize animation"""
            particle.set_data([], [])
            table.set_data([], [])
            path.set_data([], [])
            return particle, table, path

        def animate(i):
            """perform animation step"""
            if self.parameters['trace']:
                self.pathx = np.append(self.pathx, self.state[0])
                self.pathy = np.append(self.pathy, self.state[1])
            self.step(dt)
            # update pieces of the animation
            table.set_data(xlines, ylines)
            particle.set_data(self.state[0], self.state[1])
            path.set_data(self.pathx, self.pathy)
            return particle, table, path

        ani = animation.FuncAnimation(fig, animate, frames=600,
                                      interval=0.001, blit=True, init_func=init)

        plt.show()


if __name__ == '__main__':
    table = LTable(initX=1., initY=1., initXVel=6, initYVel=7, trace=True)
    table.main()
