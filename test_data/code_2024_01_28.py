code_question_3_IS = """
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
plt.legend() plt.show()"""

code_question_3_GS = """
import numpy as np 
import matplotlib.pyplot as plt 
L = 1000 # Number of samples 
x = np.zeros(L) 
y = np.zeros(L) 

# Write your code here 

# Plot the results    
fig, (ax1, ax2) = plt.subplots(2) 
ax1.set_title('Sample trajectories') 
ax1.plot(x,label='x') 
ax1.plot(y,label='y') 
ax1.set(xlabel='Sample number') 
ax1.legend() 
ax2.plot(x,y,'.') 
ax2.set_title('Samples') 
ax2.set(xlabel='x',ylabel='y') 
ax2.set_aspect('equal', 'box') 
fig.tight_layout() 
plt.show()
"""

