# Working with DICOM Data

This project demonstrates the process of working with DICOM (Digital Imaging and Communications in Medicine) files using Python. The goal is to read, process, and visualize 3D medical imaging data, such as CT or MRI scans, from DICOM files. The project includes functionality for loading DICOM files, extracting relevant metadata, creating a 3D volume from the image slices, and displaying the volume using visualization tools.

## Features

- Load and process DICOM files from a directory.
- Sort DICOM slices based on the `SliceLocation` tag to ensure correct slice order.
- Generate a 3D volume from the DICOM slices.
- Visualize the 3D volume using PyVista with interactive features.

## Requirements

To run this project, you'll need to install the following dependencies:

- `pydicom`: A Python package for working with DICOM files.
- `numpy`: A package for numerical computations and handling arrays.
- `pyvista`: A package for 3D visualization and rendering.

You can install the required dependencies using pip:

```pip install pydicom numpy pyvista```

## How to use :

## Installation

1. Clone the repository to your local machine:
``` git clone https://github.com/Oussemagu/working_with_dicom.git ```
2. Place the DICOM files in the `series-000001` directory or modify the directory_name variable to match the directory containing your DICOM files.

`3.`Install the required dependencies
```  pip install -r requirements.txt ```

`4.` Run the script

# working_with_dicom
open link where you can find DICOM samples:
https://www.dicomlibrary.com/
dicom standard browser: https://dicom.innolitics.com/ciods
