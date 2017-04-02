from matplotlib import pyplot as plt
from matplotlib import animation
import numpy as np
from scipy import optimize as op
from AbstractTable import AbstractTable as abT
from matplotlib.collections import PatchCollection



class Lorentz(abT):
    """
    subclass of AbstractTable for the Rectangle table
    """
    def __init__(self, **kwargs):
        super(Lorentz,self).__init__(**kwargs)
        self.maxx = 3
        self.maxy = 3
        self.minx = -3
        self.miny = -3
        self.radius = 1
        self.length = abs(self.minx - self.maxx)
        self.height = abs(self.maxy - self.miny)

    def drawTable(self,ec='none'):
        """
        makes a fig and axes and adds the table as a patch.
        ec should be set to 'k' when generating a preview
        """
        self.fig, self.ax = plt.subplots(figsize=(10, 10))
        self.fig.canvas.set_window_title('Lorentz Billiards Simulation')
        self.ax.set(xlim=[(self.minx - 0.5),(self.maxx + 0.5)],
            ylim=[(self.miny - 0.5),(self.maxy + 0.5)])
        self.ax.axis('off')
        # make table
        # make patch list and add the circle and bounding box
        patches=[]
        patches.append(plt.Rectangle((self.minx, self.miny), self.length,
            self.height, ec='none', lw=1, fc='none'))
        patches.append(plt.Circle((0, 0), self.radius))
        # make collection of patches from list
        self.table = PatchCollection(patches)
        # have to set these parameters because the collection resets everything
        self.table.set_edgecolor(ec)
        self.table.set_linewidth(1)
        self.table.set_facecolor('none')
        # add the patches to the axis
        self.ax.add_collection(self.table)
        plt.axis('equal')


    def step(self,particle, dt):
        """
        checks for collissions and updates velocities accordinly for one
        particle
        """
        # check for crossing boundary
        crossed_x1 = particle.state[0] < self.minx
        crossed_x2 = particle.state[0] > self.maxx
        crossed_y1 = particle.state[1] < self.miny
        crossed_y2 = particle.state[1] > self.maxy

        if crossed_x1:
            if particle.state[3] != 0:
                fun = lambda y: particle.state[2] / particle.state[3] * \
                                (y - particle.state[1]) + particle.state[0]
                root = op.brentq(fun, self.miny-0.1, self.maxy + 0.1)
                particle.state[1] = root

            particle.state[0] = self.minx
            particle.state[2] *= -1
        elif crossed_x2:
            if particle.state[3] != 0:
                fun = lambda y: particle.state[2] / particle.state[3] * (y - particle.state[1]) + particle.state[0] - self.maxx
                root = op.brentq(fun, self.miny-0.1, self.maxy + 0.1)
                particle.state[1] = root

            particle.state[0] = self.maxx
            particle.state[2] *= -1

        if crossed_y1:
            if particle.state[2] != 0:
                fun = lambda x: particle.state[3] / particle.state[2] * (x - particle.state[0]) + particle.state[1]
                root = op.brentq(fun, self.minx-0.1, self.maxx + 0.1)
                particle.state[0] = root
            particle.state[1] = self.miny
            particle.state[3] *= -1
        elif crossed_y2:
            if particle.state[2] != 0:
                fun = lambda x: particle.state[3] / particle.state[2] * \
                                (x - particle.state[0]) + particle.state[1] - self.maxy
                root = op.brentq(fun, self.minx-0.1, self.maxx + 0.1)
                particle.state[0] = root
            particle.state[1] = self.maxy
            particle.state[3] *= -1

        # check for crossing boundary
        if np.hypot(particle.state[0], particle.state[1]) < self.radius:
            if particle.state[2] != 0 and abs(particle.state[3] / particle.state[2]) <= 1:
                m = particle.state[3] / particle.state[2]
                intercept = m * -particle.state[0] + particle.state[1]

                # discriminant
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
                # print((particle.state[0], particle.state[1]))

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

if __name__ == '__main__':
    table = Lorentz()
    table.main()
