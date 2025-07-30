import random
from scipy.stats import norm

# Create a trapezoidal modulating function
def modulator(t, t1, t2, t3, t4):
    if t <= t1 or t >= t4:
        return 0.0
    elif t < t2:
        return (t-t1)/(t2-t1)
    elif t < t3:
        return 1.0
    else:
        return 1.0-(t-t3)/(t4-t3)

def WhiteNoise(dt,Tfinal,tup,tdown,seed=None):

    if seed is not None:
        random.seed(seed)

    Npts = int(Tfinal/dt)

    noise = [norm.ppf(random.random()) for i in range(Npts)]

    t1 = 0; t2 = tup; t3 = Tfinal-tdown; t4 = Tfinal
    modnoise = [noise[i]*modulator(dt*(i+1),t1,t2,t3,t4) for i in range(Npts)]

    return modnoise

if __name__ == '__main__':
    y = WhiteNoise(0.5,10,2,2)
    print(y)
