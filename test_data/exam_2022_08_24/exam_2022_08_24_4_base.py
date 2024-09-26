import numpy as np
from scipy.stats import norm, truncnorm, uniform
import matplotlib.pyplot as plt

# target distribution
a = -np.inf
b = 0
def p(x):
    return truncnorm.pdf(x,a,b,loc=0,scale=1)

L = 1000 # number of samples
x = norm.rvs(loc=0,scale=1,size=L) #draw samples
w = (x < b) # compute weights
w = w/np.sum(w)*L # normalize weights

# plot a weighted histogram
plt.hist(x,weights=w,bins=50,density=True)

# plot the target distribution and the samples
xv = np.linspace(-8,8,100)
plt.plot(xv,p(xv))
plt.show()