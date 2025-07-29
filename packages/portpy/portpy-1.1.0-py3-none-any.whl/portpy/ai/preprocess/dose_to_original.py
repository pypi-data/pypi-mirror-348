import SimpleITK as sitk
import numpy as np
import matplotlib.pyplot as plt
import os
from skimage.transform import resize


def get_dataset(in_dir, case, suffix):
    filename = os.path.join(in_dir, case + suffix)
    img = None
    if os.path.exists(filename):
        img = sitk.ReadImage(filename)
        img = sitk.GetArrayFromImage(img)

    return img


def resample(img, ref_image):
    resampler = sitk.ResampleImageFilter()
    resampler.SetInterpolator(sitk.sitkLinear)
    resampler.SetReferenceImage(ref_image)
    img = resampler.Execute(img)

    return img


def resample_dose(dose, ref_dose):
    dose = sitk.GetArrayFromImage(dose)
    # dose = dose * 74.0

    dims = sitk.GetArrayFromImage(ref_dose).shape
    dose = np.moveaxis(dose, 0, -1)  # Channels last
    expected_shape = (dims[1], dims[2], dims[0])
    dose = resize(dose, expected_shape, order=1, preserve_range=True, anti_aliasing=False)
    dose = np.moveaxis(dose, -1, 0)
    dose = sitk.GetImageFromArray(dose)
    dose.SetOrigin(ref_dose.GetOrigin())
    dose.SetDirection(ref_dose.GetDirection())
    dose.SetSpacing(ref_dose.GetSpacing())

    return dose


def crop_img(img, start, end, is_mask=False):
    # Crop to setting given by start/end coordinates list, assuming depth,height,width
    img_arr = sitk.GetArrayFromImage(img)
    img_cropped = img_arr[start[0]:end[0] + 1, start[1]:end[1], start[2]:end[2]]
    img_cropped = sitk.GetImageFromArray(img_cropped)
    img_cropped.SetOrigin(img.GetOrigin())
    img_cropped.SetDirection(img.GetDirection())
    img_cropped.SetSpacing(img.GetSpacing())
    # img_cropped = np.moveaxis(img_cropped, 0, -1)  # Slices last
    #
    # order = 0
    # if is_mask is False:
    #     order = 1
    # img_resized = resize(img_cropped, (128, 128, 128), order=order, preserve_range=True, anti_aliasing=False).astype(np.float32)
    # if is_mask is True:
    #     img_resized = img_resized.astype(np.uint8)
    #
    # img_resized = np.moveaxis(img_resized, -1, 0)  # Slices first again

    return img_cropped

def get_crop_settings(oar):
    # Use to get crop settings
    # Don't use cord or eso as they spread through more slices
    # If total number of slices is less than 128 then don't crop at all
    # Use start and end index from presence of any anatomy or ptv
    # If that totals more than 128 slices then leave as is.
    # If that totals less than 128 slices then add slices before and after to make total slices to 128

    oar1 = oar.copy()
    oar1[np.where(oar == 1)] = 0
    oar1[np.where(oar == 2)] = 0

    # For 2D cropping just do center cropping 256x256
    center = [0, oar.shape[1] // 2, oar1.shape[2] // 2]
    start = [0, center[1] - 150, center[2] - 150]
    end = [0, center[1] + 150, center[2] + 150]

    depth = oar1.shape[0]
    if depth < 128:
        start[0] = 0
        end[0] = depth

        return start, end

    first_slice = -1
    last_slice = -1
    for i in range(depth):
        frame = oar1[i]
        if np.any(frame):
            first_slice = i
            break
    for i in range(depth - 1, -1, -1):
        frame = oar1[i]
        if np.any(frame):
            last_slice = i
            break

    expanse = last_slice - first_slice + 1
    if expanse >= 128:
        start[0] = first_slice
        end[0] = last_slice

        return start, end

    # print('Get\'s here')
    slices_needed = 128 - expanse
    end_slices = slices_needed // 2
    beg_slices = slices_needed - end_slices

    room_available = depth - expanse
    end_room_available = depth - last_slice - 1
    beg_room_available = first_slice

    leftover_beg = beg_room_available - beg_slices
    if leftover_beg < 0:
        end_slices += np.abs(leftover_beg)
        first_slice = 0
    else:
        first_slice = first_slice - beg_slices

    leftover_end = end_room_available - end_slices
    if leftover_end < 0:
        first_slice -= np.abs(leftover_end)
        last_slice = depth - 1
    else:
        last_slice = last_slice + end_slices

    if first_slice < 0:
        first_slice = 0

    start[0] = first_slice
    end[0] = last_slice

    return start, end


def process_case(in_dir, case):
    # ct = get_dataset(in_dir, case, '_CT.nrrd')
    # dose = get_dataset(in_dir, case, '_dose_resampled.nrrd')
    oar = get_dataset(in_dir, case, '_RTSTRUCTS.nrrd')
    ptv = get_dataset(in_dir, case, '_PTV.nrrd')

    oar[np.where(ptv == 1)] = 6

    start, end = get_crop_settings(oar)

    return start, end

def attach_slices(pred_dose, ref_dose, start, end):
    dose = sitk.GetArrayFromImage(pred_dose)
    # dose = dose * 74.0
    ref_dose_arr = sitk.GetArrayFromImage(ref_dose)
    # ref_dose_copy = ref_dose
    ref_dose_arr[start[0]:end[0] + 1, start[1]:end[1], start[2]:end[2]] = dose
    # dose = ref_dose_arr
    # ref_dose = sitk.GetImageFromArray(ref_dose)
    dose = sitk.GetImageFromArray(ref_dose_arr)
    dose.SetOrigin(ref_dose.GetOrigin())
    dose.SetDirection(ref_dose.GetDirection())
    dose.SetSpacing(ref_dose.GetSpacing())

    return dose

def read_influence_matrix(in_dir, case):
    filename = os.path.join(in_dir, case, 'Dose.txt')  # Sparse
    # filename = os.path.join(in_dir, case, 'Dose1.txt')   # Dense Beam Echo
    # filename = os.path.join(in_dir, case, 'Dose2.txt')  # Dense beam Manual
    beamlet_info = np.genfromtxt(filename)
    return beamlet_info

cases = ['LUNG1-002', 'LUNG1-005']
gt_dir = r'\\pensmph6\mpcsresearch1\YangJ\lung-echo\pred'
pred_dir = r'\\pensmph\MphShared\Treatment Planning\ECHO\Bi-weekly meeting\Gourav\DosePrediction'

for idx, case in enumerate(cases):
    filename = os.path.join(gt_dir, case + '_CT.nrrd')
    ct = sitk.ReadImage(filename)

    filename = os.path.join(gt_dir, case + '_dose_ECHO.nrrd')
    # filename = os.path.join(gt_dir, case + '_dose.nrrd')
    gt_dose = sitk.ReadImage(filename)
    gt_dose_resampled_to_orgCT = resample(gt_dose, ct)

    filename = os.path.join(gt_dir, case + '_CT2DOSE.nrrd')
    pred_dose = sitk.ReadImage(filename)

    # Undo the crop settings we used
    start, end = process_case(gt_dir, case)    # Get the crop setting
    gt_dose_to_ct_cropped = crop_img(gt_dose_resampled_to_orgCT, start, end, is_mask=False)  # Crop the actual dose to crop CT
    pred_dose = resample_dose(pred_dose, gt_dose_to_ct_cropped)  # First get pred dose to cropped dose dimensions
    pred_dose = attach_slices(pred_dose, gt_dose_resampled_to_orgCT, start, end)    # attach cropped slices of actual dose
    pred_dose_resampled = resample(pred_dose, gt_dose)      # resample the undo-crop to original dose


    filename = os.path.join(pred_dir, case + '_pred_dose_original_resolution.nrrd')
    sitk.WriteImage(pred_dose_resampled, filename)


in_dir_infMatrix = r'\\pensmph6\mpcsresearch1\YangJ\lung-echo\influenceMatrix'
cases = ['LUNG1-002', 'LUNG1-005']


for idx, case in enumerate(cases):

    print('Processing case: {} {} of {} ...'.format(case, idx+1, len(cases)))
    beamlet_info = read_influence_matrix(in_dir_infMatrix, case)
    filename = os.path.join(pred_dir, case + '_pred_dose_on_echo_points.txt')
    with open(filename, 'w') as f:
        for row in beamlet_info:
            curr_pt = (row[0], row[1], row[2])
            # curr_val = row[3]
            # list_curr_pt = [0] + list(curr_pt)
            # curr_pt = tuple(list_curr_pt)
            curr_indx = pred_dose_resampled.TransformPhysicalPointToIndex(curr_pt)  # X,Y,Z

            print('{} {} {} {}'.format(row[0], row[1], row[2], pred_dose_resampled[curr_indx[0], curr_indx[1], curr_indx[2]]), file=f)

    filename = os.path.join(pred_dir, case + '_actual_dose_on_echo_points.txt')
    with open(filename, 'w') as f:
        for row in beamlet_info:
            curr_pt = (row[0], row[1], row[2])
            # curr_val = row[3]
            # list_curr_pt = [0] + list(curr_pt)
            # curr_pt = tuple(list_curr_pt)
            curr_indx = gt_dose.TransformPhysicalPointToIndex(curr_pt)  # X,Y,Z

            print('{} {} {} {}'.format(row[0], row[1], row[2], gt_dose[curr_indx[0], curr_indx[1], curr_indx[2]]), file=f)
