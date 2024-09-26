import numpy as np
import matplotlib .pyplot as plt
# Generate points
x = np.array ([0.1 , 0.5, 1, 1.2, 2, 3])
y = np.array ([2.2 , 2.1, 3.9, 5.3, 9.1, 17.5])

# compute mean of parameters
# -- Question 3a(i) --
# mu = ?
sigma = 1
Phi = np.array ([[1 ,xx , xx **2] for xx in x])
aux = np.linalg.pinv(np.eye (3) + 1 / sigma **2 * Phi.T @ Phi)
mu = aux @ (1 / sigma **2 * Phi.T @ y[:, None ])
print(mu)
# --------------------
# compute covariance
# -- Question 3a(i) --
# cov = ?
cov = np.linalg.pinv(np.eye (3) + 1 / sigma **2 * Phi.T @ Phi)
print(cov)
# --------------------