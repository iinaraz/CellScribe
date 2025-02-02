import pandas as pd
import warnings
import os

def extract_input_data(expression_file_path, population_file_path):

   # ---------------- Check the file formatting ---------------------------

    if os.path.splitext(expression_file_path)[1].lower() != ".csv":
        raise ValueError("Error: The expression matrix should be in csv format.")

    if os.path.splitext(population_file_path)[1].lower() != ".csv":
        raise ValueError("Error: The populations file should be in a csv format.")

    # ----------------- Read input files ---------------------------------
    # Read expression matrix
    try:
        data = pd.read_csv(expression_file_path, sep=",", engine="python")
        print("File expression matrix read succesfully.")
    except Exception as e:
        print(f"Not able to load the expression file {e}. Check the input file.")
    
    # Read populations file
    try:
        populations = pd.read_csv(population_file_path, sep=",", engine="python")
        print("File populations read successfully.")
    except Exception as e:
        print("Not able to load the cell type file {e}. Check the input file.")
    
    # ------------------ Check data labels -----------------------------------
    # First column of expression matrix should be named "Identifier"
    if data.columns[0] != "Identifier":
        raise ValueError("The first column of the expression matrix should be labeled 'Identifier' and contain identifiers for the molecules.")

    # Columns of populations should be named "Label" and "Population"
    required_columns = {"Label", "Population"}

    if not required_columns.issubset(populations.columns):
        missing = required_columns - set(populations.columns)
        raise ValueError(f"Error: The 'populations' DataFrame is missing the following required columns: {missing}")
    
    # Check that there's at least two populations (so differential expression analysis can be performed)
    if len(populations['Population'].unique()) < 2:
        raise ValueError("Only one population detected. The minimum number of populations is two.")

    # Column names 1:ncol(data) should match to a group in populations
    matching_labels = populations["Label"].isin(data.columns[1:])

    if matching_labels.all():
        print("All 'Label' values in 'populations' match column names in 'data'.")
    elif matching_labels.any():
        warnings.warn("Some 'Label' values in 'populations' match column names in 'data', but not all.", UserWarning)
    else:
        raise ValueError("No 'Label' values in 'populations' match column names in 'data'.")

    # Check if any sample in data is NOT in populations["Label"]
    unmatched_columns = [col for col in data.columns[1:] if col not in populations["Label"].values]
    if unmatched_columns:
        raise ValueError(f"The following samples in 'expression matrix' are missing from 'populations[\"Label\"]': {unmatched_columns}")

    # ---------------- Processing ---------------------------------------
    # Set identifiers as rownames and remove character column from the expression matrix
    data_num = data.set_index(data.columns[0])


    return [data_num, populations]