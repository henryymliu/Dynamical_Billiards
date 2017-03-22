import numpy as np
from matplotlib import animation
from matplotlib import pyplot as plt
from AbstractTable import AbstractTable as abT

class CircleTable(abT):
    """docstring for CircleTable."""

    def __init__(self, **kwargs):
        super(CircleTable,self).__init__(**kwargs)
        self.radius = 2

    def drawTable(self,ec='none'):
        self.fig, self.ax = plt.subplots(figsize=(10,10))
        self.fig.canvas.set_window_title('Circle Billiards Simulation')
        self.ax.set(xlim=[-2, 2], ylim=[-2, 2])
        self.ax.axis('off')
        self.table = plt.Circle((0, 0), self.radius, fc='none',ec=ec)
        plt.axis('equal')
        self.ax.add_patch(self.table)

    def step(self, particle, dt):
        # particle.state[:2] += dt * particle.state[2:]
        # check for crossing boundary
        if np.hypot(particle.state[0], particle.state[1]) > 2:
            # circ = lambda x: np.sqrt(abs(4 - x**2)) - particle.state[3]/particle.state[2]*(x-particle.state[0])+particle.state[1]
            # root = op.fsolve(circ, particle.state[0])
            # print(root)
            # first quadrant
            # dy/dx
            # intercept = particle.state[3] * -particle.state[0] / particle.state[2] + particle.state[1]

            if abs(particle.state[3] / particle.state[2]) <= 1:
                m = particle.state[3] / particle.state[2]
                intercept = m * -particle.state[0] + particle.state[1]

                # discrimanant
                b = 2 * m * intercept
                a = m ** 2 + 1
                c = -self.radius ** 2 + intercept ** 2

                # choose root based on proximity with x
                root = -b / (2 * a)
                dis = (np.sqrt(np.fabs(b ** 2 - 4 * a * c))) / (2 * a)
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
                # print(np.hypot(particle.state[2], particle.state[3]))


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
                # print(np.hypot(particle.state[2], particle.state[3]))

    # def main(self):
    #     # self.radius = self.parameters['radius']
    #     fig, ax = plt.subplots()
    #     ax.set(xlim=[-2, 2], ylim=[-2, 2])
    #     ax.axis('off')
    #     table = plt.Circle((0, 0), self.radius, fc='none')
    #     plt.axis('equal')
    #     ax.add_patch(table)
    #
    #     particle, = ax.plot([], [], 'ro', ms=6)
    #     path, = ax.plot([], [], 'r-', lw=1)
    #
    #     dt = 1 / 30
    #     particle.state = np.array([self.parameters['initX'], self.parameters['initY'],
    #                            self.parameters['initXVel'], self.parameters['initYVel']])#.astype(np.longdouble)
    #     self.pathx = np.array([])#.astype(np.longdouble)
    #     self.pathy = np.array([])#.astype(np.longdouble)
    #
    #     def init():
    #         """initialize animation"""
    #         particle.set_data([], [])
    #         table.set_edgecolor('none')
    #         path.set_data([], [])
    #         return particle, table, path
    #
    #     def animate(i):
    #         """perform animation step"""
    #         if self.parameters['trace']:
    #             self.pathx = np.append(self.pathx, particle.state[0])
    #             self.pathy = np.append(self.pathy, particle.state[1])
    #         self.step(dt)
    #         # update pieces of the animation
    #         table.set_edgecolor('k')
    #         particle.set_data(particle.state[0], particle.state[1])
    #         path.set_data(self.pathx, self.pathy)
    #         return particle, table, path
    #
    #     ani = animation.FuncAnimation(fig, animate, frames=600,
    #                                   interval=0.001, blit=True, init_func=init)
    #
    #     plt.show()
    #

if __name__ == '__main__':
    table = CircleTable()
    table.main()
