import numpy as np
from matplotlib import animation
from matplotlib import pyplot as plt
from scipy import optimize as op

# plan for abstract table
# create list of n particle objects
#       each particle has initial particle.state from gui
#       somehow assign each color, possibly from a master color list?
#       setep through each particle (done)


class Ball:
    def __init__(self, **kwargs):
        # x , y, xvel, yvel
        # super().__init__()
        self.parameters = kwargs
        self.state = self.parameters['initstate']
        self.color = self.parameters['color']


class AbstractTable(object):
    """docstring for AbstractTable."""
    """each table must implement step and drawTable"""

    def __init__(self, **kwargs):
        super().__init__()
        self.parameters = kwargs
        self.colorlist = ['r', 'g', 'b', 'y']
        self.ballList = []
        self.nBalls = 1 # TODO use number of balls as parameter instead of string

        # self.maxx = self.parameters['width']
        # self.maxy = self.parameters['height']

    # each table must implement this
    # use self.fig, self.ax, and self.table for plotting
    def drawTable(self):

        # TODO this needs tweaking to make aspect always the same
        # self.fig, self.ax = plt.subplots(figsize=(10, 10))
        # self.fig.canvas.set_window_title('Rectangle Billiards Simulation')
        # self.ax.set(xlim=[-0.5, self.maxx + 0.5], ylim=[-0.5, self.maxy + 0.5])
        # # ax.axis('off')
        # # make table
        # self.table = plt.Rectangle((0, 0), self.maxx, self.maxy, ec='none', lw=1, fc='none')
        # self.ax.add_patch(self.table)
        # plt.axis('equal')
        return None
    # each table must implement this function
    # each step increment Position
    def step(self, particle, dt):
        # set new Position
        # check for crossing boundary
        # crossed_x1 = particle.state[0] < 0
        # crossed_x2 = particle.state[0] > self.maxx
        # crossed_y1 = particle.state[1] < 0
        # crossed_y2 = particle.state[1] > self.maxy
        #
        # # reset the position to the boundry line
        # if crossed_x1:
        #     fun = lambda y: particle.state[2] / particle.state[3] * (y - particle.state[1]) + particle.state[0]
        #     root = op.brentq(fun, -0.1, self.maxy + 0.1)
        #     particle.state[0] = 0
        #     particle.state[1] = root
        #     particle.state[2] *= -1
        # elif crossed_x2:
        #     fun = lambda y: particle.state[2] / particle.state[3] * (y - particle.state[1]) + particle.state[0] - self.maxx
        #     root = op.brentq(fun, -0.1, self.maxy + 0.1)
        #     particle.state[0] = self.maxx
        #     particle.state[1] = root
        #     particle.state[2] *= -1
        #
        # if crossed_y1:
        #     fun = lambda x: particle.state[3] / particle.state[2] * (x - particle.state[0]) + particle.state[1]
        #     root = op.brentq(fun, -0.1, self.maxx + 0.1)
        #     particle.state[0] = root
        #     particle.state[1] = 0
        #     particle.state[3] *= -1
        # elif crossed_y2:
        #     fun = lambda x: particle.state[3] / particle.state[2] * (x - particle.state[0]) + particle.state[1] - self.maxy
        #     root = op.brentq(fun, -0.1, self.maxx + 0.1)
        #     particle.state[0] = root
        #     particle.state[1] = self.maxy
        #     particle.state[3] *= -1
        return None

    def stepall(self, dt):
            for particle in self.ballList:
                # particle.state[:2] += dt * particle.state[2:]
                particle.state[0] += dt * particle.state[2]
                particle.state[1] += dt * particle.state[3]

                self.step(particle, dt)

    # TODO separate table plotting stuff from ball selection
    def main(self):
        self.drawTable()

        # define time step for 30 fps
        dt = 1 / 30

        # temporary workaround; will later directly use number
        if self.parameters['ballFormation'] == '1 Ball':
            self.nBalls = 1
        elif self.parameters['ballFormation'] == '2 Balls':
            self.nBalls = 2
        elif self.parameters['ballFormation'] == '3 Balls':
            self.nBalls = 3
        elif self.parameters['ballFormation'] == '4 Balls':
            self.nBalls = 4

        # initialize balls
        particles = []
        paths = []
        self.pathx = {}
        self.pathy = {}

        for i in range(0, self.nBalls):
            self.ballList.append(Ball(**{'color': self.colorlist[i], 'initstate': self.parameters['balls']['Ball ' + str(i + 1)]}))
            particles.append(self.ax.plot([], [], self.ballList[i].color + 'o', ms=6)[0])
            paths.append(self.ax.plot([], [], self.ballList[i].color + '-', lw=1)[0])
            # paths[i], = ax.plot([], [], self.ballList[i -1].color + '-', lw=1)
            self.pathx[i] = np.array([])
            self.pathy[i] = np.array([])
        # set initial conditions
        # self.particle.state = self.parameters['balls']
        # for :

           # particle.state[ball] = np.array(particle.state)

        # self.dotStyle = {'Ball 1': 'ro', 'Ball 2': 'bo', 'Ball 3': 'go', 'Ball 4': 'yo'}
        # self.lineStyle = {'Ball 1': 'r-', 'Ball 2': 'b-', 'Ball 3': 'g-', 'Ball 4': 'y-'}
        # if self.parameters['ballFormation'] == '1 Ball':
        #     self.particle.state = {'Ball 1': self.particle.state['Ball 1']}
        #     self.dotStyle = {'Ball 1': self.dotStyle['Ball 1']}
        #     self.lineStyle = {'Ball 1': self.lineStyle['Ball 1']}
        # elif self.parameters['ballFormation'] == '2 Balls':
        #     self.particle.state = {'Ball 1': self.particle.state['Ball 1'], 'Ball 2': self.particle.state['Ball 2']}
        #     self.dotStyle = {'Ball 1': self.dotStyle['Ball 1'], 'Ball 2': self.dotStyle['Ball 2']}
        #     self.lineStyle = {'Ball 1': self.lineStyle['Ball 1'], 'Ball 2': self.lineStyle['Ball 2']}
        # elif self.parameters['ballFormation'] == '3 Balls':
        #     self.particle.state = {'Ball 1': self.particle.state['Ball 1'], 'Ball 2': self.particle.state['Ball 2'],
        #                   'Ball 3': self.particle.state['Ball 3']}
        #     self.dotStyle = {'Ball 1': self.dotStyle['Ball 1'], 'Ball 2': self.dotStyle['Ball 2'],
        #                      'Ball 3': self.dotStyle['Ball 3']}
        #     self.lineStyle = {'Ball 1': self.lineStyle['Ball 1'], 'Ball 2': self.lineStyle['Ball 2'],
        #                       'Ball 3': self.dotStyle['Ball 3']}
        # elif self.parameters['ballFormation'] == '4 Balls':
        #     self.particle.state = {'Ball 1': self.particle.state['Ball 1'], 'Ball 2': self.particle.state['Ball 2'],
        #                   'Ball 3': self.particle.state['Ball 3'], 'Ball 4': self.particle.state['Ball 4']}
        #     self.dotStyle = {'Ball 1': self.dotStyle['Ball 1'], 'Ball 2': self.dotStyle['Ball 2'],
        #                      'Ball 3': self.dotStyle['Ball 3'], 'Ball 4': self.dotStyle['Ball 4']}
        #     self.lineStyle = {'Ball 1': self.lineStyle['Ball 1'], 'Ball 2': self.lineStyle['Ball 2'],
        #                       'Ball 3': self.lineStyle['Ball 3'], 'Ball 4': self.lineStyle['Ball 4']}

        # for ball in self.dotStyle.keys():
        #     particles[ball], = ax.plot([], [], self.dotStyle[ball], ms=6)
        #     paths[ball], = ax.plot([], [], self.lineStyle[ball], lw=1)
        #     self.pathx[ball] = np.array([])
        #     self.pathy[ball] = np.array([])

        # init function for animation
        # TODO: possibly cleanup return statements?
        def init():
            """initialize animation"""
            for ball in particles:
                ball.set_data([], [])
                ball.set_data([], [])
            self.table.set_edgecolor('none')

            if self.parameters['ballFormation'] == '4 Balls':

                return particles[0], particles[1], particles[2], particles[3], \
                        self.table, paths[0], paths[1],paths[2],paths[3]

            elif self.parameters['ballFormation'] == '3 Balls':
                return particles[0], particles[1], particles[2], \
                       self.table, paths[0], paths[1], paths[2]
            elif self.parameters['ballFormation'] == '2 Balls':
                return particles[0], particles[1], \
                       self.table, paths[0], paths[1]
            else:
                return particles[0], self.table, paths[0]

        def animate(k):
            """perform animation step"""
            # trace the particle if check box is selected
            if self.parameters['trace']:
                for i in range(0, self.nBalls):
                    self.pathx[i] = np.append(self.pathx[i], self.ballList[i].state[0])
                    self.pathy[i] = np.append(self.pathy[i], self.ballList[i].state[1])
            self.stepall(dt)
            # update pieces of the animation
            self.table.set_edgecolor('k')

            for ball in range(0, self.nBalls):
                particles[ball].set_data(self.ballList[ball].state[0], self.ballList[ball].state[1])
                paths[ball].set_data(self.pathx[ball], self.pathy[ball])

            if self.parameters['ballFormation'] == '4 Balls':

                return particles[0], particles[1], particles[2], particles[3], \
                       self.table, paths[0], paths[1], paths[2], paths[3]

            elif self.parameters['ballFormation'] == '3 Balls':
                return particles[0], particles[1], particles[2], \
                       self.table, paths[0], paths[1], paths[2]
            elif self.parameters['ballFormation'] == '2 Balls':
                return particles[0], particles[1], \
                       self.table, paths[0], paths[1]
            else:
                return particles[0], self.table, paths[0]

        # define animation
        ani = animation.FuncAnimation(self.fig, animate, frames=600,
                                      interval=np.ceil((1 / self.parameters['playbackSpeed']) * 10 ** 3), blit=True,
                                      init_func=init)

        plt.show()
