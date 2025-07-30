import os
import shutil
from miblab import osf_fetch  # Updated import path per review

def test_osf_fetch():
    # Set test parameters
    dataset = "Challenge_Guideline"  # Example dataset
    folder = "test_download"
    project_id = "u7a6f"  # Public OSF project

    # Clean up before test
    if os.path.exists(folder):
        shutil.rmtree(folder)

    # Run osf_fetch
    try:
        print(f"Testing osf_fetch with dataset='{dataset}' from public OSF project '{project_id}'")
        osf_fetch(dataset=dataset, folder=folder, project=project_id, extract=True, verbose=True)
    except Exception as e:
        assert False, f"osf_fetch raised an exception: {e}"

    # Assertions (pytest-compatible)
    assert os.path.exists(folder), "Folder was not created"
    assert any(os.scandir(folder)), "No files were downloaded"

    # Leave folder for inspection (optional)
    print(f"Test passed. Downloaded files are in: {folder}")
    # To auto-cleanup after the test, uncomment below:
    shutil.rmtree(folder)

if __name__ == "__main__":
    test_osf_fetch()
