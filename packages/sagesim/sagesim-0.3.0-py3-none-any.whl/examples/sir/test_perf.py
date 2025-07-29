import numpy as np
import cupy as cp
import time

A = [0, 1, 2]
B = np.array([0, 1, 2])
C = cp.array([0, 1, 2])

# Timing for list A
start_time = time.time()
for i in range(1000):
    A.append(3)
list_time = time.time() - start_time

# Timing for numpy array B
start_time = time.time()
for i in range(1000):
    B = np.append(B, 3)
numpy_time = time.time() - start_time

# Timing for cupy array C
start_time = time.time()
for i in range(1000):
    C = cp.append(C, 3)
cupy_time = time.time() - start_time

print(f"List append time: {list_time:.6f} seconds")
print(f"Numpy append time: {numpy_time:.6f} seconds")
print(f"Cupy append time: {cupy_time:.6f} seconds")
