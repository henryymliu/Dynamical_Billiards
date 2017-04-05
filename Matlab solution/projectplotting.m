%Initial Conditions
x0=0;
y0=0;
x0p=1;
y0p=-1.1;
timelength=400;
tspace=linspace(0,timelength,10000); % Change this at your discretion for number of interations
n=4;
%%X solution
syms x(t)
[W]=odeToVectorField(diff(x,2)==-n*x^(n-1));
N=matlabFunction(W,'vars',{'t','Y'});
sol=ode45(N,[0 timelength],[x0 x0p]);
xpath=deval(sol,tspace,1);
%%Y solution
syms y(t)
[V]=odeToVectorField(diff(y,2)==-n*y^(n-1));
M=matlabFunction(V,'vars',{'t','Y'});
sol=ode45(M,[0 timelength],[y0 y0p]);
ypath=deval(sol,tspace,1);

plot(xpath,ypath);
axis([-1.5 1.5 -1.5 1.5]);shg;