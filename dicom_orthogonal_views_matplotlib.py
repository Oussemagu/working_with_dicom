
#This script processes a set of DICOM files (specifically CT scan images) 
#and visualizes the resulting 3D image slices in three orthogonal views: Axial, Sagittal, and Coronal.
# The  dataset  used can be viewed and downloaded from DICOM Library
#dataset URL to download :
#https://www.dicomlibrary.com?requestType=WADO&studyUID=1.2.826.0.1.3680043.8.1055.1.20111102150758591.92402465.76095170&manage=1b9baeb16d2aeba13bed71045df1bc65&token=71052ed504213a73c8e166ab466c446ab3b2594996ef30e283
#The main steps include:
#1. Loading DICOM files from a specified directory.
#2. Filtering out invalid files (those without the `SliceLocation` attribute).
#3. Sorting the valid DICOM slices based on the `SliceLocation`.
#4. Extracting pixel data and arranging the slices into a 3D numpy array.
#5. Calculating the aspect ratios for different views based on pixel spacing and slice thickness.
#6. Plotting and displaying the three orthogonal views of the 3D image slices.

#The script assumes that all DICOM slices have the same pixel spacing and slice thickness, 
# which is typical in medical imaging studies.
import pydicom
import numpy as np
import matplotlib.pyplot as plt
import os


def load_dicom_files(directory):
    """Load DICOM files from a directory and return the list of valid slices."""
    full_path = os.path.join(os.getcwd(), directory)
    print(f"Full path: {full_path}")

    # List all files in the directory with their full path
    file_list = [entry.path for entry in os.scandir(full_path) if entry.is_file()]

    files = []
    for fname in file_list:
        try:
            print(f"Loading: {fname}")
            file = pydicom.dcmread(fname)
            files.append(file)
            print(f"SliceLocation: {file.SliceLocation}")
        except Exception as e:
            print(f"Error loading {fname}: {e}")

    return files


def filter_and_sort_slices(files):
    """Filter out files with no SliceLocation and sort by SliceLocation."""
    slices = [f for f in files if hasattr(f, "SliceLocation")]
    skipcount = len(files) - len(slices)
    print(f"Skipped {skipcount} files with no SliceLocation.")
    slices = sorted(slices, key=lambda s: s.SliceLocation)
    return slices


def create_3d_array(slices):
    """Create a 3D numpy array from the DICOM slices."""
    img_shape = list(slices[0].pixel_array.shape)
    img_shape.append(len(slices))  # Add third dimension for slices
    img3d = np.zeros(img_shape)

    # Fill 3D array with the images from the files
    for i, s in enumerate(slices):
        img3d[:, :, i] = s.pixel_array

    return img3d


def plot_slices(img3d, ps, ss):
    """Plot the orthogonal slices."""
    # Pixel aspects, assuming all slices are the same
    ax_aspect = ps[1] / ps[0]  # Aspect ratio for axial view (depth in Z)
    sag_aspect = ps[1] / ss  # Aspect ratio for sagittal view (Left-to-right side view)
    cor_aspect = ss / ps[0]  # Aspect ratio for coronal view (Front-to-back view)

    # Plotting
    fig, axs = plt.subplots(2, 2, figsize=(10, 10))

    # Axial view (depth in Z)
    axs[0, 0].imshow(img3d[:, :, img3d.shape[2] // 2], cmap="gray")
    axs[0, 0].set_title('Axial view')
    axs[0, 0].set_aspect(ax_aspect)

    # Sagittal view (Left-to-right side view)
    axs[0, 1].imshow(img3d[:, img3d.shape[1] // 2, :], cmap="gray")
    axs[0, 1].set_title('Sagittal view')
    axs[0, 1].set_aspect(sag_aspect)

    # Coronal view (Front-to-back view)
    axs[1, 0].imshow(img3d[img3d.shape[0] // 2, :, :].T, cmap="gray")
    axs[1, 0].set_title('Coronal view')
    axs[1, 0].set_aspect(cor_aspect)
    axs[1, 1].axis('off')  # Optionally hide the 4th subplot
    # Adjust spacing between subplots
    plt.subplots_adjust(hspace=0.4, wspace=0.4)
    plt.show()


def main():
    # Load the DICOM files
    directory_name = "series-000001"  # CT DICOM sample from https://www.dicomlibrary.com/
    files = load_dicom_files(directory_name)

    # Filter and sort the slices
    slices = filter_and_sort_slices(files)

    if slices:
        # Pixel spacing and slice thickness
        ps = slices[0].PixelSpacing  # Pixel spacing [mm] in X and Y directions
        ss = slices[0].SliceThickness  # Slice thickness [mm]

        # Create 3D image array
        img3d = create_3d_array(slices)

        # Plot the orthogonal slices
        plot_slices(img3d, ps, ss)
    else:
        print("No valid slices found.")


if __name__ == "__main__":
    main()

