'''
=============================================================================
 PART 2: STATISTICAL INFERENCE, T-TESTS, & CHI-SQUARED
=============================================================================
1. STUDENT'S T-DISTRIBUTION
   Used when sample sizes are small (N < 30) and population variance is
   unknown. It has "heavier tails" than the Gaussian to account for the
   increased uncertainty of small samples. As N -> infinity, it becomes Gaussian.

2. CONFIDENCE INTERVALS & SAMPLE SIZE
   To estimate a population mean within a specific error margin (E), we
   calculate the required sample size: N = (Z * sigma / E)^2.
   (Professor's example: Cell diameter, sigma=0.5, E=0.1 -> N ≈ 100).

3. HYPOTHESIS TESTING (T-TEST)
   We test a Null Hypothesis (H0: no difference) against an Alternative (Ha).
   The p-value is the probability of seeing our data (or more extreme) if H0
   is true. If p < 0.05, we reject H0.

4. CHI-SQUARED GOODNESS-OF-FIT
   Used for categorical data. It compares OBSERVED frequencies against
   EXPECTED theoretical frequencies to see if a model fits the data.
=============================================================================
'''

import numpy as np
import matplotlib.pyplot as plt
import seaborn as sbn
from scipy import stats

sbn.set_theme(style="whitegrid")


#--------------------------------------------------------------------------------#
# PLOT 1: T-DISTRIBUTION VS. STANDARD NORMAL
#--------------------------------------------------------------------------------#

fig1, ax1 = plt.subplots(figsize=(10, 6))
x = np.linspace(-4, 4, 500)

ax1.plot(x, stats.norm.pdf(x, 0, 1), 'k-', lw=3, label='Standard Normal (Z)')
ax1.plot(x, stats.t.pdf(x, df=3), 'r--', lw=2, label='T-distribution (df=3, N=4)')
ax1.plot(x, stats.t.pdf(x, df=10), 'b-.', lw=2, label='T-distribution (df=10, N=11)')
ax1.plot(x, stats.t.pdf(x, df=30), 'g:', lw=2, label='T-distribution (df=30, N=31)')

ax1.set_title("Student's T-Distribution: Accounting for Small Sample Uncertainty", fontsize=16)
ax1.set_xlabel("Test Statistic")
ax1.set_ylabel("Probability Density")
ax1.legend(fontsize=11)
ax1.set_ylim(0, 0.45)

# Highlight the "Heavy Tails"
ax1.fill_between(x, stats.t.pdf(x, df=3), where=(np.abs(x) > 2), color='red', alpha=0.2)
ax1.text(3.2, 0.05, 'Heavy Tails\n(More uncertainty\nfor small N)', color='red', fontsize=12, ha='center')

plt.tight_layout()
plt.show()


#--------------------------------------------------------------------------------#
# PLOT 2: HYPOTHESIS TESTING & P-VALUES (Two-Sample T-Test Concept)
#--------------------------------------------------------------------------------#

fig2, ax2 = plt.subplots(figsize=(10, 6))

# Null Hypothesis Distribution (Mean = 0)
x_h0 = np.linspace(-4, 6, 500)
y_h0 = stats.norm.pdf(x_h0, 0, 1)
ax2.plot(x_h0, y_h0, 'k-', lw=3, label=r'Null Hypothesis ($H_0$: $\mu = 0$)')

# Alternative Hypothesis (Observed Sample Mean = 2.5)
y_ha = stats.norm.pdf(x_h0, 2.5, 1)
ax2.plot(x_h0, y_ha, 'b-', lw=3, label=r'Observed Sample ($\bar{x} = 2.5$)')

# P-value region (Probability of getting >= 2.5 under H0)
p_val = 1 - stats.norm.cdf(2.5, 0, 1)
ax2.fill_between(x_h0, y_h0, where=(x_h0 >= 2.5), color='red', alpha=0.4,
                 label=rf'p-value = {p_val:.4f} (Reject $H_0$ if < 0.05)')

ax2.axvline(2.5, color='blue', linestyle='--', lw=2)
ax2.set_title("Hypothesis Testing: The P-Value", fontsize=16)
ax2.set_xlabel("Measurement Value (Z-score)")
ax2.set_ylabel("Probability Density")
ax2.legend(fontsize=12)
plt.tight_layout()
plt.show()


#--------------------------------------------------------------------------------#
# PLOT 3: CHI-SQUARED GOODNESS-OF-FIT
#--------------------------------------------------------------------------------#

# Imagine a biological experiment expecting a 1:2:1 Mendelian ratio.
categories = ['Phenotype A', 'Phenotype B', 'Phenotype C']
expected_probs = np.array([0.25, 0.50, 0.25])
total_observed = 100
expected_counts = expected_probs * total_observed

# Simulated Observed Data (Slightly off from perfect 25-50-25 due to noise)
observed_counts = np.array([22, 55, 23])

# Calculate Chi-Squared Statistic
chi2_stat, p_value_chi = stats.chisquare(f_obs=observed_counts, f_exp=expected_counts)

fig3, ax3 = plt.subplots(figsize=(10, 6))
x_pos = np.arange(len(categories))
width = 0.35

bars1 = ax3.bar(x_pos - width/2, expected_counts, width, label='Expected (Theory)', color='lightgray', edgecolor='black')
bars2 = ax3.bar(x_pos + width/2, observed_counts, width, label='Observed (Experiment)', color='salmon', edgecolor='black')

ax3.set_title(rf"Chi-Squared Goodness-of-Fit ($\chi^2$ = {chi2_stat:.2f}, p = {p_value_chi:.3f})", fontsize=16)
ax3.set_xticks(x_pos)
ax3.set_xticklabels(categories, fontsize=12)
ax3.set_ylabel("Frequency Count", fontsize=12)
ax3.legend(fontsize=12)

# Add text explaining the result
if p_value_chi > 0.05:
    result_text = "p > 0.05: Fail to reject H0.\nThe data FITS the theoretical model."
    color = 'green'
else:
    result_text = "p < 0.05: Reject H0.\nThe data DOES NOT fit the model."
    color = 'red'

ax3.text(0.5, 0.9, result_text, transform=ax3.transAxes, fontsize=14,
         ha='center', va='top', color=color, fontweight='bold',
         bbox=dict(boxstyle="round", facecolor="white", edgecolor=color, alpha=0.8))

plt.tight_layout()
plt.show()

'''
WHAT TO LOOK FOR:
1. T-DISTRIBUTION: Notice how the red curve (N=4) is much shorter and wider
   than the black Gaussian curve. This "heaviness" in the tails means that
   with small samples, extreme outliers are much more likely to happen by
   pure chance. You need a larger test statistic to claim significance.

2. P-VALUE: The red shaded area is the p-value. It answers the question:
   "If the Null Hypothesis (black line) is completely true, what are the
   odds that random noise would accidentally push my measurement all the
   way out to 2.5?" Because that red area is tiny (p < 0.05), we conclude
   the measurement is statistically significant, not just noise.

3. CHI-SQUARED: This test is strictly for categorical "bins" (like cell types
   or genetic phenotypes). It mathematically penalizes the differences
   between the gray bars (theory) and red bars (reality). A high p-value
   is actually GOOD here—it means your experimental data successfully
   matches your biological model!
'''
