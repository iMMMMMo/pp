import os
import pydicom
from pydicom.dataset import Dataset, FileDataset
from pydicom.uid import generate_uid, ExplicitVRLittleEndian
from pydicom._storage_sopclass_uids import CTImageStorage
from skimage.util import img_as_ubyte
from skimage.exposure import rescale_intensity

class DicomIO:
    def __init__(self):
        self.filename = None
        self.patient_data = None

    def read(self, filename):
        if os.path.exists(filename):
            self.filename = filename
            self.patient_data = pydicom.dcmread(filename)
        else:
            raise FileNotFoundError(f"File not found: {filename}!")
    
    def get_patient_data(self):
        if self.patient_data:
            return self.patient_data
        else:
            raise ValueError("No data. File not loaded!")
    
    def write(self, patient_data, img):
        img_converted = img_as_ubyte(rescale_intensity(img, out_range=(0.0, 1.0)))

        meta = Dataset()
        meta.MediaStorageSOPClassUID = CTImageStorage
        meta.MediaStorageSOPInstanceUID = generate_uid()
        meta.TransferSyntaxUID = ExplicitVRLittleEndian  

        ds = FileDataset(None, {}, preamble=b"\0" * 128)
        ds.file_meta = meta

        ds.SOPInstanceUID = meta.MediaStorageSOPInstanceUID
        ds.PatientName = patient_data["PatientName"]
        ds.PatientID = patient_data["PatientID"]
        ds.ImageComments = patient_data.get("ImageComments", "")

        ds.SeriesInstanceUID = generate_uid()
        ds.StudyInstanceUID = generate_uid()
        ds.FrameOfReferenceUID = generate_uid()

        ds.Rows, ds.Columns = img_converted.shape

        ds.Modality = "CT"
        ds.BitsAllocated = 8
        ds.BitsStored = 8
        ds.HighBit = 7
        ds.PixelRepresentation = 0
        ds.SamplesPerPixel = 1
        ds.PhotometricInterpretation = "MONOCHROME2"
        ds.ImageType = r"ORIGINAL\PRIMARY\AXIAL"

        ds.PixelData = img_converted.tobytes()

        ds.save_as(self.filename, write_like_original=False)
