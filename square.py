from matplotlib import pyplot as plt
from matplotlib import animation
import numpy as np

class SquareTable(object):
    """docstring for SquareTable."""
    def __init__(self, **kwargs):
        super(SquareTable, self).__init__()
        self.parameters = kwargs

    def tableX(self,t_array):
        x=np.empty(t_array.size)
        for i,t in enumerate(t_array):
            if t >= 0. and t<=1. :
                x[i]=2.*t
            elif t>1. and t<=2. :
                x[i]=2.
            elif t>2. and t<=3. :
                x[i]=2.-(2.*(t-2))
            elif t>3. and t<=4. :
                x[i]=0.
            else:
                x[i]=0.
        return x

    def tableY(self,t_array):
        y=np.empty(t_array.size)
        for i,t in enumerate(t_array):
            if t >= 0. and t<=1. :
                y[i]=0.
            elif t>1. and t<=2. :
                y[i]=(2.*t)-2
            elif t>2. and t<=3. :
                y[i]=2.
            elif t>3. and t<=4. :
                y[i]=2.-(2.*(t-3))
            else:
                y[i]=0.
        return y

    def main(self):
        t1=np.linspace(0.,1.,1000)
        t2=np.linspace(1.,2.,1000)
        t3=np.linspace(2.,3.,1000)
        t4=np.linspace(3.,4.,1000)
        t=np.concatenate((t1,t2,t3,t4))
        x=np.array(self.tableX(t))
        y=np.array(self.tableY(t))
        fig, ax=plt.subplots()
        ax.set(xlim=[-1,3],ylim=[-1,3])
        ax.plot(x,y)
        plt.show()

if __name__ == '__main__':
    table=SquareTable()
    table.main()
