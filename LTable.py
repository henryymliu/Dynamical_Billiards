from matplotlib import pyplot as plt
from matplotlib import animation
import numpy as np

class LTable(object):
    """docstring for LTable."""
    def __init__(self, **kwargs):
        super().__init__()
        self.parameters = kwargs


    def step(self,dt):
        old_state = np.array(self.state[:2])
        self.state[:2] += dt * self.state[2:]
        # check for crossing boundary
        crossed_x1 =  self.state[0] < 0
        crossed_x2 = (self.state[0] > 2  and self.state[1] >= 2 and old_state[0]<=2 )
        crossed_x3 = (self.state[0] > 4  and self.state[1] < 2)
        crossed_y1 =                         self.state[1] < 0
        crossed_y2 = (self.state[0] >= 2 and self.state[1] > 2 and old_state[0]>=2)
        crossed_y3 = (self.state[0] < 2  and self.state[1] > 6 )

        if crossed_x1:
            self.state[0]=0
            self.state[2]*=-1
            #print('crossed_x1', old_state[:2], self.state[:2], dt)
        elif crossed_x2:
            self.state[0]=2
            self.state[2]*=-1
            #print('crossed_x2', old_state[:2], self.state[:2], dt)
        elif crossed_x3:
            self.state[0]=4
            self.state[2]*=-1
            #print('crossed_x3', old_state[:2], self.state[:2], dt)
        elif crossed_y1:
            self.state[1]=0
            self.state[3]*=-1
            #print('crossed_x1', old_state[:2], self.state[:2], dt)
        elif crossed_y2:
            self.state[1]=2
            self.state[3]*=-1
            #print('crossed_y2', old_state[:2], self.state[:2], dt)
        elif crossed_y3:
            self.state[1]=6
            self.state[3]*=-1
            #print('crossed_y3', old_state[:2], self.state[:2], dt)



    def main(self):
        x =np.array([0,4,4,2,2,0,0])
        y=np.array([0,0,2,2,6,6,0])
        
        fig, ax=plt.subplots()
        ax.set(xlim=[-0.4,5],ylim=[-0.4,7])
        ax.axis('off')
        table,=ax.plot(x,y, 'k-',lw=1)

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
            table.set_data([],[])
            path.set_data([],[])
            return particle, table, path

        def animate(i):
            """perform animation step"""
            if self.parameters['trace']:
                self.pathx=np.append(self.pathx,self.state[0])
                self.pathy=np.append(self.pathy,self.state[1])
            self.step(dt)
            # update pieces of the animation
            table.set_data(x,y)
            particle.set_data(self.state[0], self.state[1])
            path.set_data(self.pathx,self.pathy)
            return particle, table, path

        ani = animation.FuncAnimation(fig, animate, frames=600,
                              interval=0.001, blit=True, init_func=init)


        plt.show()

if __name__ == '__main__':
    table=LTable(initX=1.,initY=1.,initXVel=1.7,initYVel=2.4, trace = True)
    table.main()
