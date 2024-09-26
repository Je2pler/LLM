import numpy as np
from scipy.stats import norm , truncnorm , uniform
import matplotlib .pyplot as plt

# target distribution
a = -np.inf
b = -4
def p(x):
    return truncnorm .pdf(x,a,b,loc=0, scale =1)

# proposal distribution
m = -4.25
def q(x):
    return norm.pdf(x,loc=m,scale =0.25)

L = 1000 # number of samples
x = norm.rvs(loc=m,scale =0.25 , size=L) #draw samples
w = p(x)/q(x) # compute weights
w = w/np.sum(w)*L

# plot a weighted histogram
plt.hist(x,weights=w,bins =50, density=True)
# plot the target distribution and the proposal
xv = np.linspace (-6,-3,100)
plt.plot(xv ,p(xv),label='target')
plt.plot(xv ,q(xv),label='proposal')
plt.legend ()
plt.show()