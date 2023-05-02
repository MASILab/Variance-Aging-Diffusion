import pylab as pl
import numpy as np
from matplotlib.font_manager import FontProperties

a = np.array([[-2,2]])
pl.figure(figsize=(6.5, 0.5))
img = pl.imshow(a, cmap="RdBu")
pl.gca().set_visible(False)
cax = pl.axes([0.1, 0.3, 0.8, 0.6])
pl.colorbar(orientation="horizontal", cax=cax, ticks=[-2,-1,0,1,2])

# Save
pl.savefig("/home/local/VANDERBILT/gaoc11/Projects/Variance-Aging-Diffusion/Figure/clustermap_v5/colorbar/colorbar_beta.png", dpi=300, bbox_inches='tight')


a = np.array([[0,50]])
pl.figure(figsize=(6.5, 0.5))
img = pl.imshow(a, cmap="hot")
pl.gca().set_visible(False)
cax = pl.axes([0.1, 0.3, 0.8, 0.6])
pl.colorbar(orientation="horizontal", cax=cax, ticks=[0,2,10,25,50])

# Save
pl.savefig("/home/local/VANDERBILT/gaoc11/Projects/Variance-Aging-Diffusion/Figure/clustermap_v5/colorbar/colorbar_pvalue.png", dpi=300, bbox_inches='tight')