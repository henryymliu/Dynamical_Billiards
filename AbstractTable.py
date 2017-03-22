import numpy as np
from matplotlib import animation
from matplotlib import pyplot as plt
from scipy import optimize as op
from PIL import Image

# plan for abstract table
# create list of n particle objects
#       each particle has initial particle.state from gui
#       somehow assign each color, possibly from a master color list?
#       setep through each particle (done)

# Ball object that stores its state (x, y, xvel, yvel) and plot color
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
        self.nBalls = self.parameters['nBalls']

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
    # for each check particle, check if boundaries crossed and update velocity and position
    def step(self, particle, dt):

        return None

    # iterates through all particles; steps through time and then checks for boundaries
    def stepall(self, dt):
        for particle in self.ballList:
            # particle.state[:2] += dt * particle.state[2:]
            particle.state[0] += dt * particle.state[2]
            particle.state[1] += dt * particle.state[3]

            self.step(particle, dt)

    def generatePreview(self):
        # image = Image.open('images/Circle_1Ball.png')
        # return image
        self.drawTable('k')
        balls=[]

        for i in range(self.nBalls):
            balls.append(Ball(color= self.colorlist[i], initstate= self.parameters['balls']['Ball ' + str(i + 1)]))
            self.ax.plot(balls[i].state[0], balls[i].state[1],
                balls[i].color + 'o', ms=6)

        self.table.set_linewidth(6)

        self.fig.savefig('preview.png')
        f=Image.open('preview.png')
        f=f.resize((300,300))
        return f

    def update(self,**kwargs):
        self.parameters=kwargs
    def main(self):
        plt.close('all')
        self.drawTable()

        # define time step for 30 fps
        dt = 1 / 30

        # initialize balls
        particles = []
        paths = []
        self.pathx = {}
        self.pathy = {}

        for i in range(self.nBalls):
            self.ballList.append(Ball(color= self.colorlist[i], initstate= self.parameters['balls']['Ball ' + str(i + 1)]))
            particles.append(self.ax.plot([], [], self.ballList[i].color + 'o', ms=6)[0])
            paths.append(self.ax.plot([], [], self.ballList[i].color + '-', lw=1)[0])
            # paths[i], = ax.plot([], [], self.ballList[i -1].color + '-', lw=1)
            self.pathx[i] = np.array([])
            self.pathy[i] = np.array([])

        # init function for animation
        # TODO: possibly cleanup return statements?
        def init():
            """initialize animation"""
            for ball in particles:
                ball.set_data([], [])
                ball.set_data([], [])
            self.table.set_edgecolor('none')

            if self.nBalls == 4:
                return particles[0], particles[1], particles[2], particles[3], \
                        self.table, paths[0], paths[1],paths[2],paths[3]
            elif self.nBalls == 3:
                return particles[0], particles[1], particles[2], \
                       self.table, paths[0], paths[1], paths[2]
            elif self.nBalls == 2:
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

            for ball in range(self.nBalls):
                particles[ball].set_data(self.ballList[ball].state[0], self.ballList[ball].state[1])
                paths[ball].set_data(self.pathx[ball], self.pathy[ball])

            if self.nBalls == 4:

                return particles[0], particles[1], particles[2], particles[3], \
                       self.table, paths[0], paths[1], paths[2], paths[3]

            elif self.nBalls == 3:
                return particles[0], particles[1], particles[2], \
                       self.table, paths[0], paths[1], paths[2]
            elif self.nBalls == 2:
                return particles[0], particles[1], \
                       self.table, paths[0], paths[1]
            else:
                return particles[0], self.table, paths[0]

        # define animation
        ani = animation.FuncAnimation(self.fig, animate, frames=600,
                                      interval=np.ceil((1 / self.parameters['playbackSpeed']) * 10 ** 3), blit=True,
                                      init_func=init)

        plt.show()
