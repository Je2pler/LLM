# You will be asked to solve a Bayesian Linear Regression problem.

 

# The following code gives the structure for your implementation. The code is also available in the resource Programming - Problem 3.

 

import numpy as np
import matplotlib.pyplot as plt
# Generate points
x = np.array([0.1, 0.5, 1, 1.2, 2, 3])
y = np.array([2.2, 2.1, 3.9, 5.3, 9.1, 17.5])
#
# compute mean of parameters
# -- Question 3a(i) --
# mu = ?

sigma = 1
Phi = np. array ([[1 ,xx , xx **2] for xx in x])
aux = np. linalg .pinv(np.eye (3) + 1 / sigma **2 * Phi.T @ Phi)
mu = aux @ (1 / sigma **2 * Phi.T @ y[:, None ])
print(mu)
# --------------------

# compute covariance
# -- Question 3a(i) --
# cov = ?
cov = np. linalg .pinv(np.eye (3) + 1 / sigma **2 * Phi.T @ Phi)
print(cov)
# --------------------
#
# Compute the mean and variance of the test points
x_test = np.linspace(0, 4, 100)
#
# Input provided in the exercise
# -- Question 3b --
Phi_test = np. array ([[1 ,xx , xx **2] for xx in x_test ])
mean_test = ( Phi_test @ mu). flatten ()
std_test = np.sqrt(np.diag( Phi_test @ cov @ Phi_test .T) +
sigma **2)
# ------------------
# Plot
plt.plot(x, y, 'o', color ='black')
plt.plot(x_test , mean_test , color ='blue')
plt. fill_between(x_test , mean_test - 1* std_test , mean_test + 1*std_test , alpha = 0.3 , color ='blue')
plt.fill_between (x_test , mean_test - 2* std_test , mean_test + 2*std_test , alpha = 0.3 , color ='blue')
plt.show ()

