%Initial Conditions
x0=-0.1;
y0=0.3;
x0p=0.5;
y0p=-0.2;
timelength=1000;
tspace=linspace(0,timelength,30000); % Change this at your discretion for number of interations
n=2;

for n = 12:12
    figure;
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
    legend(strcat('x0=',num2str(x0),', y0=',num2str(y0),', x0p=', num2str(x0p),', y0p=', num2str(y0p),', t=',num2str(timelength)))
    axis([-1.5 1.5 -1.5 1.5]);shg;
    saveas(gcf, strcat('n',num2str(n),'.png'));
end