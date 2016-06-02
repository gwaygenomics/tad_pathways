"""
(C) 2016 Gregory Way
Identify_TAD_signal.py

Description:
Uses TAD boundaries and trait specific GWAS files that were generated by
'NHGRI-EBI_GWAS_summary.R' to output an intermediate file of TAD
coordinates for each significant SNP

Usage:
Is called by 'build_TAD_genelists.py'

Output:
Intermediate files 'data/gwas_TAD_location', which are summaries of each SNP and
which TAD they fall in. The format of the output files by row is:
[rs, Chromosome, SNP Coordinate, TAD Start, TAD End, TAD ID, nearest gene]
"""

from optparse import OptionParser
import csv
import pandas as pd

####################################
# Load Command Arguments
####################################
parser = OptionParser()  # Load command line options
parser.add_option("-t", "--TAD-data", dest="tad",
                  help="Location of TAD data", type="string")
parser.add_option("-g", "--GWAS-data", dest="gwas",
                  help="Location of GWAS data ", type="string")
parser.add_option("-o", "--output-file", dest="output",
                  help="Name of the output file", type="string")
(options, args) = parser.parse_args()

####################################
# Load Constants
####################################
TAD_DATA = options.tad
GWAS_DATA = options.gwas
OUTPUT_FH = options.output

####################################
# Load and process data
####################################
TADLoc = []
TAD_idx = 0
with open(TAD_DATA) as tadfile:
    tadreader = csv.reader(tadfile, delimiter='\t')
    for row in tadreader:
        chrom = row[0]
        TADLoc.append((chrom[3:], int(row[1]), int(row[2]), TAD_idx))
        TAD_idx += 1

TADLoc = pd.DataFrame(TADLoc, columns=('chrom', 'TADStart', 'TADEnd', 'TADidx'))

SNP_TADassign = []
with open(GWAS_DATA) as gwasfile:
    gwasreader = csv.reader(gwasfile, delimiter='\t')
    next(gwasreader)
    for row in gwasreader:

        if row[2] == 'NA' or row[2] == 'Not Mapped':
            next
        else:
            chrom = row[1][3:]
            snploc = int(row[2])
            # Find the TAD where the SNP is located
            tad = TADLoc.ix[(TADLoc.chrom == chrom) &
                            (TADLoc.TADStart <= snploc) &
                            (TADLoc.TADEnd > snploc)]

            # Clean up mapped genes
            mapgene = row[5].replace(' - ', ',')
            mapgene = mapgene.replace(' ', '')

            if len(tad) == 0:
                tad = [row[0], row[1], int(row[2]), 'NA', 'NA', 'NA', mapgene]
            else:
                # The mapped gene is the closest gene in proximity to the SNP
                # In the event that two genes are present, the gene on the left
                # is the closest gene to the left and right is closest on right.
                # Add both to the mapped gene list
                tad = [row[0], row[1], int(row[2]), tad.iloc[0, 1],
                       tad.iloc[0, 2], tad.iloc[0, 3], mapgene]

            SNP_TADassign.append(tad)

####################################
# Write the reorganized data to file
####################################
pd_columns = ('rs', 'chrom', 'snploc', 'TADStart', 'TADEnd', 'TADidx', 'gene')
SNP_TADassign = pd.DataFrame(SNP_TADassign, columns=pd_columns)

with open(OUTPUT_FH, 'wt') as w_file:
    SNP_TADassign.to_csv(w_file, index=False, header=True, sep='\t')
