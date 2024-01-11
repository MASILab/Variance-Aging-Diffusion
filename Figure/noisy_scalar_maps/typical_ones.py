import subprocess
from pathlib import Path

list_seeds = [332,360,453,863,1024,1260,1414,1730]

list_cmaps = ['hot', 'gist_heat', 'afmhot']

path_save_fd = Path('/home/local/VANDERBILT/gaoc11/Projects/Variance-Aging-Diffusion/Figure/noisy_scalar_maps/save')

for c in list_cmaps:
    
    path_cmap_selected_fd = path_save_fd / "{0}_selected".format(c)
    
    subprocess.run(['mkdir', '-p', path_cmap_selected_fd])
    
    for s in list_seeds:
        fn = path_save_fd / c / "seed_{0}.png".format(s)
        subprocess.run(['cp', fn, path_cmap_selected_fd])