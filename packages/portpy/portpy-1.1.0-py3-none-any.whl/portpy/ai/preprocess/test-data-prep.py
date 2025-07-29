# Test if 3D data with DVH histograms are properly prepared

import os
import numpy as np
import matplotlib.pyplot as plt


in_dir = r'\\pisidsmph\NadeemLab\Interns\Navdeep\msk-echo-3d-dvh-beamlet-sparse-separate-ptv\test'
case = '38067564.npz'

filename = os.path.join(in_dir, case)
data = np.load(filename)

ct = data['CT']
dose = data['DOSE']
oar = data['OAR']
hist = data['HIST']
bins = data['BINS']
beam = data['BEAM']

print(hist.shape)
print(hist[:,2])
# plt.imshow(beam[65], cmap='gray')
# plt.show()
#
# plt.imshow(dose[65], cmap='gray')
# plt.show()
# fig = plt.figure()
# plt.plot(hist[:,2])
# plt.show()
# fig = plt.figure()
# ax = plt.axes()
# ax.scatter(oar[0], cmap='Greens')
# plt.show()

for i in range(hist.shape[1]):
	plt.plot(bins, hist[:,i])

plt.legend(['Eso', 'Cord', 'Heart', 'Lung_L', 'Lung_R', 'PTV'])
plt.xlabel('Dose (Gy)')
plt.ylabel('Volume Fraction (%)')
plt.show()

# import pydicom
# import pydicom_seg
# import SimpleITK as sitk
#
# dcm = pydicom.dcmread(r'\\pensmph6\mpcsresearch1\YangJ\lung-echo\out-ECHO\00191656\RS.1.2.246.352.71.4.565238251846.56541.20210304153054')
#
# reader = sitk.ImageSeriesReader()
# result = reader.GetGDCMSeriesFileNames(dcm)
# reader.SetFileNames(result)
# dicoms = reader.Execute()
# sitk.WriteImage(dicoms, r'\\pensmph6\mpcsresearch1\YangJ\lung-echo\out-ECHO\00191656\RS.1.2.246.352.71.4.565238251846.56541.20210304153054.nrrd') #fileName like "brain.nrrd"
#
# for segment_number in result.available_segments:
#     image_data = result.segment_data(segment_number)  # directly available
#     image = result.segment_image(segment_number)  # lazy construction
#     sitk.WriteImage(image, f'/tmp/segmentation-{segment_number}.nrrd', True)