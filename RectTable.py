from matplotlib import pyplot as plt
from matplotlib import animation
import numpy as np
from scipy import optimize as op

class RectTable(object):
    """docstring for RectTable."""
    def __init__(self, **kwargs):
        super().__init__()
        self.parameters = kwargs

    #each step increment Position
    def step(self,dt):
        #set new Position
        self.state[:2] += dt * self.state[2:]
        # check for crossing boundary
        crossed_x1 = self.state[0] < 0
        crossed_x2 = self.state[0] > self.maxx
        crossed_y1 = self.state[1] < 0
        crossed_y2 = self.state[1] > self.maxy

        #reset the position to the boundry line
        if crossed_x1:
            fun=lambda y: self.state[2]/self.state[3]*(y-self.state[1])+self.state[0]
            root=op.brentq(fun, -0.1, self.maxy+0.1)
            self.state[0]=0
            self.state[1]=root
            self.state[2]*=-1
        elif crossed_x2:
            fun=lambda y: self.state[2]/self.state[3]*(y-self.state[1])+self.state[0]-self.maxx
            root=op.brentq(fun, -0.1, self.maxy+0.1)
            self.state[0]=self.maxx
            self.state[1]=root
            self.state[2]*=-1

        if crossed_y1:
            fun=lambda x: self.state[3]/self.state[2]*(x-self.state[0])+self.state[1]
            root=op.brentq(fun, -0.1, self.maxx+0.1)
            self.state[0]=root
            self.state[1]=0
            self.state[3]*=-1
        elif crossed_y2:
            fun=lambda x: self.state[3]/self.state[2]*(x-self.state[0])+self.state[1]-self.maxy
            root=op.brentq(fun, -0.1, self.maxx+0.1)
            self.state[0]=root
            self.state[1]=self.maxy
            self.state[3]*=-1



    def main(self):
        self.maxx=self.parameters['width']
        self.maxy=self.parameters['height']
        #TODO this needs tweaking to make aspect always the same
        fig, ax=plt.subplots(figsize=(10,10))
        fig.canvas.set_window_title('Rectangle Billiards Simulation')
        ax.set(xlim=[-0.5,self.maxx+0.5],ylim=[-0.5,self.maxy+0.5])
        #ax.axis('off')
        #make table
        table=plt.Rectangle((0,0), self.maxx, self.maxy,ec='none', lw=1, fc='none')
        ax.add_patch(table)

        #define particle and path objects
        particle, = ax.plot([], [], 'ro', ms=6)
        path, =ax.plot([],[], 'r-',lw=1)
        #define time step for 30 fps
        dt=1/30
        #set initial conditons
        self.state=np.array([self.parameters['initX'],self.parameters['initY'],
            self.parameters['initXVel'],self.parameters['initYVel']])
        self.pathx=np.array([])
        self.pathy=np.array([])

        #init function for animation
        def init():
            """initialize animation"""

            particle.set_data([], [])
            table.set_edgecolor('none')
            path.set_data([],[])
            return particle, table, path

        def animate(i):
            """perform animation step"""
            #trace the particle if check box is selected
            if self.parameters['trace']:
                self.pathx=np.append(self.pathx,self.state[0])
                self.pathy=np.append(self.pathy,self.state[1])
            self.step(dt)
            # update pieces of the animation
            table.set_edgecolor('k')
            particle.set_data(self.state[0], self.state[1])
            path.set_data(self.pathx,self.pathy)
            return particle, table, path
        #define animation
        ani = animation.FuncAnimation(fig, animate, frames=600,
                              interval=np.ceil((1/self.parameters['playbackSpeed'])*10**3), blit=True, init_func=init)


        plt.show()

if __name__ == '__main__':
    table=RectTable()
    table.main()
