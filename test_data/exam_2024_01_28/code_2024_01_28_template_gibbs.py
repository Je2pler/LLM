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
