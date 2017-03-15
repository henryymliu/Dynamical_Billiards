from matplotlib import pyplot as plt
from matplotlib import animation
import numpy as np

class SquareTable(object):
    """docstring for SquareTable."""
    def __init__(self, **kwargs):
        super().__init__()
        self.parameters = kwargs


    def step(self,dt):
        self.state[:2] += dt * self.state[2:]
        # check for crossing boundary
        crossed_x1 = self.state[0] < 0
        crossed_x2 = self.state[0] > 2
        crossed_y1 = self.state[1] < 0
        crossed_y2 = self.state[1] > 2

        if crossed_x1:
            self.state[0]=0
            self.state[2]*=-1
        elif crossed_x2:
            self.state[0]=2
            self.state[2]*=-1

        if crossed_y1:
            self.state[1]=0
            self.state[3]*=-1
        elif crossed_y2:
            self.state[1]=2
            self.state[3]*=-1



    def main(self):
        fig, ax=plt.subplots()
        ax.set(xlim=[-0.4,2.4],ylim=[-0.4,2.4])
        ax.axis('off')
        table=plt.Rectangle((0,0), 2, 2,ec='none', lw=1, fc='none')
        ax.add_patch(table)

        particle, = ax.plot([], [], 'ro', ms=6)
        path, =ax.plot([],[], 'r-',lw=1)

        dt=1/1000
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
    table=SquareTable()
    table.main()
