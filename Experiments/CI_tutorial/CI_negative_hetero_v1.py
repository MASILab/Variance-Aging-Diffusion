import imageio
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
import statsmodels.api as sm
from statsmodels.stats.outliers_influence import summary_table

def fig2data(fig):
    fig.canvas.draw()
    w, h = fig.canvas.get_width_height()
    buf = np.frombuffer(fig.canvas.tostring_argb(), dtype=np.uint8)
    buf.shape = (w, h, 4)
    buf = np.roll(buf, 3, axis=2)
    return buf


seed = 0
np.random.seed(seed)
num_total = 2000

x = np.random.normal(loc=100, scale=30, size=num_total)
noise = np.zeros_like(x)
for i in range(num_total):
    noise[i] = np.random.normal(loc=0,scale=x[i])
y = noise

# Loop
sample_size = 50
figs_data = []
for i in range(60):
    idxs = np.random.choice(num_total, size=sample_size, replace=False)
    x_s = x[idxs]
    y_s = y[idxs]

    fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(7,7))

    ax.scatter(x, y, c='b', s=1, alpha=0.2, label='Unobserved Data')
    ax.scatter(x_s, y_s, c='r',s=3, label='Observed Data')
    ax.set_title('Observed Data and Ordinary Least Square (OLS) Regression')
    ax.set_ylabel('y')
    ax.set_xlabel('x')
    ax.set_ylim(top=np.max(y)+20,bottom=np.min(y)-20)

    # Regression line and CI
    X = np.column_stack((np.ones_like(x_s), x_s))
    Y = y_s
    results = sm.OLS(Y,X).fit()
    st, dat, ss2 = summary_table(results, alpha=0.05)
    predict_ci_low, predict_ci_upp = dat[:, 4:6].T

    sorting = np.argsort(x_s)
    x_sorted = x_s[sorting]
    y_pred_sorted = results.fittedvalues[sorting]
    predict_ci_low_sorted = predict_ci_low[sorting]
    predict_ci_upp_sorted = predict_ci_upp[sorting]

    ax.plot(x_sorted, y_pred_sorted, 'r-', label='OLS Regression')
    ax.plot(x_sorted, predict_ci_low_sorted, 'k--', linewidth=1, label='95% Confidence Intervals')
    ax.plot(x_sorted, predict_ci_upp_sorted, 'k--', linewidth=1)
    ax.legend(loc='upper left')
    ax.set_xlabel('x')
    ax.set_ylabel('y')

    ax.text(0.98, 0.04, "p-values: [{0:.5f}, {1:.5f}]".format(results.pvalues[0],results.pvalues[1]), 
            transform=ax.transAxes, fontsize=9,
            verticalalignment='top', horizontalalignment='right')
    
    figs_data.append(fig2data(fig))

    # Clear the axes and the figure
    ax.cla()
    fig.clf()
    
# Save the figures as a GIF using imageio
imageio.mimsave('/home/local/VANDERBILT/gaoc11/Projects/Variance-Aging-Diffusion/Experiments/CI_tutorial/CI_negative_hetero_v1.gif', figs_data, format='gif', fps=1)
