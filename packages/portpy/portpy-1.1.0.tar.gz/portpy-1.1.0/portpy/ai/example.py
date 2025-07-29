import os
import portpy.photon as pp
import SimpleITK as sitk
import os
import cvxpy as cp
import numpy as np
import matplotlib.pyplot as plt
from preprocess.predict_using_model import predict_using_model

# # preprocess portpy data
in_dir = r'\\pisidsmph\Treatplanapp\ECHO\Research\Data_newformat\PortPy\data'
# out_dir = r'./dataset'
model_name = 'portpy_test_2'
# os.system('python3 ./preprocess/data_preprocess.py --in_dir {} --out_dir'.format(in_dir, out_dir))
#
# # # train the data
# os.system(
#     'python3 train.py --dataroot ./dataset --netG unet_128 --name {} --model doseprediction3d --direction AtoB --lambda_L1 1 --dataset_mode dosepred3d --norm batch --batch_size 1 --pool_size 0 --display_port 8097 --lr 0.0002 --input_nc 8 --output_nc 1 --display_freq 10 --print_freq 1 --gpu_ids 0'.format(
#         model_name))
# #
# # # create prediction for the test data
# os.system(
#     'python3 test.py --dataroot ./dataset --netG unet_128 --name {} --phase test --mode eval --model doseprediction3d --input_nc 8 --output_nc 1 --direction AtoB --dataset_mode dosepred3d --norm batch'.format(
#         model_name))
# #
# # # os.system('python3 ./openkbp-stats/dvh-stats-open-kbp.py --planName {}'.format(planName))
# os.system('python3 ./statistics/compute_dvh_stats.py --planName {}'.format(model_name))
# #
# #
# # # convert predicted dose to portpy resolution
# os.system('python3 ./preprocess/pred_dose_to_original_portpy.py --planName {} --in_dir {}'.format(model_name, in_dir))

# # evaluation
# pred_dir = r'./results/{}/test_latest/npz_images'.format(model_name)
# out_dir = r'./results/{}/test_latest/pred_dose'.format(model_name)

# import the predicted dose back to portpy
patient_id = 'Lung_Patient_4'
# pred_dose_img = sitk.ReadImage(os.path.join(out_dir, case + '_pred_dose_original_resolution.nrrd'))
# pred_dose = sitk.GetArrayFromImage(pred_dose_img)
pred_dose = predict_using_model(patient_id=patient_id, in_dir=in_dir, model_name=model_name)

# load portpy data
data = pp.DataExplorer(data_dir=in_dir)
data.patient_id = patient_id
# Load ct and structure set for the above patient using CT and Structures class
ct = pp.CT(data)
ct_arr = ct.ct_dict['ct_hu_3d'][0]
structs = pp.Structures(data)

beams = pp.Beams(data)

# create rinds based upon rind definition in optimization params
protocol_name = 'Lung_2Gy_30Fx'
opt_params = data.load_config_opt_params(protocol_name=protocol_name)
# structs.create_opt_structures(opt_params)

# load influence matrix based upon beams and structure set
inf_matrix = pp.InfluenceMatrix(ct=ct, structs=structs, beams=beams)

# load clinical criteria from the config files for which plan to be optimized
clinical_criteria = pp.ClinicalCriteria(data, protocol_name=protocol_name)

pred_dose_1d = inf_matrix.dose_3d_to_1d(dose_3d=pred_dose)

# create a plan using ct, structures, beams and influence matrix. Clinical criteria is optional
my_plan = pp.Plan(ct, structs, beams, inf_matrix, clinical_criteria)

# create cvxpy problem using the clinical criteria and optimization parameters
opt = pp.Optimization(my_plan, opt_params=opt_params)
# x = opt.vars['x']
A = inf_matrix.A
x = cp.Variable(A.shape[1], pos=True)
opt.vars['x'] = x
ptv_vox = inf_matrix.get_opt_voxels_idx('PTV')
opt.obj += [
    (1 / len(ptv_vox)) * cp.sum_squares(A[ptv_vox, :] @ x - pred_dose_1d[ptv_vox] / my_plan.get_num_of_fractions())]
# voxel weights for oar objectives
all_vox = np.arange(A.shape[0])
oar_voxels = all_vox[~np.isin(np.arange(A.shape[0]), ptv_vox)]
dO = cp.Variable(oar_voxels.shape[0], pos=True)
opt.constraints += [A[oar_voxels, :] @ x <= pred_dose_1d[oar_voxels] / my_plan.get_num_of_fractions() + dO]
opt.obj += [(1 / dO.shape[0]) * cp.sum_squares(dO)]

[Qx, Qy, num_rows, num_cols] = opt.get_smoothness_matrix(inf_matrix.beamlets_dict)
smoothness_X_weight = 0.6
smoothness_Y_weight = 0.4
opt.obj += [(smoothness_X_weight * (1 / num_cols) * cp.sum_squares(Qx @ x) +
            smoothness_Y_weight * (1 / num_rows) * cp.sum_squares(Qy @ x))]

sol = opt.solve(solver='MOSEK', verbose=True)
# sol = opt.solve(solver='MOSEK', verbose=True)
sol = {'optimal_intensity': x.value, 'inf_matrix': inf_matrix}

# plot fluence 3d and 2d for the 1st beam
pp.Visualization.plot_fluence_3d(sol=sol, beam_id=my_plan.beams.get_all_beam_ids()[0])

struct_names = ['PTV', 'ESOPHAGUS', 'HEART', 'CORD']
fig, ax = plt.subplots(figsize=(12, 8))
ax = pp.Visualization.plot_dvh(my_plan, sol=sol, struct_names=struct_names, style='solid', ax=ax, norm_flag=True)
ax = pp.Visualization.plot_dvh(my_plan, dose_1d=pred_dose_1d, struct_names=struct_names, style='dotted', ax=ax,
                               norm_flag=True)
ax.set_title('- Optimized .. Predicted')
plt.show()
