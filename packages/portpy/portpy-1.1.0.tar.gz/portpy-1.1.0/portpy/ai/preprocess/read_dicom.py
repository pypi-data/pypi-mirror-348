# Read dicom files from dicom directory
import os
import SimpleITK as sitk
from pydicom import dcmread
import numpy as np


def read_dicom(in_dir, case):
    dicom_names = os.listdir(os.path.join(in_dir, case))
    dicom_paths = []
    for dcm in dicom_names:
        if dcm[:2] == 'CT':
            dicom_paths.append(os.path.join(in_dir, case, dcm))

    img_positions = []
    for dcm in dicom_paths:
        ds = dcmread(dcm)
        img_positions.append(ds.ImagePositionPatient[2])

    indexes = np.argsort(np.asarray(img_positions))
    dicom_names = list(np.asarray(dicom_paths)[indexes])

    reader = sitk.ImageSeriesReader()
    reader.SetFileNames(dicom_names)
    img = reader.Execute()

    return img


# in_dir = '/data/MSKCC-Intern-2021/Dose-Echo-Data/pCT_Dose_ECHO_dicomset'
# out_dir = '/data/MSKCC-Intern-2021/Dose-Echo-Data/pCT_Dose_ECHO_dicomset_extracted'

# in_dir = r'\\pensmph6\MpcsResearch1\YangJ\lung-echo\out'
# out_dir = r'\\pisidsmph\NadeemLab\Gourav\lung-manual-dicomextracted'
# in_dir = r'\\pensmph6\mpcsresearch1\YangJ\lung-echo\out-ECHO'
# out_dir = r'\\pensmph6\mpcsresearch1\YangJ\lung-echo\pred'
in_dir = r'\\pisidsmph\Treatplanapp\ECHO\Research\Data_newformat'
out_dir = r'\\pisidsmph\Treatplanapp\ECHO\Research\Data_newformat\Paraspinal\ECHO_PARAS_3$ECHO_20200003'
if not os.path.exists(out_dir):
    os.makedirs(out_dir)

cases = os.listdir(in_dir)
cases = ['CTData']
for idx, case in enumerate(cases):
    try:
        print('Processing case {}: {} of {} ...'.format(case, idx + 1, len(cases)))
        img = read_dicom(in_dir, case)
        filename = os.path.join(out_dir, case + '_CT.nrrd')
        sitk.WriteImage(img, filename)
    except:
        print('Processing of case {} failed'.format(case))
        pass

img = sitk.ReadImage(
    r'\\pisidsmph\Treatplanapp\ECHO\Research\Data_newformat\Paraspinal\ECHO_PARAS_3$ECHO_20200003\CTData_CT.nrrd')
img_arr = sitk.GetArrayFromImage(img)
img_arr = img_arr.permute
img_arr_slice_last = np.moveaxis(img_arr, 0, -1)  # Slices last
# import matplotlib.pyplot as plt
# fig = plt.figure()
# plt.imshow(img_arr_slice_last[:,:,100], cmap='gray')
# import h5py
#
# with h5py.File(
#         r'\\pisidsmph\Treatplanapp\ECHO\Research\Data_newformat\Paraspinal\ECHO_PARAS_3$ECHO_20200003\Data\CT_Data.h5',
#         'w') as hf:
#     hf.create_dataset("CT", data=img_arr_slice_last)
# b = dcmread(
#     r'\\pisidsmph\Treatplanapp\ECHO\Research\Data_newformat\CTData\CT.1.2.840.1275.2208.2.1.4.3024394737.5524.1587142543.3594.dcm')
# CT_MetaData = {}
# CT_MetaData['BottomLeftCorner_mm'] = img.GetOrigin()
# CT_MetaData['VoxelSpacing_XYZ_mm'] = img.GetSpacing()
# CT_MetaData['Size_XYZ'] = img.GetSize()
# CT_MetaData['Direction_XYZ'] = img.GetDirection()
# CT_MetaData['Tube_Voltage_KV'] = b.KVP
# CT_MetaData['ScannerManufacturer'] = b.Manufacturer
# CT_MetaData['ScannerManufacturerModel'] = b.ManufacturerModelName
# CT_MetaData['ReconstructionAlgorithm'] = b.ConvolutionKernel
# CT_MetaData['CTImage_File'] = 'CTData.h5'
# import json
#
# with open(
#         r'\\pisidsmph\Treatplanapp\ECHO\Research\Data_newformat\Paraspinal\ECHO_PARAS_3$ECHO_20200003\Data\CT_MetaData.json',
#         'w') as fp:
#     json.dump(CT_MetaData, fp, indent=4)
# ctVoxInd = np.zeros((np.prod(np.shape(img_arr_slice_last)), 1))
# HU = np.zeros((np.prod(np.shape(img_arr_slice_last)), 1))
# count = 0
# for i in range(img_arr_slice_last.shape[0]):
#     for j in range(img_arr_slice_last.shape[1]):
#         for k in range(img_arr_slice_last.shape[2]):
#             ctVoxInd[count] = count
#             HU[count] = img_arr_slice_last[i, j, k]
#             count = count + 1
#
# import matplotlib.pyplot as plt
#
#
# def myshow(img, slice):
#     nda = sitk.GetArrayFromImage(img)
#     show_slice = nda[slice, :, :]
#     plt.imshow(show_slice, cmap='gray')
#     plt.title = 'Slice# {}'.format(slice)


image_viewer = sitk.ImageViewer()
# Uncomment the line below to change the default external viewer to your viewer of choice and test that it works.
image_viewer.SetApplication('C:/ProgramData/NA-MIC/Slicer 4.11.20210226/Slicer')

image_viewer.Execute(img)