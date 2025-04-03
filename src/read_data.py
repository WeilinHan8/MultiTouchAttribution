import os
import zipfile
import pandas as pd

def read_data(directory, save_path):
    """
    Read the data from given directory.

    Parameters:
    ----------
    directory : str
        The directory to the raw data.
    save_path : str
        The path to save the extracted data from the zip file.

    Returns:
    -------
    Pandas DataFrame or None
    """
    
    # check if the directory exists, if not raise an error
    if not os.path.isdir(directory):
        raise ValueError('The directory provided does not exist.')
        
    # check if the dirctory points to a zip file or csv file, if not raise an error  
    if directory[-4:] not in ['.zip', '.csv']:
        raise ValueError('The  provided does not point to a zip or csv file.')

    if directory.endswith('.zip'):
        # Extract the zip file to the save_path
        with zipfile.ZipFile(directory, 'r') as zip_ref:
            zip_ref.extractall(save_path)

        # Get the list of extracted files
        extracted_files = os.listdir(save_path)
        if not extracted_files:
            raise ValueError('The ZIP file is empty.')

        # Look for a CSV file inside the extracted folder
        csv_files = [f for f in extracted_files if f.endswith('.csv')]
        if not csv_files:
            raise ValueError('No CSV file found in the ZIP archive.')

        # Load the first CSV file found
        csv_path = os.path.join(save_path, csv_files[0])
        return pd.read_csv(csv_path)
    
    elif directory.endswith('.csv'):
        return pd.read_csv(directory)  
            
    return None