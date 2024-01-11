# Check the calculation of the motion (one scaler value for each DTI), and compare the value with the one provided by PreQual.
# Conclusion: PreQual calculates the average of all rms without excluding the first rms, which is always zero.

import pandas as pd
import numpy as np
import csv
import pdb

fn_eddy_rms = '/nfs2/harmonization/BLSA/BLSA_7927_07-0_10/ASSESSORS/BLSA-x-BLSA_7927-x-BLSA_7927_07-0_10-x-dtiQA_synb0_v7-x-80a935a0-bec9-4f02-a707-885f1287c0c8/EDDY/eddy_results.eddy_movement_rms'

second_column = []
with open(fn_eddy_rms, 'r') as f:
    c = csv.reader(f, delimiter=' ')
    for line in c:
        second_column.append(float(line[2]))
        
first_column = []
with open(fn_eddy_rms, 'r') as f:
    c = csv.reader(f, delimiter=' ')
    for line in c:
        first_column.append(float(line[0]))

pdb.set_trace()
