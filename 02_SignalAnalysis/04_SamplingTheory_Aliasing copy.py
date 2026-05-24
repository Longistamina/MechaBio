'''
In the real world, physical signals (like temperature or voltage) are continuous—they exist at every infinite fraction of a second.
But computers can only store discrete numbers.

# Sampling is the process of taking a "snapshot" of the continuous signal at regular intervals.
# 𝑇𝑠 (Sampling Period): The time gap between snapshots (e.g., taking a reading every 0.1 seconds).
# 𝑓𝑠 (Sampling Frequency): How many snapshots you take per second (𝑓𝑠 = 1/𝑇𝑠)
# Mathematical formulation: sampling is equivalent to multiplying your continuous true signal by an Impulse Train
                            (a series of infinite spike functions).

The golden rule: The Nyquist Theorem
# How fast do you need to take snapshots to capture the true shape of a wave?
# The Nyquist Theorem states that your sampling frequency (fs) must be strictly greater than twice the highest frequency (fmax) present in your signal
# fs > 2fmax

######################################################################################

What happens if we break the rule? -> Aliasing occurs
# Aliasing is a distortion where high-frequency components "fold back" and disguise themselves as lower frequencies.
# For example: watch a video of car driving fast, the camera's frame rate (fs) was too slow to catch the true speed of the wheel (fmax)
               -> so your brain (the computer) connects the dots and creates a "fake" slow-moving backward wheel.

# If you sample a true frequency (fmax) at a sampling rate (fs) that is too low,
# the computer will "see" an aliased frequency (f_alias)
# f_alias = |f_true - fs|

######################################################################################

But ow do we know fmax in advance to set our sampling rate?"
-> In real life,  environmental noise makes fmax technically infinite
-> So, engineers work backward:
    1. Define your bandwidth: Decide what frequencies you actually care about (e.g., a human heartbeat is ~1 Hz to 5 Hz).
    2. Use an Anti-Aliasing Filter: Before the signal hits the computer, pass it through an analog Low-Pass Filter
                                   to physically chop off all high-frequency noise above your bandwidth (e.g., block everything above 10 Hz).
    3. Set fs: Now that you've artificially forced fmax = 10 Hz, you safely set your sampling rate to >20 Hz.
'''

import numpy as np
import matplotlib.pyplot as plt
import seaborn as sbn

sbn.set_theme(style="darkgrid")

# 1. The True Continuous Signal (8 Hz)
t_cont = np.linspace(0, 2, 1000) # 2 seconds of high-resolution continuous data
f_true = 8
y_cont = np.cos(2 * np.pi * f_true * t_cont)

# 2. The Sampling Process (Breaking the Nyquist Rule!)
# Nyquist requires fs > 2 * 8 = 16 Hz.
# Let's sample at fs = 7 Hz (Too slow!)
fs = 3.5
t_sample = np.arange(0, 2, 1/fs)
y_sample = np.cos(2 * np.pi * f_true * t_sample)

# 3. The Aliased Signal (The "Fake" wave the computer sees)
# The computer connects the dots and thinks the frequency is |7 - 8| = 1 Hz
n = f_true // fs
f_alias = abs(f_true - n*fs)
y_alias = np.cos(2 * np.pi * f_alias * t_cont)

#--------------------------------------------------------------------------------#
# Plotting the Illusion
#--------------------------------------------------------------------------------#
plt.figure(figsize=(14, 6))

# Plot the true, fast 8 Hz wave
plt.plot(t_cont, y_cont, color='blue', alpha=0.4, linewidth=2, label=f'True Signal ({f_true} Hz)')

# Plot the slow, fake 3 Hz wave that the computer "thinks" is there
plt.plot(t_cont, y_alias, color='red', linestyle='--', linewidth=3, label=f'Aliased Signal ({f_alias} Hz)')

# Plot the actual discrete data points we collected
plt.stem(t_sample, y_sample, linefmt='black', markerfmt='ko', basefmt=" ", label='Sampled Data Points')

plt.title("Aliasing: When Sampling Too Slowly Creates a Fake Signal", fontsize=16)
plt.xlabel("Time (seconds)", fontsize=12)
plt.ylabel("Amplitude", fontsize=12)
plt.legend(fontsize=12, loc='upper right')
plt.tight_layout()
plt.show()
