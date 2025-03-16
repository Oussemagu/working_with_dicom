import pydicom
import numpy as np
import os
import pyvista as pv

def load_dicom_files(directory_name):
    
    """Load DICOM files from the specified directory."""
    full_path = os.path.join(os.getcwd(), directory_name)
    print(f"Full path: {full_path}")

    # List all DICOM files in the directory
    file_list = [entry.path for entry in os.scandir(full_path) if entry.is_file()]
    files = []

    for fname in file_list:
        print(f"Loading: {fname}")
        dicom_file = pydicom.dcmread(fname)
        if hasattr(dicom_file, 'SliceLocation'):  # Only keep files with SliceLocation
            files.append(dicom_file)
            print(f"SliceLocation: {dicom_file.SliceLocation}")
    
    print(f"File count: {len(files)}")
    return files

def sort_slices_by_location(files):
    """Sort DICOM files by their SliceLocation tag"""
    return sorted(files, key=lambda s: s.SliceLocation)

def create_3d_array_from_slices(slices):
    """Create a 3D NumPy array from DICOM slices. """
    # Get 2D image size [rows, cols]
    img_shape = list(slices[0].pixel_array.shape)
    
    # Add the third dimension: number of slices
    img_shape.append(len(slices))
    
    # Create empty 3D array to hold the images
    img3d = np.zeros(img_shape)

    # Fill 3D array with the images from the DICOM files
    for i, s in enumerate(slices):
        img3d[:, :, i] = s.pixel_array

    return img3d

def display_3d_volume(img3d):
    """Display the 3D volume using PyVista  """
    # Convert the 3D NumPy array into a PyVista grid
    volume = pv.wrap(img3d)

    # Set up a plotter for the 3D volume
    plotter = pv.Plotter()
    plotter.add_volume(volume, cmap="gray")  # Display the volume with a grayscale colormap

    # Add a scalar bar to indicate intensity levels
    plotter.add_scalar_bar(title="Intensity")

    # Show the 3D visualization
    plotter.show()

def main():
    """
    Main function to load DICOM files, process them, and display a 3D volume.
    """
    directory_name = "series-000001"  # DICOM sample from https://www.dicomlibrary.com/
    
    # Load DICOM files
    dicom_files = load_dicom_files(directory_name)

    # Sort DICOM files based on SliceLocation
    sorted_slices = sort_slices_by_location(dicom_files)

    # Create a 3D array from the sorted slices
    img3d = create_3d_array_from_slices(sorted_slices)

    # Display the 3D volume
    display_3d_volume(img3d)

if __name__ == "__main__":
    main()
