import pydicom
import numpy as np
import os
import pyvista as pv

# load the DICOM files
directory_name="series-000001" #CT DICOM sample from https://www.dicomlibrary.com/
full_path=os.path.join(os.getcwd(),directory_name)
print(f"full path: {full_path}")

# List all files in the directory with their full path 
file_list=[entry.path for entry in os.scandir(full_path) if entry.is_file()]
files = []

for fname in file_list:
    print(f"loading: {fname}")
    files.append(pydicom.dcmread(fname))
    print(pydicom.dcmread(fname).SliceLocation)
print(f"file count: {len(files)}")
# SliceLocation is used to indicate relative position of a particular slice in a 3D imaging study
#SliceLocation  in DCIM files is used to determine the order of the slices
# skip files with no SliceLocation (eg scout views)
slices = []
skipcount = 0
for f in files:
    if hasattr(f, "SliceLocation"):
        slices.append(f)
    else:
        skipcount = skipcount + 1

print(f"skipcount values: {skipcount}")
# sort the dicom files based on the SliceLocation tag
slices = sorted(slices, key=lambda s: s.SliceLocation)

# pixel aspects, assuming all slices are the same
ps = slices[0].PixelSpacing # Pixel spacing [mm] in X and Y directions
ss = slices[0].SliceThickness #Slice thikness [mm]
ax_aspect = ps[1] / ps[0]  # Aspect ratio for axial view (depth in Z)
sag_aspect = ps[1] / ss  # Aspect ratio for sagittal view (Left-to-right side view)
cor_aspect = ss / ps[0] # Aspect ratio for coronal view (Front-to-back view)

# create 3D array

#get 2D image size [rows,cols]
img_shape = list(slices[0].pixel_array.shape)
#add the third dimension : number of slices
img_shape.append(len(slices))
# img3d : empty 3D array
img3d = np.zeros(img_shape)

# fill 3D array with the images from the files
for i, s in enumerate(slices):
    img2d = s.pixel_array
    img3d[:, :, i] = img2d

# use PyVista to display the 3D volume
# Convert the 3D NumPy array into a PyVista grid
volume = pv.wrap(img3d)

# Set up a plotter for the 3D volume
plotter = pv.Plotter()
plotter.add_volume(volume,cmap="gray")  # Display the volume with a grayscale colormap

# Add a scalar bar to indicate intensity levels
plotter.add_scalar_bar(title="Intensity")

# Show the 3D visualization
plotter.show()
