"""
AbstractTable module for Dynamical Billiards Simulator
All the different tables will be a subclass of this abstract superclass
"""

import numpy as np
from matplotlib import animation
from matplotlib import pyplot as plt
import matplotlib.patches as patches

from PIL import Image

class Ball(object):
    """Holds the colour and state of a ball in the simulation"""
    def __init__(self, **kwargs):
        super().__init__()
        self.parameters = kwargs
        self.state = self.parameters['initstate']
        self.color = self.parameters['color']

class AbstractTable(object):
    """
    Abstract class for a table that simulates collisions
    this superclass takes care of the animating and preview generation
    subclasses will take care of detecting collisions and drawing the table

    subclasses must implement:
        drawTable
        step

    all others are optional
    """

    def __init__(self, **kwargs):
        super().__init__()
        self.parameters = kwargs
        self.colorlist = ['r', 'g', 'b', 'y']
        self.ballList = []
        self.nBalls = self.parameters['nBalls']
        self.drag = 0.999 # TODO: possibly change this with entrybox

        # use colormap for many colors
        self.cmap = plt.cm.get_cmap("rainbow", self.nBalls + 1)

    def drawTable(self, ec='none'):
        """
        Each table must implement this function
        should make a figure and axes in self and should draw the table as a
        collection of matplotlib patches

        edge colour is for the patches, when animating it can be left as none
        but must be 'k' for generatePreview
        """
        return None

    def step(self, particle, dt):
        """
        each table must implement this function
        for each check particle, check if boundaries crossed and update
        velocity (position is updated in stepall)
        """
        return None

    def stepall(self, dt):
        """
        updates position of each ball and checks boundaries using step
        """
        for particle in self.ballList:
            if self.parameters['friction']:
                particle.state[2] *= self.drag
                particle.state[3] *= self.drag
            particle.state[0] += dt * particle.state[2]
            particle.state[1] += dt * particle.state[3]

            self.step(particle, dt)

    def generatePreview(self):
        """
        saves a preview of the figure as preview.png and returns a PIL image
        object of the preview

        must run update before using this method
        """
        # draw table with black edge color
        self.drawTable('k')
        balls=[]
        # initialize all the balls and their positions
        for i in range(self.nBalls):
            balls.append(Ball(color=self.cmap(i),
                              initstate=self.parameters['balls'][i]))
            self.ax.plot(balls[i].state[0], balls[i].state[1],
                         color=self.cmap(i), marker = 'o', ms=8)
            # plot arrow indicating velocity vector
            self.ax.add_patch(patches.Arrow(balls[i].state[0], balls[i].state[1], balls[i].state[2]*0.3,
                                            balls[i].state[3]*0.3, width=0.05, ls='-', color=self.cmap(i)))

        # linewidth needs to be larger than animating so it will be visible in
        # the preview
        self.table.set_linewidth(6)

        self.fig.savefig('preview.png')
        f=Image.open('preview.png')
        # resize object so it will fit in tkinter canvas
        f=f.resize((300,300))
        return f

    def update(self, **kwargs):
        """saves new parameters for the Simulation"""
        self.parameters = kwargs

    def main(self,frames=600):
        """
        opens the matplotlib window and starts the animation
        should run update before calling with function
        """
        # close any figures made from generatePreview
        plt.close('all')
        # make figure and axis and add the table to it
        self.drawTable()
        # define time step. this value seems to work well but can be adjusted
        dt = 1 / 30

        # initialize balls and axes objects
        particles = []
        paths = []
        self.pathx = {}
        self.pathy = {}

        for i in range(self.nBalls):
            # make ball object and add it to ball list
            self.ballList.append(Ball(color=self.cmap(i), initstate=self.parameters['balls'][i]))

            # initialize particles and paths that will be plotted

            particles.append(self.ax.plot([], [], color=self.cmap(i), marker='o', ms=6)[0])
            paths.append(self.ax.plot([], [], color=self.cmap(i), ls='-', lw=1)[0])
            self.pathx[i] = np.array([])
            self.pathy[i] = np.array([])

        def init():
            """
            initialize function for the animation.
            gets run before each frame.
            """
            # reset particles
            for ball in particles:
                ball.set_data([], [])
                ball.set_data([], [])
            # reset table
            self.table.set_edgecolor('none')
            return tuple(particles) + (self.table,) + tuple(paths)

        def animate(k):
            """perform animation step"""
            # trace the particle if check box is selected
            if self.parameters['trace']:
                for i in range(self.nBalls):
                    self.pathx[i] = np.append(self.pathx[i],
                        self.ballList[i].state[0])
                    self.pathy[i] = np.append(self.pathy[i],
                        self.ballList[i].state[1])
            # update position and check for collisions
            self.stepall(dt)
            # update table
            self.table.set_edgecolor('k')
            # set particle position and path data
            for ball in range(self.nBalls):
                particles[ball].set_data(self.ballList[ball].state[0],
                    self.ballList[ball].state[1])
                paths[ball].set_data(self.pathx[ball], self.pathy[ball])
            return tuple(particles) + (self.table,) + tuple(paths)

        # define animation with appropriate playbackSpeed
        ani = animation.FuncAnimation(self.fig, animate, frames=frames,
            interval=np.ceil((1 / self.parameters['playbackSpeed']) * 10 ** 3),
            blit=True, init_func=init)
        # show matplotlib window
        plt.show()
        return ani
