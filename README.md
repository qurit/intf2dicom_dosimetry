To convert interfiles to DICOM:

1. Clone this repository to `/path/to/intf2dicom_dosimetry`
2. In whatever python script your using, add `sys.path.append('`/path/to/intf2dicom_dosimetry/src')` at the top of the script
3. Then `from intf2dicom_dosimetry import intf2dcm`.
4. Make sure the interfile header and data are in the same directory. Then use `intf2dcm(headerfile_path)` to convert the interfile header to a pydicom dataset.
