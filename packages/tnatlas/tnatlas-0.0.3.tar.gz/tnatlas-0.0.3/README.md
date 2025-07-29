# Overview

TnAtlas is a Python package for identifying and annotating transposon integration events into genomes.

Given a set of sequencing reads, transposon sequences, and genomes, the TnAtlas package can:

* Looks for reads which contain genomic DNA preceded by transposon DNA.
* Annotating the reads with corresponding features from the genome.
* Produces a summary for a set of reads in excel format.

For those who *do not want to write Python code*, the package also ships with 2 utilities, `tnfind` and `tnmeta`, which can be used to run analysis from the command line. 

# Installing

## Dependencies

* Python >= 3.8 
* blastn >= 2.12

### Optionally
Some parts of the pipeline also require

* fastqc (for sequencing quality control reports)
* sickle (for trimming based on sequencing quality)

## From source code

1. Get the code:
   
   `git clone https://github.com/lgrozinger/transposonaligner`
3. Install using pip:
   
   `python3 -m pip install ./transposonaligner`

## From PyPI (using pip)

Coming soon to PyPI...

# Usage

# Contributing

Contributions of all kinds are welcomed, including:
* Code for new features and bug fixes
* Test code and examples
* Bug reports and suggestions for new features (e.g. opening a github issue)

If you plan to change the source code, please open an issue for discussing the proposed changes and fork the repository.

# Citing

If you use this work as part of a publication, please cite as: ___________________

# Acknowledgements
