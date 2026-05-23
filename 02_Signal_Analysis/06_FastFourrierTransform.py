'''
FFT = Fast Fourrier Transform

There is a massive misconception among students that the FFT is a completely different mathematical formula from the DFT.

FFT equals DFT. It just depends on how your computer or the software computes the spectrum.
It is simply a brilliantly efficient algorithm (a shortcut) to calculate the exact same DFT formula we just learned.

################################################

The Problem: The "Brute Force" DFT is Too Slow

X[k] = sum_{n=0}^{N-1} [ x[n] * e^(-i * 2*pi * k * n / N) ]

To calculate the amplitude for one single frequency bin ``k``, the computer must do N multiplications and additions.
Because there are N total frequency bins to calculate
-> The total math operation is NxN = N^2

################################################

The Magic of FFT: "Divide and Conquer"

In 1965, Cooley and Tukey popularized the FFT algorithm.
They realized that the complex exponential math e^(-i....) inside the DFT formula is highly symmetric and repetitive.
-> Instead of calculating the whole sum at once, the FFT uses a "Divide and Conquer" strategy.

1. FFT first splits the N data points into ``even`` indices and ``odd`` indices
2. It splits those halves into halves again, recursively, until it is just calculating tiny 2-point DFTs.
3. It then stitches the results back together, completely skipping the redundant, repetitive math.

=> The Result: The number of operations drops from N^2 to N*log(N)
'''

import numpy as np
import time

# Create a dummy signal (N must be a power of 2 for classic FFT to be most efficient)
N = 4096
t = np.linspace(0, 1, N)
x_t = np.sin(2 * np.pi * 50 * t) + 0.5 * np.sin(2 * np.pi * 120 * t)

print(f"Total Data Points (N): {N}\n") # 4096

#--------------------------------------------------------------------------------#
# 1. THE "BRUTE FORCE" DFT (O(N^2) complexity)
#--------------------------------------------------------------------------------#
# To prevent your computer from freezing, we will ONLY calculate the first 100
# frequency bins using the raw mathematical formula via matrix multiplication.
start_time = time.time()

k_values = np.arange(100)      # Only computing 100 bins
n_values = np.arange(N)
# Create the N x 100 matrix of complex exponentials
complex_matrix = np.exp(-1j * 2 * np.pi * np.outer(k_values, n_values) / N)
X_dft_partial = np.dot(complex_matrix, x_t)

dft_time = time.time() - start_time
print(f"Brute-Force DFT (only 100 out of {N} bins): {dft_time:.5f} seconds") # 0.01867 seconds


#--------------------------------------------------------------------------------#
# 2. THE FFT ALGORITHM (O(N log N) complexity)
#--------------------------------------------------------------------------------#
# np.fft.fft computes ALL N frequency bins instantly using the recursive FFT trick
start_time = time.time()

X_fft_full = np.fft.fft(x_t)

fft_time = time.time() - start_time
print(f"Optimized FFT (ALL {N} bins):             {fft_time:.7f} seconds") # 0.0016351 seconds

#--------------------------------------------------------------------------------#
# 3. PROOF THAT THEY ARE MATHEMATICALLY IDENTICAL
#--------------------------------------------------------------------------------#
# Let's compare the first 100 bins of both methods
difference = np.max(np.abs(X_dft_partial - X_fft_full[:100]))
print(f"\nMaximum mathematical difference between DFT and FFT: {difference:.2e}") # 1.26e-11
print("(Note: 1e-14 is essentially zero, caused by floating-point rounding)")
