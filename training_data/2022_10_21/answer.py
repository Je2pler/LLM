import numpy as np
import matplotlib .pyplot as plt

L = 10000 # Number of samples
expected_value = np.zeros(L)


# probabilities:
p = np.array ([[0.3 , 0.1] ,
[0.2 , 0.4]])

print(f'--- Item (a) ---')
e1 = 0
e2 = 0
e3 = 0
for x in range(2):
    for y in range(2):
        e1 += p[x, y] * (x + y)
        e2 += p[x, y] * (x * y ** 2)
        e3 += p[x, y] * x**(y)

print(f'Item i = {e1}')
print(f'Item ii = {e2}')
print(f'Item iii = {e3}')

print(f'--- Item (b) ---')
px = p[1, 0] + p[1, 1]
py = p[0, 1] + p[1, 1]

print(f'P(X = 1) = {px}, P(Y = 1) = {py}')
px_y_equals_0 = p[1, 0] / (1-py)
px_y_equals_1 = p[1, 1] / py
py_x_equals_0 = p[0, 1] / (1-px)
py_x_equals_1 = p[1, 1] / (px)

print(f'P(X=1 | Y=0) = {px_y_equals_0}')
print(f'P(X=1 | Y=1) = {px_y_equals_1}')
print(f'P(Y=1 | X=0) = {py_x_equals_0}')
print(f'P(Y=1 | X=1) = {py_x_equals_1}')

print(f'--- Item (c/d) ---')
# Initialize
sum_of_values = 0.0
x = 1
y = 0

# initialize sampler
rng = np.random. RandomState (0)

# Gibbs sampler
for k in range(L):
    # --- ADD YOUR COMPUTATION BELOW ---
    # Sample from p(x|y) to update x
    px_given_y = px_y_equals_1 if y == 1 else px_y_equals_0
    x = rng.rand () < px_given_y # Sample from bernoulli
    # Sample from p(y|x) to update y
    py_given_x = py_x_equals_1 if x == 1 else py_x_equals_0
    y = rng.rand () < py_given_x # Sample from bernoulli
    # -----------------------------------

    sum_of_values += x * y
    expected_value [k] = 1 / (k+1) * sum_of_values #Expected value of iteration k

# Plot the results
fig , ax1 = plt.subplots (1)
ax1.plot(expected_value , label='')
ax1.set(xlabel='Sample number (L)')
ax1.set(Ylabel='Estimate of E(X*Y)')
fig. tight_layout ()
plt.show ()



"""

i. The burn-in period is the number of iteration it takes before the effect of the initialization vanishes and the sampler instead sample from the stationary distribution.

ii. For a burning period b you would discard the first b samples before start saving them in the vector expected_value.

"""