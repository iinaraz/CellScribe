
<img src="CellScribe_logo.PNG" alt="Logo" width="600"/>

# CellScribe
Generation of molecular signatures for cell populations

# Introduction
Cellular signatures are sets of molecular markers that describe or characterize a specific cell type and are used to resolve cell types from complex data, identify cell types, and analyze the differential expression of cell type-specific molecules in different conditions. This program will receive a processed expression matrix of several sorted cell population samples and output a set of molecules that characterize each cell type that appears in the matrix.

The program is meant to be used when cell type-specific expression information is available (e.g., sorted cell populations or single-cell data). The signatures are calculated based on the background of the other populations.

<img src="CellScribe.png" alt="Cell signature concept image" width="800"/>

## Signature generation details

The signature is built from differential expression results that compares the expression values of one population to the average of the background (rest of the populations).

Upregulated markers for the specific population are chosen based on the default or user generated parameters.

*Default thresholds:*

Number of markers: 30

Log2 fold change: 0

Adjusted p-value: 0.05

The signature generation will be executed for all populations in the input matrix iteratively, so a table of molecular signatures will be available for all input populations.

## Requirements
### Input requirements
The user should be able to provide an expression matrix for the program with sorted cell populations.

The expression matrix has to contain a column `Identifier` as the first column of the matrix to identify the molecules.
The population file has to contains columns `Label` and `Population` where `Label` maps to the column names of the expression matrix.

### Software requirements
Python 3.7 ->

## Input
Expression matrix - first column is gene/protein/feature names (Identifier), other columns are samples.
Identifier|CellType_A_1|CellType_A_2|CellType_A_3|CellType_B_1|CellType_B_2|CellType_B_3|CellType_C_1|CellType_C_2|CellType_C_3
---|---|---|---|---|---|---|---|---|---
Protein_1|6.87|9.95|3.59|2.41|12.50|14.51|10.35|10.55|14.23	
Protein_2|14.36|3.81|8.44|10.27|13.65|5.27|3.09|9.39|14.40	
Protein_3|11.52|5.80|2.45|6.09|6.13|8.46|4.10|3.22|13.89	
Protein_4|9.78|6.76|13.82|8.61|3.43|5.91|13.68|6.78|6.81	
Protein_5|4.03|7.93|5.36|13.80|4.96|5.70|9.88|5.45|2.20	
Protein_6|4.03|12.21|10.61|5.24|7.55|2.48|2.12|5.17|14.07	
Protein_7|2.76|4.60|6.05|7.33|12.63|9.92|3.32|14.65|7.57	
Protein_8|13.26|8.69|8.76|11.82|13.19|8.53|10.63|7.11|14.57	
Protein_9|9.81|9.70|9.11|4.97|2.09|2.67|2.07|13.60|14.53	
Protein_10|11.20|2.60|4.40|3.00|8.64|5.62|4.09|10.20|13.09

Sample metadata
A csv file that indicates the labels (same as column names of the expression matrix) and maps populations in which group/population each sample belongs to.
Label|Population
---|---
Celltype_A_1|A
Celltype_A_2|A
Celltype_A_3|A
Celltype_B_1|B
Celltype_B_2|B
Celltype_B_3|B
Celltype_C_1|C
Celltype_C_2|C
Celltype_C_3|C

# Execution
## Installation
```
pip install -r requirements.txt
```
Navigate to the parent directory where you wish your CellScribe to be

```
git clone https://github.com/iinaraz/CellScribe.git
```

## Running the program
```
# Navigate to the CellScribe repository
cd <path_to_repository>

# See argument information by running
python cellscribe.py --help

# Run CellScribe from command line
python cellscribe.py --data PATH_TO_EXPRESSION_MATRIX --populations PATH_TO_POPULATION_INFO --n_markers N_MARKERS --fc_threshold LOG2_FC_THRESHOLD --pval_threshold ADJUSTED_PVALUE_THRESHOLD
```

Initiating CellScribe will create a folder in the current directory and store the results (see Output) in the directory.


## Running with example data

Testing the tool is possible by using files in the [data](https://github.com/iinaraz/CellScribe/tree/main/data) folder.

Data published by:
Rieckmann JC, Geiger R, Hornburg D, Wolf T, Kveler K, Jarrossay D, Sallusto F, Shen-Orr SS, Lanzavecchia A, Mann M, Meissner F. Social network architecture of human immune cells unveiled by quantitative proteomics. Nat Immunol. 2017 May;18(5):583-593. doi: 10.1038/ni.3693. Epub 2017 Mar 6. PMID: 28263321.

The data is a subset of sorted immune cell populations analyzed by mass spectrometry-based proteomics.

To run the program with the example data, follow the steps for requirements installation and clone the repository as described above. Then run:

```
python cellscribe.py "data/proteins_subset.csv" --populations "data/sample_info.csv"
```

Parameters for arguments n_markers, fc_threshold and pval_threshold can be adjusted by choice.


## Output

A table with markers for each population and their differential expression results

Volcano plot of differential expression results for each population with selected markers labeled

Settings used in the analysis will be saved in settings.yaml in the results folder

## Information

For more detailed inspection of the program, see [Jupyter notebook](https://github.com/iinaraz/CellScribe/blob/main/cellscribe.ipynb).

This program and the Github repository was written by Iina Raz. The project was done as a part of a [Python Programming Course](https://github.com/szabgab/wis-python-course-2024-11) at the Weizmann Institute of Science.

