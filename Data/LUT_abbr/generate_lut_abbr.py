import pandas as pd

list_atlas = ['BrainColor', 'EveType1', 'EveType2', 'EveType3']

for atlas in list_atlas:
    df = pd.read_csv("/home/local/VANDERBILT/gaoc11/Projects/Variance-Aging-Diffusion/Data/LUT_customize/{0}_LUT.csv".format(atlas))
    df['ROI_abbr'] = df['ROI_rename']
    
    
    df['ROI_abbr'] = df['ROI_abbr'].apply(lambda x: x.replace(' (Include Optic Radiation)', ''))
    df['ROI_abbr'] = df['ROI_abbr'].apply(lambda x: x.replace(' (a Part of MCP)', ''))
    
    df['ROI_abbr'] = df['ROI_abbr'].apply(lambda x: x.replace('Lobules', 'Lob.'))
    df['ROI_abbr'] = df['ROI_abbr'].apply(lambda x: x.replace('White Matter', 'WM'))
    df['ROI_abbr'] = df['ROI_abbr'].apply(lambda x: x.replace('Inferior Frontal Gyrus','IFG'))
    df['ROI_abbr'] = df['ROI_abbr'].apply(lambda x: x.replace('Retrolenticular', 'Rl.'))
    df['ROI_abbr'] = df['ROI_abbr'].apply(lambda x: x.replace('Fronto-occipital', 'Focc.'))
    df['ROI_abbr'] = df['ROI_abbr'].apply(lambda x: x.replace('Fronto-orbital', 'Forb.'))
    df['ROI_abbr'] = df['ROI_abbr'].apply(lambda x: x.replace('Corpus Callosum', 'CC'))
    df['ROI_abbr'] = df['ROI_abbr'].apply(lambda x: x.replace('Stria Terminalis', 'ST'))
    df['ROI_abbr'] = df['ROI_abbr'].apply(lambda x: x.replace('Cingulum', 'Cing.'))
    df['ROI_abbr'] = df['ROI_abbr'].apply(lambda x: x.replace('Longitudinal', 'Long.'))
    
    df['ROI_abbr'] = df['ROI_abbr'].apply(lambda x: x.replace('Right', 'R.').replace('Left', 'L.'))
    df['ROI_abbr'] = df['ROI_abbr'].apply(lambda x: x.replace('Posterior', 'Post.'))
    df['ROI_abbr'] = df['ROI_abbr'].apply(lambda x: x.replace('Anterior', 'Ant.'))
    df['ROI_abbr'] = df['ROI_abbr'].apply(lambda x: x.replace('Lateral', 'Lat.'))
    df['ROI_abbr'] = df['ROI_abbr'].apply(lambda x: x.replace('Superior', 'Sup.'))
    df['ROI_abbr'] = df['ROI_abbr'].apply(lambda x: x.replace('Internal', 'Int.'))
    df['ROI_abbr'] = df['ROI_abbr'].apply(lambda x: x.replace('Exterior', 'Ext.'))
    df['ROI_abbr'] = df['ROI_abbr'].apply(lambda x: x.replace('Frontal', 'Front.'))
    df['ROI_abbr'] = df['ROI_abbr'].apply(lambda x: x.replace('Postcentral', 'Postcent.'))
    df['ROI_abbr'] = df['ROI_abbr'].apply(lambda x: x.replace('Medial', 'Med.'))
    df['ROI_abbr'] = df['ROI_abbr'].apply(lambda x: x.replace('Middle', 'Mid.'))
    df['ROI_abbr'] = df['ROI_abbr'].apply(lambda x: x.replace('Inferior', 'Inf.'))
    df['ROI_abbr'] = df['ROI_abbr'].apply(lambda x: x.replace('Temporal', 'Temp.'))
    
    df['ROI_abbr'] = df['ROI_abbr'].apply(lambda x: x.replace('Segment', 'Seg.'))
    df['ROI_abbr'] = df['ROI_abbr'].apply(lambda x: x.replace('Part', 'Pt.'))
    df['ROI_abbr'] = df['ROI_abbr'].apply(lambda x: x.replace('Supplementary', 'Suppl.'))
    
    df['ROI_abbr'] = df['ROI_abbr'].apply(lambda x: x.replace('of', ''))

    df.to_csv("/home/local/VANDERBILT/gaoc11/Projects/Variance-Aging-Diffusion/Data/LUT_abbr/{0}_LUT.csv".format(atlas), index=False)

