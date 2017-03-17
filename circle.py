from matplotlib import pyplot as plt
from matplotlib import animation
import numpy as np
from scipy import optimize as op

class CircleTable(object):
    """docstring for CircleTable."""
    def __init__(self, **kwargs):
        super().__init__()
        self.parameters = kwargs


    def step(self,dt):

        #TODO: CHANGE
        self.state[:2] += dt * self.state[2:]
        # check for crossing boundary
        if np.hypot(self.state[0], self.state[1]) > 2:
            #circ = lambda x: np.sqrt(abs(4 - x**2)) - self.state[3]/self.state[2]*(x-self.state[0])+self.state[1]
            #root = op.fsolve(circ, self.state[0])
            #print(root)
            #first quadrant
            #dy/dx
            #intercept = self.state[3] * -self.state[0] / self.state[2] + self.state[1]

            if self.state[2] != 0:
                m = self.state[3] / self.state[2]
                intercept = m * -self.state[0] + self.state[1]

                #discrimanant
                b = 2*m*intercept
                a = m**2 + 1
                c = -4 + intercept**2
                if self.state[0] > 0:
                    root = (-b + np.sqrt(abs(b**2 - 4*a*c)))/(2*a);
                else:
                    root = (-b - np.sqrt(abs(b**2 - 4 * a * c))) / (2 * a);


                self.state[0] = root
                self.state[1] = m * root + intercept
                # print((self.state[0], self.state[1]))

                vel_norm = np.hypot(self.state[0],self.state[1])
                dot = (self.state[2] * self.state[0] + self.state[3] * self.state[1]) / (vel_norm**2)
                self.state[2] = self.state[2] - 2 * dot * self.state[0]
                self.state[3] = self.state[3] - 2 * dot * self.state[1]

                # self.state[3] *= -1/2;
                # self.state[2] *= -1;
                # print((self.state[2], self.state[3]))
                print((self.state[0], self.state[1]))


            elif self.state[3] != 0:
                m = self.state[2] / self.state[3]
                intercept = m * -self.state[1]+ self.state[0]
                # discriminant
                b = 2 * m * intercept
                a = m ** 2 + 1
                c = -4 + intercept ** 2
                if self.state[1] > 0:
                    root = (-b + np.sqrt(abs(b ** 2 - 4 * a * c))) / (2 * a);
                else:
                    root = (-b - np.sqrt(abs(b ** 2 - 4 * a * c))) / (2 * a);

                #vel = [self.state[0], self.state[1]] / vel_norm

                self.state[0] = m * root + intercept
                self.state[1] = root
                # print((self.state[0], self.state[1]))
                vel_norm = np.hypot(self.state[0], self.state[1])
                dot = (self.state[2] * self.state[0] + self.state[3] * self.state[1]) / (vel_norm ** 2)
                self.state[2] = self.state[2] - 2 * dot * self.state[0]
                self.state[3] = self.state[3] - 2 * dot * self.state[1]
                # print((self.state[2], self.state[3]))
                print((self.state[0], self.state[1]))


    def main(self):
        fig, ax=plt.subplots()
        ax.set(xlim=[-2,2],ylim=[-2,2])
        ax.axis('off')
        table=plt.Circle((0,0), 2, fc = 'none')
        plt.axis('equal')
        ax.add_patch(table)

        particle, = ax.plot([], [], 'ro', ms=6)
        path, =ax.plot([],[], 'r-',lw=1)


        dt=1/30
        self.state=np.array([self.parameters['initX'],self.parameters['initY'],
            self.parameters['initXVel'],self.parameters['initYVel']])
        self.pathx=np.array([])
        self.pathy=np.array([])


        def init():
            """initialize animation"""
            particle.set_data([], [])
            table.set_edgecolor('none')
            path.set_data([],[])
            return particle, table, path

        def animate(i):
            """perform animation step"""
            if self.parameters['trace']:
                self.pathx=np.append(self.pathx,self.state[0])
                self.pathy=np.append(self.pathy,self.state[1])
            self.step(dt)
            # update pieces of the animation
            table.set_edgecolor('k')
            particle.set_data(self.state[0], self.state[1])
            path.set_data(self.pathx,self.pathy)
            return particle, table, path

        ani = animation.FuncAnimation(fig, animate, frames=600,
                              interval=0.001, blit=True, init_func=init)

        plt.show()

if __name__ == '__main__':
    table=CircleTable()
    table.main()
