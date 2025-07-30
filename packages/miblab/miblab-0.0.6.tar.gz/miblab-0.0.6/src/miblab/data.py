import os
import zipfile

# Try importing optional dependencies
try:
    import requests
    from osfclient.api import OSF
    from tqdm import tqdm
    import_error = False
except ImportError:
    import_error = True

# Zenodo DOI of the repository
DOI = {
    'MRR': "15285017",    
    'TRISTAN': "15301607", 
}

# miblab datasets
DATASETS = {
    'KRUK.dmr.zip': {'doi': DOI['MRR']},
    'tristan_humans_healthy_controls.dmr.zip': {'doi': DOI['TRISTAN']},
    'tristan_humans_healthy_ciclosporin.dmr.zip': {'doi': DOI['TRISTAN']},
    'tristan_humans_healthy_metformin.dmr.zip': {'doi': DOI['TRISTAN']},
    'tristan_humans_healthy_rifampicin.dmr.zip': {'doi': DOI['TRISTAN']},
    'tristan_humans_patients_rifampicin.dmr.zip': {'doi': DOI['TRISTAN']},
    'tristan_rats_healthy_multiple_dosing.dmr.zip': {'doi': DOI['TRISTAN']},
    'tristan_rats_healthy_reproducibility.dmr.zip': {'doi': DOI['TRISTAN']},
    'tristan_rats_healthy_six_drugs.dmr.zip': {'doi': DOI['TRISTAN']},
}

def zenodo_fetch(dataset:str, folder:str, doi:str=None, filename:str=None):
    """Download a dataset from Zenodo.

    Note if a dataset already exists locally it will not be downloaded 
    again and the existing file will be returned. 

    Args:
        dataset (str): Name of the dataset
        folder (str): Local folder where the result is to be saved
        doi (str, optional): Digital object identifier (DOI) of the 
          Zenodo repository where the dataset is uploaded. If this 
          is not provided, the function will look for the dataset in
          miblab's own Zenodo repositories.
        filename (str, optional): Filename of the downloaded dataset. 
          If this is not provided, then *dataset* is used as filename.

    Raises:
        NotImplementedError: If miblab is not installed with the data
          option
        requests.exceptions.ConnectionError: If the connection to 
          Zenodo cannot be made.

    Returns:
        str: Full path to the downloaded datafile.
    """
    if import_error:
        raise NotImplementedError(
            'Please install miblab as pip install miblab[data]'
            'to use this function.'
        )
        
    # Create filename 
    if filename is None:
        file = os.path.join(folder, dataset)
    else:
        file = os.path.join(folder, filename)

    # If it is already downloaded, use that.
    if os.path.exists(file):
        return file
    
    # Get DOI
    if doi is None:
        if dataset in DATASETS:
            doi = DATASETS[dataset]['doi']
        else:
            raise ValueError(
                f"{dataset} does not exist in one of the miblab "
                f"repositories on Zenodo. If you want to fetch " 
                f"a dataset in an external Zenodo repository, please "
                f"provide the doi of the repository."
            )
    
    # Dataset download link
    file_url = "https://zenodo.org/records/" + doi + "/files/" + dataset

    # Make the request and check for connection error
    try:
        file_response = requests.get(file_url) 
    except requests.exceptions.ConnectionError as err:
        raise requests.exceptions.ConnectionError(
            f"\n\n"
            f"A connection error occurred trying to download {dataset} "
            f"from Zenodo. This usually happens if you are offline."
            f"The detailed error message is here: {err}"
        ) 
    
    # Check for other errors
    file_response.raise_for_status()

    # Create the folder if needed
    if not os.path.exists(folder):
        os.makedirs(folder)

    with open(file, 'wb') as f:
        f.write(file_response.content)

    return file

def osf_fetch(dataset: str, folder: str, project: str = "un5ct", token: str = None, extract: bool = True, verbose: bool = True):
    """
    Download a dataset from OSF (Open Science Framework).

    This function downloads a specific dataset (folder or subfolder) from a public or private OSF project.
    Files are saved into the specified local directory. If a zip file is found, it will be extracted by default.

    Args:
        dataset (str): Subfolder path inside the OSF project. If an empty string, all files in the root will be downloaded (use with caution).
        folder (str): Local folder where the dataset will be saved.
        project (str, optional): OSF project ID (default is "un5ct").
        token (str, optional): Personal OSF token for accessing private projects. Read from OSF_TOKEN environment variable if needed.
        extract (bool, optional): Whether to automatically unzip downloaded .zip files (default is True).
        verbose (bool, optional): Whether to print progress messages (default is True).

    Raises:
        FileNotFoundError: If the specified dataset path does not exist in the OSF project.
        NotImplementedError: If required packages are not installed.

    Returns:
        str: Path to the local folder containing the downloaded data.

    Example:
        >>> from miblab import osf_fetch
        >>> osf_fetch('TRISTAN/RAT/bosentan_highdose/Sanofi', 'test_download')
    """
    if import_error:
        raise NotImplementedError(
            "Please install miblab as pip install miblab[data] to use this function."
        )

    # Prepare local folder
    os.makedirs(folder, exist_ok=True)

    # Connect to OSF and locate project storage
    osf = OSF(token=token)  #osf = OSF()  for public projects
    project = osf.project(project)
    storage = project.storage('osfstorage')

    # Navigate the dataset folder if provided
    current = storage
    if dataset:
        parts = dataset.strip('/').split('/')
        for part in parts:
            for f in current.folders:
                if f.name == part:
                    current = f
                    break
            else:
                raise FileNotFoundError(f"Folder '{part}' not found when navigating path '{dataset}'.")

    # Recursive download of all files and folders
    def download(current_folder, local_folder):
        os.makedirs(local_folder, exist_ok=True)
        files = list(current_folder.files)
        iterator = tqdm(files, desc=f"Downloading to {local_folder}") if verbose and files else files
        for file in iterator:
            local_file = os.path.join(local_folder, file.name)
            try:
                with open(local_file, 'wb') as f:
                    file.write_to(f)
            except Exception as e:
                if verbose:
                    print(f"Warning downloading {file.name}: {e}")

        for subfolder in current_folder.folders:
            download(subfolder, os.path.join(local_folder, subfolder.name))

    download(current, folder)

    # Extract all downloaded zip files if needed
    if extract:
        for dirpath, _, filenames in os.walk(folder):
            for filename in filenames:
                if filename.lower().endswith('.zip'):
                    zip_path = os.path.join(dirpath, filename)
                    extract_to = os.path.join(dirpath, filename[:-4])
                    os.makedirs(extract_to, exist_ok=True)
                    try:
                        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                            bad_file = zip_ref.testzip()
                            if bad_file:
                                raise zipfile.BadZipFile(f"Corrupt file {bad_file} inside {zip_path}")
                            zip_ref.extractall(extract_to)
                        os.remove(zip_path)
                        if verbose:
                            print(f"Unzipped and deleted {zip_path}")
                    except Exception as e:
                        if verbose:
                            print(f"Warning unzipping {zip_path}: {e}")

    return folder