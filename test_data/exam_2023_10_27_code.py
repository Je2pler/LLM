import numpy as np
import scipy
import matplotlib.pyplot as plt 

np.random.seed(1)

def p(x):
# The unnormalised target density
    return np.exp(-x * np.tanh(x ** 3))

def q(x):
# The proposal density.
    return scipy.stats.norm.pdf(x, 0, 3)

# Plot p(x) and q(x)
xs = np.linspace(-7, 7, 1000)
plt.plot(xs, p(xs))
plt.plot(xs, q(xs))
plt.show()

# Implement your importance sampling here


#print(expectation)