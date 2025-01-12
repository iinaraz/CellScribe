# CellScribe
Generation of molecular signatures for cell types from sorted cell proteomics data

# Introduction
Cellular signatures are sets of molecular markers that describe or characterize a specific cell type and are used to resolve cell types from complex data, identify cell types, and analyze the differential expression of cell type-specific molecules in different conditions. This program will receive a processed expression matrix of several sorted cell population samples and output a set of molecules that characterize each cell type that appears in the matrix.

<img src="CellScribe.png" alt="Cell signature concept image" width="600"/>

## Requirements
### Input requirements
The user should be able to provide an expression matrix for the program with sorted cell populations

### Software requirements
Python 3.7 ->

### Packages
```
pandas
numpy
itertools
scipy
scikit-learn
```

# Algorithm
1. Program reads an expression matrix file (.csv format)

2. Hierarchical clustering of the data and selection of cluster-specific high-abundance molecules

3. Principal component analysis and selection of molecules contributing most to the uniqueness of the cell type (variation)

4. Pairwise comparison between all cell types using statistical method and aggregating results for each cell type

5. Consensus signature - combine signature hits from each approach to establish a robust signature for each cell type

# Execution
## Installation
```
pip install -r requirements.txt
```
```
git clone https://github.com/iinaraz/CellScribe
```

## Input
Expression matrix
Name|CellType_A_1|CellType_A_2|CellType_A_3|CellType_B_1|CellType_B_2|CellType_B_3|CellType_C_1|CellType_C_2|CellType_C_3
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

## Running the program
```
# Navigate to the CellScribe repository
cd <path_to_repository>

# Run CellScribe from command line
python CellScribe.py <filename>
```

## Output
A table with columns Celltype, Marker and Value

The value will describe the strength of the specific molecule as a signature marker based on the features analyzed.

## Information

This program and the Github repository was written by Iina Raz. The project was done as a part of a [Python Programming Course](https://github.com/szabgab/wis-python-course-2024-11) at the Weizmann Institute of Science.

