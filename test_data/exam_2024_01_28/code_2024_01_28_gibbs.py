import numpy as np
import matplotlib.pyplot as plt

L = 1000 # Number of samples
x = np.zeros(L)
y = np.zeros(L)

# Compute the parameters in 3a
m = np.array([5 , -5])
S = np.array([[4 , -1],[-1, 1]])

a = -1
b = 0
sxy2 = 3

c = -0.25
d = -3.75
syx2 = 0.75

 # Gibbs sampler
for k in range (L -1):
# Sample from p(x|y)
    x[k+1] = np. random . randn (1)*np.sqrt(sxy2)+a*y[k]+b
 # Sample from p(y|x)
    y[k+1] = np. random . randn (1)*np.sqrt(syx2)+c*x[k+1]+d

# Plot the results
fig,(ax1 , ax2) = plt.subplots (2)
ax1.set_title ('Sample trajectories')
ax1.plot(x, label ='x')
ax1.plot(y, label ='y')
ax1.set( xlabel ='Sample number')
ax1.legend ()
ax2.plot(x,y,'.')
ax2.set_title ('Samples')
ax2.set( xlabel ='x',ylabel ='y')
ax2.set_aspect ('equal', 'box')
fig.tight_layout()
plt.show ()

# Optional : Compute sample mean and covariance matrix .
X = np.c_[x,y]
X = X[5: ,:] # Exclude burn -in

# Compute the mean and covariance
print (np.mean(X,axis = 0))
# [ 5.15457107 -5.01908503]
print (np.cov(X.T))
# [[ 3.89703182 -0.93740488]
# [ -0.93740488 0.96146407]]