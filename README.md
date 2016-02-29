############################################
# Incorporating TADs into GWAS Analysis
(C) 2016 Gregory Way
############################################

#############
# SUMMARY
#############
The repository contains methods for manipulating, observing, and visualizing
topologically associating domains (TADs) in the context of 1000 Genomes Phase
III data, and hg19 Gencode genes. The repository also proposes methods and tools
for the incorporation of TAD domains into the prioritization of GWAS signals
through the investigation of publically available GWAS data.

#############
# CONTACT
#############
For all questions and bug reporting:
GregWay@mail.med.upenn.edu

#############
# USAGE
#############
The analysis can be performed in full through
a single command:
~~~~~~~~~~~~~~~~~~
./ANALYSIS.sh
~~~~~~~~~~~~~~~~~~
which first downloads pertinent data and also outputs all figures.

#######################
# DEPENDENCIES
#######################

# Python 2.7
* pandas (0.17.1)
* pickle
* subprocess
* vcf (0.6.7)

# R 3.2.3
* readr (0.2.2)

