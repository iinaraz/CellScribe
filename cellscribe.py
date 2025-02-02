import os
from input_processing import extract_input_data
from output_dir import create_output_dir
from differential_expression import population_differential_expression
import warnings
import argparse
import pandas as pd
import yaml

def main():

    # Create output directory for results
    res_path = create_output_dir()

    ## ----------------- SET UP ARGUMENTS -----------------------

    logo = """

  █████  █████  ██     ██     ██████  ██████  █████   ███  █████  █████
 ██      ██     ██     ██     ██      ██      █   █    █   █   █  ██   
 ██      █████  ██     ██     ██████  ██      █████    █   █████  █████ 
 ██      ██     ██     ██         ██  ██      █  █     █   █   █  ██   
  █████  █████  █████  █████  ██████  ██████  █   █   ███  █████  █████

"""

    # Create parser
    parser = argparse.ArgumentParser(description= "\nCellScribe generates differential expression -based marker signatures for predetermined populations using expression data from high-throughput technologies such as mass spectrometry based proteomics, single-cell RNA sequencing or RNA sequencing.",
                                     formatter_class=argparse.RawTextHelpFormatter)  # Preserves formatting)

    # Add argument for expression matrix file and celltypes
    parser.add_argument("--data", type=str, help="Path to the input expression matrix (csv). The first column should be named `Identifier` and contain identifiers for the molecules.", required=True)
    parser.add_argument("--populations", type=str, help="Path to the txt file of populations (txt). The file should contain columns `Label` that match to the sample column names in the data file, and a `Population` column that categorizes each label to a population.", required=True)

    # Add optional arguments to control user parameters
    parser.add_argument("--n_markers", type=int, default=30, help="Number of markers to select per population. Default is 30.", required=False)
    parser.add_argument("--fc_threshold", type=float, default=0, help="Log2 fold change threshold for differential expression. Default is 0.", required=False)
    parser.add_argument("--pval_threshold", type=float, default=0.05, help="Adjusted p-value threshold for differential expression. Default is 0.05.", required=False)
    args = parser.parse_args()

    # Save path to files from args
    data_path = args.data
    populations_path = args.populations

    # Save n markers (default if not provided)
    n_markers=args.n_markers
    fc_threshold=args.fc_threshold
    pval_threshold=args.pval_threshold

    # Save settings information
    settings = {
        "data": data_path,
        "populations": populations_path,
        "n_markers": n_markers,
        "fc_threshold": fc_threshold,
        "pval_threshold": pval_threshold
    }

    param_file_path = os.path.join(res_path, "param.yaml")

    with open(param_file_path, "w") as file:
        yaml.dump(settings, file)

    # Print logo
    print(logo)

    # -------------------- LOAD DATA --------------------------
    # Load data
    input = extract_input_data(data_path, populations_path)

    data = input[0]
    populations = input[1]

    # ------------------ GENERATE SIGNATURES -------------------

    # Differential expression analysis one vs rest
    DE_results = population_differential_expression(data, populations, output_dir=res_path, n_top_markers=n_markers, fc_threshold=fc_threshold, pval_threshold=pval_threshold)
    print(f"Signature results saved in: {res_path}/signatures.csv")

    # ----------------- SAVE RESULTS TO CSV ---------------------
    DE_results.to_csv(os.path.join(res_path ,"signatures.csv"), index=False)
    


if __name__ == "__main__":
    main()