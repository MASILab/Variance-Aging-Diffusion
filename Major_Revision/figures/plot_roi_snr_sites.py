import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from multiprocessing import Pool


def raincloud_plot(idx):
    lut = pd.read_csv('/home-nfs2/local/VANDERBILT/gaoc11/Projects/Variance-Aging-Diffusion/Data/LUT_abbr/EveType1_LUT.csv')
    roi_name = lut.loc[lut['id']==idx, 'ROI_rename'].values[0]
    roi_name_abbr = lut.loc[lut['id']==idx, 'ROI_abbr'].values[0]
    
    df = pd.read_csv('/home-nfs2/local/VANDERBILT/gaoc11/Projects/Variance-Aging-Diffusion/Major_Revision/data/data_site_motion_fa-std_snr.csv')
    df = df.loc[df['dataset']=='BLSA', ['site', f'EveType1-{idx}-SNR']].copy()
    df['site'] = df['site'].str.replace('blsa_', '').astype(int).astype(str)
    
    fig, ax = plt.subplots(1, 1, figsize=(2, 2), tight_layout=True)
    ax = sns.violinplot(
        data = df, x='site', y=f'EveType1-{idx}-SNR',
        cut=0, width=0.9, inner=None, saturation=1, linewidth=0,
        native_scale=True, ax=ax,
        )

    for item in ax.collections:
        x0, y0, width, height = item.get_paths()[0].get_extents().bounds
        item.set_clip_path(plt.Rectangle((x0, y0), width/2, height, transform=ax.transData))
        
    num_items = len(ax.collections)
    ax = sns.stripplot(
        data = df, x='site', y=f'EveType1-{idx}-SNR',
        jitter=0.2, color = 'tab:blue', alpha=0.25, size=1, legend=False,
        native_scale=True, ax=ax,
        )

    for item in ax.collections[num_items:]:
        item.set_offsets(item.get_offsets() + (0.25,0))

    ax = sns.boxplot(
        data = df, x='site', y=f'EveType1-{idx}-SNR',
        width=0.2, linecolor='black', showfliers=False,
        boxprops=dict(facecolor=(0,0,0,0),
                    linewidth=0.75, zorder=3),
        whiskerprops=dict(linewidth=0.75),
        capprops=dict(linewidth=0.75),
        medianprops=dict(linewidth=0.75, color='orange', zorder=4),
        native_scale=True, ax=ax,
        )

    ax.tick_params(labelsize=9, which='both')
    ax.set_xlabel('scanner ID', fontsize=9)
    ax.set_ylabel('signal-to-noise ratio', fontsize=9)
    ax.set_title(f"{roi_name_abbr}", fontsize=9)

    save_png = f'/home-nfs2/local/VANDERBILT/gaoc11/Projects/Variance-Aging-Diffusion/Major_Revision/figures/roi_snr_v1/each_roi/{idx}_{roi_name}.png'
    fig.savefig(save_png, dpi=300)
    print(f"Saved {save_png}")


if __name__ == '__main__':
    lut = pd.read_csv('/home-nfs2/local/VANDERBILT/gaoc11/Projects/Variance-Aging-Diffusion/Data/LUT_abbr/EveType1_LUT.csv')
    list_idx = lut['id'].values.tolist()

    with Pool(processes=6) as pool:
        for _ in pool.imap(raincloud_plot, list_idx):
            pass
