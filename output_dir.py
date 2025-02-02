import os
from datetime import datetime

def create_output_dir():
    # Get the current date
    current_date = datetime.now().strftime("%Y-%m-%d")
    
    # Define the folder name
    folder_name = f"CellScribe_{current_date}"
    
    # Create the folder in the current working directory
    os.makedirs(folder_name, exist_ok=True)

    return folder_name