import numpy as np
from matplotlib import animation
from matplotlib import pyplot as plt
from scipy import optimize as op
from AbstractTable import AbstractTable as abT


class RectTable(abT):
    """
    subclass of AbstractTable for the Rectangle table
    needs height and width in addition to AbstractTable parameters
    """

    def __init__(self, **kwargs):
        super(RectTable,self).__init__(**kwargs)
        self.maxx = self.parameters['width']
        self.maxy = self.parameters['height']

    def drawTable(self,ec='none'):
        """
        makes a fig and axes and adds the table as a patch.
        ec should be set to 'k' when generating a preview
        """
        self.fig, self.ax = plt.subplots(figsize=(10, 10))
        self.fig.canvas.set_window_title('Rectangle Billiards Simulation')
        self.ax.set(xlim=[-0.5, 5.5], ylim=[-0.5, 5.5])
        self.ax.axis('off')
        # make table
        self.table = plt.Rectangle((0, 0), self.maxx, self.maxy, ec=ec, lw=1,
            fc='none')
        self.ax.add_patch(self.table)
        plt.axis('equal')

    def update(self,**kwargs):
        """updates superclass parameters as well as height and width"""
        super(RectTable,self).update(**kwargs)
        self.maxx = self.parameters['width']
        self.maxy = self.parameters['height']

    def step(self,particle, dt):
        """
        checks for collissions and updates velocities accordinly for one
        particle
        """
        # check for crossing boundary
        crossed_x1 = particle.state[0] < 0
        crossed_x2 = particle.state[0] > self.maxx
        crossed_y1 = particle.state[1] < 0
        crossed_y2 = particle.state[1] > self.maxy

        # reset the position to the boundry line
        if crossed_x1:
            fun = lambda y: particle.state[2] / particle.state[3] *\
                (y - particle.state[1]) + particle.state[0]
            root = op.brentq(fun, -0.1, self.maxy + 0.1)
            particle.state[0] = 0
            particle.state[1] = root
            particle.state[2] *= -1
        elif crossed_x2:
            fun = lambda y: particle.state[2] / particle.state[3] *\
                (y - particle.state[1]) + particle.state[0] - self.maxx
            root = op.brentq(fun, -0.1, self.maxy + 0.1)
            particle.state[0] = self.maxx
            particle.state[1] = root
            particle.state[2] *= -1
        if crossed_y1:
            fun = lambda x: particle.state[3] / particle.state[2] *\
                (x - particle.state[0]) + particle.state[1]
            root = op.brentq(fun, -0.1, self.maxx + 0.1)
            particle.state[0] = root
            particle.state[1] = 0
            particle.state[3] *= -1
        elif crossed_y2:
            fun = lambda x: particle.state[3] / particle.state[2] *\
                (x - particle.state[0]) + particle.state[1] - self.maxy
            root = op.brentq(fun, -0.1, self.maxx + 0.1)
            particle.state[0] = root
            particle.state[1] = self.maxy
            particle.state[3] *= -1

if __name__ == '__main__':
    table = RectTable()
    table.main()
