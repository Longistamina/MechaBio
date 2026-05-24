'''
DFT = Discrete Fourrier Transform

The Continuous Fourier Transform (FT) requires integrating from -inf to +inf.
But computers cannot store infinite data, nor can they compute continuous integrals.
-> They only have finite, discrete arrays of numbers (e.g., 1,000 samples collected over 2 seconds).

To solve this, we use the Discrete Fourier Transform (DFT).
In Python, this is computed using the highly optimized Fast Fourier Transform (FFT) algorithm.

##############################################

Instead of continuous integral from -inf to +inf,
DFT use uses a discrete summation (sigma)

X[k] = sum_{n=0}^{N-1} [ x[n] * e^(-i * 2*pi * k * n / N) ]

Where:
x[n] = your discrete time-domain data points
N    = total number of data points
k    = the frequency bin index (0, 1, 2... N-1)

##############################################

However, the DFT mathematically assumes that the finite snippet of data you feed it repeats infinitely.

Imagine you record 1 second of a sine wave and feed it to the DFT,
the DFT doesn't just see that 1 second; it assumes that exact 1-second snippet loops over and over again for all of eternity.
effectively turning your aperiodic snippet into a periodic signal.

##############################################

What happens if your 1-second recording doesn't contain an exact, whole number of wave cycles?

# Perfect Alignment (No Leakage): If you record exactly 5 full cycles of a 5 Hz wave,
  the wave ends exactly where it began (e.g., at zero). When the DFT "loops" it,
  the end connects perfectly to the beginning. The spectrum shows a single, sharp, perfect spike at 5 Hz.

# The Glitch (Spectral Leakage): what if the data is a 5.5 Hz wave sampled for 1 second.
  This results in 5.5 cycles. The wave starts at zero, but ends at its peak.
  When the DFT "loops" this snippet, it creates a violent, instantaneous vertical jump
  from the peak of the end back to the zero of the beginning.

# The Result: Remember the Fourier Series! What creates sharp, vertical jumps? High frequencies!
  Because of this artificial "glitch" at the window edge, the energy of your 5.5 Hz signal "leaks"
  or smears into neighboring frequency bins. Instead of a sharp spike, you get a wide, messy mountain.

##############################################

The Band-Aid: Zero Padding
-> How do we make this smeared mess easier to look at? Zero Padding.

# The Action: You take your original time-domain signal and simply append hundreds or thousands of 0s
              to the end of the array before running the FFT.

# The Math: The frequency resolution (the "width" of your frequency bins) is defined as Δf = fs/N
  (Sampling Rate divided by Total Points). By adding zeros, you artificially inflate N.
  A larger N makes Δf much smaller, giving you more, narrower frequency bins.

# Warning: Zero padding does NOT add new information or fix the leakage.
   It simply interpolates the data. It draws a smooth, high-resolution curve through the smeared leakage points,
   making it easier to visually guess where the true peak is, but the underlying "glitch" is still there.
'''

import numpy as np
import matplotlib.pyplot as plt
import seaborn as sbn

sbn.set_theme(style="darkgrid")

#--------------------------------------------------------------------------------#
# 1. SETUP THE TIME DOMAIN AND SIGNAL
#--------------------------------------------------------------------------------#
fs = 100          # Sampling frequency (100 Hz)
T = 1.0           # Duration of recording (1 second)
N = int(fs * T)   # Total number of data points (100 points)
t = np.linspace(0, T, N, endpoint=False)

# We use 5.5 Hz. In 1 second, this creates 5.5 cycles (a non-integer!).
# This guarantees a discontinuity when the DFT loops it.
f_true = 5.5
x_t = np.sin(2 * np.pi * f_true * t)

#--------------------------------------------------------------------------------#
# 2. THE STANDARD DFT (Using numpy's FFT algorithm)
#--------------------------------------------------------------------------------#
# np.fft.fft computes the Discrete Fourier Transform
X_f = np.fft.fft(x_t)
# np.fft.fftfreq generates the corresponding frequency bins
freqs = np.fft.fftfreq(N, 1/fs)

# We only care about the positive half of the spectrum for physical signals
half_N = N // 2
magnitude = np.abs(X_f[:half_N]) * 2 / N  # Normalize amplitude
f_positive = freqs[:half_N]

#--------------------------------------------------------------------------------#
# 3. ZERO PADDING (The "Smoothing" Trick)
#--------------------------------------------------------------------------------#
# Let's pad the signal with 900 zeros, making the new N = 1000
N_padded = 1000
x_t_padded = np.pad(x_t, (0, N_padded - N), mode='constant')

# Run FFT on the padded signal
X_f_padded = np.fft.fft(x_t_padded)
freqs_padded = np.fft.fftfreq(N_padded, 1/fs)

half_N_pad = N_padded // 2
magnitude_padded = np.abs(X_f_padded[:half_N_pad]) * 2 / N # Note: normalize by original N!
f_positive_padded = freqs_padded[:half_N_pad]

#--------------------------------------------------------------------------------#
# 4. PLOTTING THE RESULTS
#--------------------------------------------------------------------------------#
plt.figure(figsize=(12, 6))

# Plot the Standard DFT (Notice the thick, discrete "smear" of leakage)
plt.stem(f_positive, magnitude, linefmt='red', markerfmt='ro', basefmt=" ",
         label=f'Standard DFT (N={N}) - Spectral Leakage!')

# Plot the Zero-Padded DFT (Notice the smooth curve connecting the leaked bins)
plt.plot(f_positive_padded, magnitude_padded, color='blue', linewidth=2,
         label=f'Zero-Padded DFT (N={N_padded}) - Smoothed Interpolation')

# Mark the true frequency
plt.axvline(f_true, color='green', linestyle='--', linewidth=2, label=f'True Frequency ({f_true} Hz)')

plt.title("Spectral Leakage & Zero Padding (5.5 Hz Signal sampled for 1 second)", fontsize=14)
plt.xlabel("Frequency (Hz)", fontsize=12)
plt.ylabel("Magnitude", fontsize=12)
plt.xlim(0, 15) # Zoom in on the peak
plt.legend(fontsize=11)
plt.tight_layout()
plt.show()
'''
The Red Dots (Standard DFT): Notice how the energy isn't just at 5.5 Hz.
It has "leaked" into 4 Hz, 5 Hz, 6 Hz, and 7 Hz.
If you were trying to measure a tiny 6 Hz biological signal hiding next to this 5.5 Hz signal,
the leakage would completely bury it!
(In real engineering, we use "Windowing functions" like the Hanning window to fade the edges of the signal to zero
to prevent this glitch, which the slides briefly mention).

The Blue Line (Zero Padding): Notice how the blue line passes perfectly through the red dots.
It didn't get rid of the leakage (the energy is still spread out), but by shrinking Δf (making the bins smaller),
it drew a smooth envelope.
-> This makes it much easier for our eyes (and peak-finding algorithms)
   to see that the true center of the mountain is exactly at 5.5 Hz.

Notice we used ``np.fft.fft``.
The Fast Fourier Transform (FFT) is just a clever algorithmic shortcut to calculate the exact same DFT summation formula,
but in a fraction of the time (O(N*log(N)) instead of O(N^2))
'''
