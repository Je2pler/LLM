import numpy as np
import matplotlib.pyplot as plt

L = 1000 # Number of samples
expected_value = np.zeros(L)

# Initialize
sum_of_values = 0
x = 1
y = 0

# Gibbs sampler
for k in range(L):
    # --- ADD YOUR COMPUTATION BELOW ---
    #   Sample from p(x|y) to update x
    x = x  # <- REPLACE BY YOUR COMPUTATION
    #   Sample from p(y|x) to update y
    y = y  # <- REPLACE BY YOUR COMPUTATION
    # -----------------------------------

    sum_of_values += x * y
    expected_value[k] = 1 / (k+1) * sum_of_values  # Expected value of iteration k

# Plot the results    
fig, ax1 = plt.subplots(1)
ax1.set_title('Sample trajectories')
ax1.plot(expected_value, label='')
ax1.set(xlabel='Sample number')
fig.tight_layout()
plt.show()
