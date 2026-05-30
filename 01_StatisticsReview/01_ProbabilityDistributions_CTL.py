'''
=============================================================================
 PART 1: PROBABILITY DISTRIBUTIONS & THE CENTRAL LIMIT THEOREM
=============================================================================
1. HISTOGRAMS & BINNING
   To visualize a Probability Density Function (PDF), we use histograms.
   Choosing the right number of bins is critical. Rules like Bendat & Piersol
   or Freedman-Diaconis help estimate the optimal bin count based on sample
   size (N) and data spread to avoid over-smoothing or excessive noise.

2. POISSON & EXPONENTIAL DISTRIBUTIONS
   - Poisson (Discrete): Models the number of events occurring in a fixed
     interval of time/space (e.g., photon arrivals, cell mutations).
   - Exponential (Continuous): Models the WAITING TIME between independent
     Poisson events. Mean = 1/lambda.

3. GAUSSIAN (NORMAL) DISTRIBUTION
   The "bell curve" defined by mean (mu) and standard deviation (sigma).
   The 68-95-99.7 Rule:
   - 68% of data falls within ±1σ
   - 95% falls within ±2σ
   - 99.7% falls within ±3σ

4. MONTE CARLO & THE CENTRAL LIMIT THEOREM (CLT)
   The CLT states that the distribution of sample means (or sums of independent
   variables) converges to a Gaussian distribution as sample size increases,
   REGARDLESS of the original distribution's shape.
   The professor demonstrated this via Monte Carlo simulation by rolling dice.
=============================================================================
'''

import numpy as np
import matplotlib.pyplot as plt
import seaborn as sbn
from scipy import stats

sbn.set_theme(style="whitegrid")

#--------------------------------------------------------------------------------#
# PLOT 1: POISSON & EXPONENTIAL RELATIONSHIP
#--------------------------------------------------------------------------------#

fig1, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

# Poisson: Number of events (e.g., photons arriving per second)
lam = 5.0 # Average rate (lambda)
x_pois = np.arange(0, 20)
pmf_pois = stats.poisson.pmf(x_pois, lam)

ax1.bar(x_pois, pmf_pois, color='skyblue', edgecolor='black', label=rf'Poisson ($\lambda={lam}$)')
ax1.set_title("Poisson Distribution (Discrete Events)", fontsize=14)
ax1.set_xlabel("Number of Events (k)")
ax1.set_ylabel("Probability")
ax1.legend()

# Exponential: Waiting time between those events
x_exp = np.linspace(0, 5, 500)
pdf_exp = stats.expon.pdf(x_exp, scale=1/lam) # Mean = 1/lambda

ax2.plot(x_exp, pdf_exp, color='coral', linewidth=3, label=rf'Exponential (Mean=$1/\lambda = {1/lam:.2f}$)')
ax2.fill_between(x_exp, pdf_exp, color='coral', alpha=0.3)
ax2.set_title("Exponential Distribution (Waiting Times)", fontsize=14)
ax2.set_xlabel("Waiting Time")
ax2.set_ylabel("Probability Density")
ax2.legend()

plt.tight_layout()
plt.show()


#--------------------------------------------------------------------------------#
# PLOT 2: GAUSSIAN & THE 68-95-99.7 RULE
#--------------------------------------------------------------------------------#

fig2, ax3 = plt.subplots(figsize=(10, 6))

mu, sigma = 0, 1
x_norm = np.linspace(-4, 4, 1000)
y_norm = stats.norm.pdf(x_norm, mu, sigma)

ax3.plot(x_norm, y_norm, 'k-', lw=2, label='Standard Normal')

# Shade 68% (±1σ)
ax3.fill_between(x_norm, y_norm, where=(x_norm >= -1) & (x_norm <= 1),
                 color='green', alpha=0.3, label=r'$\pm 1\sigma$ (68.2%)')
# Shade 95% (±2σ)
ax3.fill_between(x_norm, y_norm, where=(x_norm >= -2) & (x_norm <= -1) | (x_norm >= 1) & (x_norm <= 2),
                 color='blue', alpha=0.3, label=r'$\pm 2\sigma$ (95.4%)')
# Shade 99.7% (±3σ)
ax3.fill_between(x_norm, y_norm, where=(x_norm >= -3) & (x_norm <= -2) | (x_norm >= 2) & (x_norm <= 3),
                 color='red', alpha=0.3, label=r'$\pm 3\sigma$ (99.7%)')

ax3.set_title("Gaussian Distribution & Confidence Intervals", fontsize=16)
ax3.set_xlabel("Standard Deviations from Mean (Z-score)")
ax3.set_ylabel("Probability Density")
ax3.legend(loc='upper right')
plt.tight_layout()
plt.show()


#--------------------------------------------------------------------------------#
# PLOT 3: MONTE CARLO & THE CENTRAL LIMIT THEOREM (Rolling Dice)
#--------------------------------------------------------------------------------#
# The professor used dice rolling to prove the CLT.
# A single die is uniformly distributed (flat). But if we roll MULTIPLE dice
# and SUM them, the distribution rapidly becomes a Gaussian bell curve!

fig3, axes = plt.subplots(2, 2, figsize=(12, 10))
axes = axes.flatten()

num_simulations = 10000
dice_counts = [1, 2, 5, 20] # Number of dice rolled per trial

for i, num_dice in enumerate(dice_counts):
    # Monte Carlo Simulation: Roll 'num_dice' dice, 'num_simulations' times
    # np.random.randint(1, 7) simulates a 6-sided die
    rolls = np.random.randint(1, 7, size=(num_simulations, num_dice))
    sums = np.sum(rolls, axis=1)

    # Plot Histogram
    axes[i].hist(sums, bins=30, density=True, color='teal', alpha=0.6, edgecolor='black')

    # Overlay theoretical Gaussian with matching mean and variance
    # Mean of 1 die = 3.5, Variance = 35/12
    theo_mean = num_dice * 3.5
    theo_var = num_dice * (35/12)
    x_fit = np.linspace(sums.min(), sums.max(), 200)
    axes[i].plot(x_fit, stats.norm.pdf(x_fit, theo_mean, np.sqrt(theo_var)),
                 'r-', lw=3, label='Gaussian Fit (CLT)')

    axes[i].set_title(f"Sum of {num_dice} Dice (N={num_simulations} trials)", fontsize=14)
    axes[i].set_xlabel("Sum of Dice")
    axes[i].set_ylabel("Density")
    axes[i].legend()

plt.suptitle("Monte Carlo Proof of the Central Limit Theorem", fontsize=18, y=1.02)
plt.tight_layout()
plt.show()

'''
WHAT TO LOOK FOR:
- Top Left (1 Die): The distribution is completely flat (Uniform).
- Top Right (2 Dice): A triangle shape begins to form.
- Bottom Left (5 Dice): The bell curve is clearly emerging.
- Bottom Right (20 Dice): The distribution is virtually indistinguishable
  from a perfect Gaussian. This proves the CLT: even if the underlying
  physics (a single die) is NOT normal, the sum/average of multiple
  independent measurements WILL BE normal. This is why engineers can
  use Gaussian statistics for almost all measurement errors!
'''
