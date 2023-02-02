import numpy as np
import os
from pathlib import Path
import pydicom
import sys


def find_first_entry_containing_substring(list_of_attributes, substring, dtype=np.float32):
    line = list_of_attributes[np.char.find(list_of_attributes, substring)>=0][0]
    if dtype == np.float32:
        return np.float32(line.replace('\n', '').split(':=')[-1])
    elif dtype == str:
        return (line.replace('\n', '').split(':=')[-1].replace(' ', ''))
    elif dtype == int:
        return int(line.replace('\n', '').split(':=')[-1].replace(' ', ''))

def intf2dcm(headerfile):
    # Interfile attributes   
    with open(headerfile) as f:
        headerdata = f.readlines()
    headerdata = np.array(headerdata)
    dim1 = find_first_entry_containing_substring(headerdata, 'matrix size [1]', int)
    dim2 = find_first_entry_containing_substring(headerdata, 'matrix size [2]', int)
    dim3 = find_first_entry_containing_substring(headerdata, 'matrix size [3]', int)
    dx = find_first_entry_containing_substring(headerdata, 'scaling factor (mm/pixel) [1]', np.float32) 
    dy = find_first_entry_containing_substring(headerdata, 'scaling factor (mm/pixel) [2]', np.float32) 
    dz = find_first_entry_containing_substring(headerdata, 'scaling factor (mm/pixel) [3]', np.float32) 
    number_format = find_first_entry_containing_substring(headerdata, 'number format', str)
    num_bytes_per_pixel = find_first_entry_containing_substring(headerdata, 'number of bytes per pixel', np.float32)
    imagefile = find_first_entry_containing_substring(headerdata, 'name of data file', str)
    pixeldata = np.fromfile(os.path.join(str(Path(headerfile).parent), imagefile), dtype=np.float32)
    dose_scaling_factor = np.max(pixeldata) / (2**16 - 1) 
    pixeldata /= dose_scaling_factor
    pixeldata = pixeldata.astype(np.int32)

    ds = pydicom.read_file(os.path.join(str(Path(os.path.realpath(__file__)).parent), "template.dcm"))
    ds.BitsAllocated = 32
    ds.Rows = dim1
    ds.Columns = dim2
    ds.PixelRepresentation = 0
    ds.NumberOfFrames = dim3
    ds.PatientName = "Unknown"
    ds.PatientID = "Unknown"
    ds.PixelSpacing = [dx, dy]
    ds.SliceThickness = dz
    ds.PixelData = pixeldata.tobytes()
    return ds