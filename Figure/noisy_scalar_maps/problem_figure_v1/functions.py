import sys
import numpy as np

def reorder_nifti_data(nifti_data, affine_code):
    """Reorder the axis of the array from the nifti for easier visualization. Follow ("P","L","S")

    """
    
    if 'S' in affine_code:
        si_index = affine_code.index('S')
    elif 'I' in affine_code:
        si_index = affine_code.index('I')
        nifti_data = np.flip(nifti_data, axis=si_index)
    else:
        sys.exit("Check the orientation of the image!")
        
    if 'L' in affine_code:
        lr_index = affine_code.index('L')
    elif 'R' in affine_code:
        lr_index = affine_code.index('R')
        nifti_data = np.flip(nifti_data, axis=lr_index)
    else:
        sys.exit("Check the orientation of the image!")

    if 'P' in affine_code:
        ap_index = affine_code.index('P')
    elif 'A' in affine_code:
        ap_index = affine_code.index('A')
        nifti_data = np.flip(nifti_data, axis=ap_index)
    else:
        sys.exit("Check the orientation of the image!")

    nifti_data = np.moveaxis(nifti_data, [ap_index, lr_index, si_index], [0, 1, 2])
    
    return nifti_data