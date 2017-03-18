import numpy as np
from matplotlib import animation
from matplotlib import pyplot as plt
from scipy import optimize as op


class RectTable(object):
    """docstring for RectTable."""

    def __init__(self, **kwargs):
        super().__init__()
        self.parameters = kwargs

    # each step increment Position
    def step(self, dt):
        # set new Position
        for state in self.state.values():
            state[:2] += dt * state[2:]
            # check for crossing boundary
            crossed_x1 = state[0] < 0
            crossed_x2 = state[0] > self.maxx
            crossed_y1 = state[1] < 0
            crossed_y2 = state[1] > self.maxy

            # reset the position to the boundry line
            if crossed_x1:
                fun = lambda y: state[2] / state[3] * (y - state[1]) + state[0]
                root = op.brentq(fun, -0.1, self.maxy + 0.1)
                state[0] = 0
                state[1] = root
                state[2] *= -1
            elif crossed_x2:
                fun = lambda y: state[2] / state[3] * (y - state[1]) + state[0] - self.maxx
                root = op.brentq(fun, -0.1, self.maxy + 0.1)
                state[0] = self.maxx
                state[1] = root
                state[2] *= -1

            if crossed_y1:
                fun = lambda x: state[3] / state[2] * (x - state[0]) + state[1]
                root = op.brentq(fun, -0.1, self.maxx + 0.1)
                state[0] = root
                state[1] = 0
                state[3] *= -1
            elif crossed_y2:
                fun = lambda x: state[3] / state[2] * (x - state[0]) + state[1] - self.maxy
                root = op.brentq(fun, -0.1, self.maxx + 0.1)
                state[0] = root
                state[1] = self.maxy
                state[3] *= -1

    def main(self):
        self.maxx = self.parameters['width']
        self.maxy = self.parameters['height']
        # TODO this needs tweaking to make aspect always the same
        fig, ax = plt.subplots(figsize=(10, 10))
        fig.canvas.set_window_title('Rectangle Billiards Simulation')
        ax.set(xlim=[-0.5, self.maxx + 0.5], ylim=[-0.5, self.maxy + 0.5])
        # ax.axis('off')
        # make table
        table = plt.Rectangle((0, 0), self.maxx, self.maxy, ec='none', lw=1, fc='none')
        ax.add_patch(table)
        plt.axis('equal')

        # define time step for 30 fps
        dt = 1 / 30
        # set initial conditons
        self.state = self.parameters['balls']
        for ball, state in self.state.items():
            self.state[ball] = np.array(state)

        self.dotStyle = {'Ball 1': 'ro', 'Ball 2': 'bo', 'Ball 3': 'go', 'Ball 4': 'yo'}
        self.lineStyle = {'Ball 1': 'r-', 'Ball 2': 'b-', 'Ball 3': 'g-', 'Ball 4': 'y-'}
        if self.parameters['ballFormation'] == '1 Ball':
            self.state = {'Ball 1': self.state['Ball 1']}
            self.dotStyle = {'Ball 1': self.dotStyle['Ball 1']}
            self.lineStyle = {'Ball 1': self.lineStyle['Ball 1']}
        elif self.parameters['ballFormation'] == '2 Balls':
            self.state = {'Ball 1': self.state['Ball 1'], 'Ball 2': self.state['Ball 2']}
            self.dotStyle = {'Ball 1': self.dotStyle['Ball 1'], 'Ball 2': self.dotStyle['Ball 2']}
            self.lineStyle = {'Ball 1': self.lineStyle['Ball 1'], 'Ball 2': self.lineStyle['Ball 2']}
        elif self.parameters['ballFormation'] == '3 Balls':
            self.state = {'Ball 1': self.state['Ball 1'], 'Ball 2': self.state['Ball 2'],
                          'Ball 3': self.state['Ball 3']}
            self.dotStyle = {'Ball 1': self.dotStyle['Ball 1'], 'Ball 2': self.dotStyle['Ball 2'],
                             'Ball 3': self.dotStyle['Ball 3']}
            self.lineStyle = {'Ball 1': self.lineStyle['Ball 1'], 'Ball 2': self.lineStyle['Ball 2'],
                              'Ball 3': self.dotStyle['Ball 3']}
        elif self.parameters['ballFormation'] == '4 Balls':
            self.state = {'Ball 1': self.state['Ball 1'], 'Ball 2': self.state['Ball 2'],
                          'Ball 3': self.state['Ball 3'], 'Ball 4': self.state['Ball 4']}
            self.dotStyle = {'Ball 1': self.dotStyle['Ball 1'], 'Ball 2': self.dotStyle['Ball 2'],
                             'Ball 3': self.dotStyle['Ball 3'], 'Ball 4': self.dotStyle['Ball 4']}
            self.lineStyle = {'Ball 1': self.lineStyle['Ball 1'], 'Ball 2': self.lineStyle['Ball 2'],
                              'Ball 3': self.lineStyle['Ball 3'], 'Ball 4': self.lineStyle['Ball 4']}
        particles = {}
        paths = {}
        self.pathx = {}
        self.pathy = {}

        for ball in self.dotStyle.keys():
            particles[ball], = ax.plot([], [], self.dotStyle[ball], ms=6)
            paths[ball], = ax.plot([], [], self.lineStyle[ball], lw=1)
            self.pathx[ball] = np.array([])
            self.pathy[ball] = np.array([])

        # init function for animation
        def init():
            """initialize animation"""
            for ball in particles.keys():
                particles[ball].set_data([], [])
                paths[ball].set_data([], [])
            table.set_edgecolor('none')

            if self.parameters['ballFormation'] == '4 Balls':
                return particles['Ball 1'], particles['Ball 2'], \
                       particles['Ball 3'], particles['Ball 4'], table, \
                       paths['Ball 1'], paths['Ball 2'], paths['Ball 3'], \
                       paths['Ball 4']
            elif self.parameters['ballFormation'] == '3 Balls':
                return particles['Ball 1'], particles['Ball 2'], \
                       particles['Ball 3'], table, paths['Ball 1'], paths['Ball 2'], \
                       paths['Ball 3']
            elif self.parameters['ballFormation'] == '2 Balls':
                return particles['Ball 1'], particles['Ball 2'], table, \
                       paths['Ball 1'], paths['Ball 2']
            else:
                return particles['Ball 1'], table, paths['Ball 1']

        def animate(i):
            """perform animation step"""
            # trace the particle if check box is selected
            if self.parameters['trace']:
                for ball in self.pathx.keys():
                    self.pathx[ball] = np.append(self.pathx[ball], self.state[ball][0])
                    self.pathy[ball] = np.append(self.pathy[ball], self.state[ball][1])
            self.step(dt)
            # update pieces of the animation
            table.set_edgecolor('k')

            for ball in particles.keys():
                particles[ball].set_data(self.state[ball][0], self.state[ball][1])
                paths[ball].set_data(self.pathx[ball], self.pathy[ball])

            if self.parameters['ballFormation'] == '4 Balls':
                return particles['Ball 1'], particles['Ball 2'], \
                       particles['Ball 3'], particles['Ball 4'], table, \
                       paths['Ball 1'], paths['Ball 2'], paths['Ball 3'], \
                       paths['Ball 4']
            elif self.parameters['ballFormation'] == '3 Balls':
                return particles['Ball 1'], particles['Ball 2'], \
                       particles['Ball 3'], table, paths['Ball 1'], paths['Ball 2'], \
                       paths['Ball 3']
            elif self.parameters['ballFormation'] == '2 Balls':
                return particles['Ball 1'], particles['Ball 2'], table, \
                       paths['Ball 1'], paths['Ball 2']
            else:
                return particles['Ball 1'], table, paths['Ball 1']

        # define animation
        ani = animation.FuncAnimation(fig, animate, frames=600,
                                      interval=np.ceil((1 / self.parameters['playbackSpeed']) * 10 ** 3), blit=True,
                                      init_func=init)

        plt.show()


if __name__ == '__main__':
    table = RectTable()
    table.main()
