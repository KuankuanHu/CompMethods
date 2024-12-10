import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def read_vcf(file: str) -> pd.DataFrame:
    num_header = 0
    with open(file) as f:
        for line in f.readlines():
            if line.startswith("##"):
                num_header += 1
            else:
                break
    vcf = pd.read_csv(file, sep="\t", skiprows=num_header)
    vcf = vcf.rename({"#CHROM": "CHROM"}, axis=1)
    return vcf
# Credit of this function: https://medium.com/@sud0gene/parsing-variant-call-format-vcf-as-data-frames-bfc9852b64ca

def splitVcf(genotypes: list) -> np.array:
    rslt = np.array([])
    for entry in genotypes:
        haps = entry.split("|")
        rslt = np.append(rslt, float(haps[0]))
    return rslt

HA_sim_results = [
    f for f in os.listdir(os.path.expanduser("~/Documents/HA_sim_output/results"))
    if f.endswith(".vcf")
]
# List file in a dir, credit: https://stackoverflow.com/questions/3207219/how-do-i-list-all-files-of-a-directory

# Create the matrix for counts of mutant alleles
# The columns of the matrix represent positions on the genome, and rows represent trials
allele_freq_matrix = np.zeros([200, 3000])
for j in range(len(HA_sim_results)):
    path = os.path.expanduser("~/Documents/HA_sim_output/results/" + HA_sim_results[j])
    cr_vcf = read_vcf(path)
    pos_ls = cr_vcf["POS"]
    for i in range(len(pos_ls)):
        mut_freq = np.mean(splitVcf(cr_vcf.iloc[i, 9:]))
        allele_freq_matrix[j, pos_ls[i]-1] = mut_freq

#quick check
#print(allele_freq_matrix[0:10, 1480:1520])
