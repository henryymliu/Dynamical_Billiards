import numpy as np
from matplotlib import animation
from matplotlib import pyplot as plt
from scipy import optimize as op
from AbstractTable import AbstractTable as abT

class LTable(abT):
    """
    subclass of AbstractTable for the Rectangle table
    needs height and width in addition to AbstractTable parameters
    """

    def __init__(self,**kwargs):
        super(LTable,self).__init__(**kwargs)
        self.Lwidth = np.array([0,2,4])
        self.Lheight =np.array([0,2,6])

    def drawTable(self,ec='none'):
        """
        makes a fig and axes and adds the table as a patch.
        ec should be set to 'k' when generating a preview
        """
        self.fig, self.ax = plt.subplots(figsize=(10, 10))
        self.fig.canvas.set_window_title('L Billiards Simulation')
        self.ax.set(xlim=[-0.4, 5], ylim=[-0.4, 7])
        self.ax.axis('off')
        # make table
        # define array of points to draw the L
        lines = np.array([[0,0],[4,0],[4,2],[2,2],[2,6],[0,6],[0,0]])
        # make L shaped polygon patch using points in lines
        self.table = plt.Polygon(lines, ec=ec, lw=1, fc='none')
        self.ax.add_patch(self.table)
        plt.axis('equal')

    def step(self,particle, dt):
        """
        checks for collissions and updates velocities accordinly for one
        particle
        """
        old_state = np.array(particle.state[:2])

        # check for crossing boundary
        crossed_x1 = particle.state[0] < self.Lwidth[0]
        crossed_x2 = (particle.state[0] > self.Lwidth[1] and particle.state[1]\
            >= self.Lheight[1] and old_state[0] <= self.Lwidth[1])
        crossed_x3 = (particle.state[0] > self.Lwidth[2] and particle.state[1]\
            < self.Lheight[1])
        crossed_y1 = particle.state[1] < self.Lheight[0]
        crossed_y2 = (particle.state[0] >= self.Lwidth[1] and particle.state[1]\
            > self.Lheight[1] and old_state[0] >= self.Lwidth[1])
        crossed_y3 = (particle.state[0] < self.Lwidth[1] and particle.state[1]\
            > self.Lheight[2])

        if crossed_x1:
            fun = lambda y: particle.state[2] / particle.state[3] *\
                (y - particle.state[1]) + particle.state[0]
            root = op.brentq(fun, -0.1 + self.Lheight[0], self.Lheight[2] + 0.1)
            particle.state[0] = self.Lwidth[0]
            particle.state[1] = root
            particle.state[2] *= -1
            # print('crossed_x1', old_state[:2], particle.state[:2], dt)
        elif crossed_x2:
            fun = lambda y: particle.state[2] / particle.state[3] *\
                (y - particle.state[1]) + particle.state[0] - self.Lwidth[1]
            root = op.brentq(fun, -0.1 + self.Lheight[1], self.Lheight[2] + 0.1)
            particle.state[0] = self.Lwidth[1]
            particle.state[1] = root
            particle.state[2] *= -1
            # print('crossed_x2', old_state[:2], particle.state[:2], dt)
        elif crossed_x3:
            fun = lambda y: particle.state[2] / particle.state[3] *\
                (y - particle.state[1]) + particle.state[0] - self.Lwidth[2]
            root = op.brentq(fun, -0.1 + self.Lheight[0], self.Lheight[1] + 0.1)
            particle.state[0] = self.Lwidth[2]
            particle.state[1] = root
            particle.state[2] *= -1
            # print('crossed_x3', old_state[:2], particle.state[:2], dt)
        elif crossed_y1:
            fun = lambda x: particle.state[3] / particle.state[2] *\
                (x - particle.state[0]) + particle.state[1]
            root = op.brentq(fun, -0.1 + self.Lwidth[0], self.Lwidth[2] + 0.1)
            particle.state[0] = root
            particle.state[1] = self.Lheight[0]
            particle.state[3] *= -1
            # print('crossed_x1', old_state[:2], particle.state[:2], dt)
        elif crossed_y2:
            fun = lambda x: particle.state[3] / particle.state[2] *\
                (x - particle.state[0]) + particle.state[1] - self.Lheight[1]
            root = op.brentq(fun, -0.1 + self.Lwidth[1], self.Lwidth[2] + 0.1)
            particle.state[0] = root
            particle.state[1] = self.Lheight[1]
            particle.state[3] *= -1
            # print('crossed_y2', old_state[:2], particle.state[:2], dt)
        elif crossed_y3:
            fun = lambda x: particle.state[3] / particle.state[2] *\
                (x - particle.state[0]) + particle.state[1] - self.Lheight[2]
            root = op.brentq(fun, -0.1 + self.Lwidth[0], self.Lwidth[1] + 0.1)
            particle.state[0] = root
            particle.state[1] = self.Lheight[2]
            particle.state[3] *= -1
            # print('crossed_y3', old_state[:2], self.state[:2], dt)

if __name__ == '__main__':
    table = LTable(initX=1., initY=1., initXVel=6, initYVel=7, trace=True)
    table.main()
