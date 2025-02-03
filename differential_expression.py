import os
import scipy.stats
import numpy as np
import pandas as pd
from scipy.stats import ttest_ind
from statsmodels.stats.multitest import multipletests
import matplotlib.pyplot as plt
import seaborn as sns
from adjustText import adjust_text
from tqdm import tqdm
import warnings

def population_differential_expression(data, population_mapping, output_dir, n_top_markers, fc_threshold, pval_threshold, log2_transform=False):

    # ------------------ Section 1 -----------------------
    # Ensure the output directory exists
    os.makedirs(output_dir, exist_ok=True)

    # Set the cell types from the mapping file
    populations = population_mapping['Population'].unique()

    # Initialize a dictionary to store results
    results = {}

    # ---------------- Section 2: Loop through populations ----------------------------
    for group in tqdm(populations, desc="Generating signatures", unit="Population"):
        # Define target population
        target_group = group

        # Create a mask for the target and the rest (t-test is one vs rest)
        target_columns = [col for col in data.columns if target_group in col]  # Check if target_celltype appears anywhere
        rest_columns = [col for col in data.columns if col not in target_columns]

        # Initialize lists to store the results
        log_fold_changes=[]
        pvals=[]

        # -------- Section 2.1: Perform t-test and store p-values and log2 FCs for each molecule -----------
        for mol in data.index:
            target_data = data.loc[mol, target_columns]
            rest_data = data.loc[mol, rest_columns]

            # Test for equal variances
            levene_stat, levene_p = scipy.stats.levene(target_data, rest_data)

            # Decide on equal_var
            equal_var = levene_p > 0.05  # If p > 0.05, assume equal variance

            # Perform t-test
            tstat, p_value = ttest_ind(target_data, rest_data, equal_var=equal_var)
    
            # Calculate log2 fold change
            if log2_transform==False:
                log2_fc = target_data.mean() - rest_data.mean()
            else:
                log2_fc = np.log2(target_data.mean()/rest_data.mean())
    
            # Append results
            log_fold_changes.append(log2_fc)
            pvals.append(p_value)

        # Correct the p-values for multiple comparisons (FDR adjustment)
        pvals_corrected = multipletests(pvals, method='fdr_bh')[1]

        # --------- Section 2.2: Construct results dataframe for the population ------------------------
        # Create results DataFrame
        results_df = pd.DataFrame({
            'Marker': data.index,
            'Log2FoldChange': log_fold_changes,
            'PValue': pvals,
            'PAdjusted': pvals_corrected
        })

        # Set significance labels according to p-value and log2FoldChange
        results_df['Threshold'] = np.where(
            (results_df['PAdjusted'] < pval_threshold) & (results_df['Log2FoldChange'] > abs(fc_threshold)), 'Up',
            np.where((results_df['PAdjusted'] < pval_threshold) & (results_df['Log2FoldChange'] < -abs(fc_threshold)), 'Down', 'NS' )
        )

        # ---------- Section 2.3: Select top upregulated markers ------------------------------------
        # If there are upregulated molecules for the given population
        if (results_df['Threshold']=='Up').sum() > 0:

            # Select upregulated molecules as markers
            significant_results = results_df[results_df['Threshold'] == 'Up']

            # Sort by Log2 Fold Change (descending) and p-value (ascending)
            top_markers_df = significant_results.sort_values(by=['Log2FoldChange', 'PAdjusted'], ascending=[False, True])

            # Select the top n proteins if there's enough:
            if significant_results.shape[0] >= n_top_markers:
                top_markers_df = significant_results.sort_values(by=['Log2FoldChange', 'PAdjusted'], ascending=[False, True])
                selected_markers = top_markers_df.head(n_top_markers)

            # And if there aren't enough:
            else:
                selected_markers = significant_results
                warnings.warn(f"Population {target_group} has less significant hits than the selected number of markers.", UserWarning)

        else:
            warnings.warn(f"Population {target_group} failed to generate a signature. No significant hits.", UserWarning)

        selected_markers=selected_markers.copy()
        selected_markers['Population']=group

        # ------------- Section 2.4: Plot a volcanoplot ----------------------------------------------
        # Custom color palette
        palette = {'Up': '#daae21', 'Down': '#8e68a0', 'NS': '#a7a7a7'}  

        # Limits for x-axis
        x_lim =  abs(max(log_fold_changes)) + 1 

        # Create a volcano plot
        plt.figure(figsize=(10, 8))
        sns.scatterplot(
            data=results_df,
            x='Log2FoldChange',
            y=-np.log10(results_df['PAdjusted']),
            hue='Threshold',
            palette=palette,
            alpha=0.6
        )

        plt.axhline(-np.log10(pval_threshold), color='#c04858', linestyle='--', label=f"p={pval_threshold}")

        # Annotate the top molecules
        texts = []
        for i, row in selected_markers.iterrows():
            texts.append(plt.text(row['Log2FoldChange'], -np.log10(row['PAdjusted']),
                row['Marker'], fontsize=9, color='black', ha='center'))

        # Adjust text to avoid overlaps
        adjust_text(texts, arrowprops=dict(arrowstyle="->", color='black'))
        plt.xlim(-x_lim, x_lim)
        plt.title(f'Volcano Plot for {group}')
        plt.xlabel('Log2 Fold Change')
        plt.ylabel('-log10(p-value)')
        plt.legend()
        plt.tight_layout()
        plot_path = os.path.join(output_dir, f'volcano_{group}.png')
        plt.savefig(plot_path)
        plt.close()

        results[group]=selected_markers

    
    results_all = pd.concat(results.values())
    
    return results_all
