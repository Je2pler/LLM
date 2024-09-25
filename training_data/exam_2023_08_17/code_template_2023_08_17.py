import numpy as np
import matplotlib.pyplot as plt
# Generate points
x = np.array([0.1, 0.5, 1, 1.2, 2, 3])
y = np.array([2.2, 2.1, 3.9, 5.3, 9.1, 17.5])
#
# compute mean of parameters
# -- Question 3a(i) --
# mu = ?
# INSERT YOUR ANSWER HERE
# --------------------
#
# compute covariance
# -- Question 3a(i) --
# cov = ?
# INSERT YOUR ANSWER HERE
# --------------------
#
# Compute the mean and variance of the test points
x_test = np.linspace(0, 4, 100)
#
# Input provided in the exercise
# -- Question 3b --
# REPLACE THE VALUES BELLOW
mean_test = x_test # PLACEHOLDER: replace by your solution
std_test = x_test # PLACEHOLDER: replace by your solution
#------------------
#
# Plot
plt.plot(x, y, 'o', color='black')
plt.plot(x_test, mean_test, color='blue')
plt.fill_between(x_test, mean_test - 1*std_test, mean_test + 1*std_test, alpha = 0.3, color='blue')
plt.fill_between(x_test, mean_test - 2*std_test, mean_test + 2*std_test, alpha = 0.3, color='blue')
plt.show()