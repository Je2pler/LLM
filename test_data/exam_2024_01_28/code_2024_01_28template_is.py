import numpy as np
import scipy
import matplotlib.pyplot as plt

def p(x):
   # The unnormalised target density
   return np.exp(-x ** 4)

def q(x,sigma):
   # The proposal density.
   return scipy.stats.norm.pdf(x, 0, sigma)

# Standard deviation of proposal
sigma = 1

# Plot p(x) and q(x)
xs = np.linspace(-7, 7, 1000)
plt.plot(xs, p(xs), label='Target p(x)')
plt.plot(xs, q(xs,sigma), label='Proposal q(x)')
plt.legend() 
plt.show() 

# Implement your importance sampling here 
 