# Read dicom files from dicom directory
import os
import SimpleITK as sitk
from pydicom import dcmread
import numpy as np


def read_dicom(in_dir, case):
	dicom_names = os.listdir(os.path.join(in_dir, case))
	dicom_paths = []
	for dcm in dicom_names:
		if dcm[:2] == 'RD':
			dose_file_name = os.path.join(in_dir, case, dcm)

	img_positions = []
	#for dcm in dicom_paths:
	#	ds = dcmread(dcm)
	# img = ds.pixel_array
	dose_img = dcmread(dose_file_name)
	# dose_img = sitk.ReadImage([dcm for dcm in dicom_paths])
	arr_dose = dose_img.pixel_array
	rt_dose = arr_dose*dose_img.DoseGridScaling
	rt_dose_itk = sitk.GetImageFromArray(rt_dose)
	rt_dose_itk.SetOrigin(dose_img.ImagePositionPatient)
	rt_dose_itk.SetSpacing([np.float(dose_img.PixelSpacing[0]), np.float(dose_img.PixelSpacing[1]), dose_img.GridFrameOffsetVector[1]-dose_img.GridFrameOffsetVector[0]])
	# rt_dose_itk.SetDirection(dose_img.GetDirection())
		#img_positions.append(ds.ImagePositionPatient[2])
	# x_coord = np.float(dose_img.ImagePositionPatient[0]) + np.float(dose_img.PixelSpacing[0])*np.arange(0, dose_img.Columns)
	# y_coord = np.float(dose_img.ImagePositionPatient[1]) + np.float(dose_img.PixelSpacing[1]) * np.arange(0, dose_img.Rows)
	# z_coord = np.float(dose_img.ImagePositionPatient[2]) + np.array(dose_img.GridFrameOffsetVector)
	# dose_array = np.zeros(sitk.GetArrayFromImage(arr_dose).shape, dtype=np.float)

	# indexes = np.argsort(np.asarray(img_positions))
	# dicom_names = list(np.asarray(dicom_paths)[indexes])
	#
	#reader = sitk.ImageSeriesReader()
	# reader.SetFileNames(dicom_names)
	# img = reader.Execute()

	# return dose_img
	return rt_dose_itk

# in_dir = '/data/MSKCC-Intern-2021/Dose-Echo-Data/pCT_Dose_ECHO_dicomset'
# out_dir = '/data/MSKCC-Intern-2021/Dose-Echo-Data/pCT_Dose_ECHO_dicomset_extracted'

in_dir = r'\\pensmph6\MpcsResearch1\YangJ\lung-echo\out'
in_dir = r'\\pensmph6\mpcsresearch1\YangJ\lung-echo\test1\Uniform'
# out_dir = r'\\pisidsmph\NadeemLab\Gourav\lung-echo-dicomextracted'
out_dir = r'\\pisidsmph\NadeemLab\Gourav\lung-manual-dicomextracted'

# in_dir = r'\\pensmph6\mpcsresearch1\YangJ\lung-echo\test1'
# out_dir = r'\\pensmph6\mpcsresearch1\YangJ\lung-echo\Pred'

in_dir = r'\\pensmph6\mpcsresearch1\YangJ\lung-echo\out-ECHO'
out_dir = r'\\pensmph6\mpcsresearch1\YangJ\lung-echo\pred'
if not os.path.exists(out_dir):
	os.makedirs(out_dir)

cases = os.listdir(in_dir)
# cases = ['00191656']
# cases = ['38102054']
cases = ['35466237', '35510645', '35516407', '35552402', '38004274', '38013938', '35211672','35266805',
		 '35392859', '35481820', '35484001', '35500404', '35516168', '35530886', '35531238', '35545960', '35550432']
cases = ['LUNG1-002', 'LUNG1-005']
for idx, case in enumerate(cases):
	try:
		print('Processing case {}: {} of {} ...'.format(case, idx + 1, len(cases)))
		dose_img = read_dicom(in_dir, case)
		filename = os.path.join(out_dir, case + '_dose_ECHO.nrrd')
		# filename = os.path.join(out_dir, case + '_dose.nrrd')
		# dose_img.save_as(filename)
		sitk.WriteImage(dose_img, filename)
	except:
		print('Processing of case {} failed'.format(case))
		pass


# from dicompylercore import dicomparser, dvh, dvhcalc

# Access DVH data
#rtdose = dicomparser.DicomParser(r'\\pensmph6\mpcsresearch1\YangJ\lung-echo\out-ECHO\00191656\RD.1.2.246.352.71.7.565238251846.1160518.20210304160056')
# import matplotlib.pyplot as plt
# from pydicom import dcmread
# from pydicom.data import get_testdata_file