from refined_landmarking import Final_DiffusionNet
from refined_landmarking import Predictions_to_coordinates_Refined
from refined_landmarking import Segmentation
from common_functions import Realign_coordinates

import numpy as np
import argparse
import pandas as pd
import os
import pymeshlab
from tqdm import tqdm

default_demo_dir = 'demo'

parser = argparse.ArgumentParser()
parser.add_argument("--input_folder", type=str, help="Select the input folder", default=default_demo_dir)
parser.add_argument("--export_realigned_mesh", action="store_true", help="Export the realigned mesh", default=False)
parser.add_argument("--save_segmented_mesh", action="store_true", help="Export the facial segmentation", default=False)
args = parser.parse_args()

input_folder = args.input_folder     # select the folder in which the obj/stl file is placed. The algorithm expects each obj/stl file to be in a different folder
folders = os.listdir(input_folder) # the folders in the input_folder in which the input obj/stlL files should be saved

print("Folders found: {}".format(len(folders)))

save_segmented_mesh = args.save_segmented_mesh

for folder in folders: 
    
    folder_path = os.path.join(input_folder, folder) # select folder containing input obj/stl file

    files = []
    for file in os.listdir(folder_path):
        if (file.endswith(".obj") or file.endswith('.stl')) and not (file.endswith('_mm.obj') or file == 'Template.obj'):
            files.append(file)

    if len(files) == 0:
        continue

    print("Processing folder '{}' with {} files.".format(folder, len(files)))
    
    output_folder = os.path.join(input_folder, folder, 'output')   

    for scan_file in tqdm(files):
        lm_csv = os.path.join(output_folder,scan_file[:-4] + '_rough_predictions_original.csv')
        if not os.path.exists(lm_csv):
            continue

        coordinates_inital_predictions = np.asarray(pd.read_csv(lm_csv , sep=',', header=None).values[:,1:], dtype=np.float32)

        aligned_coordinates, translation, rot_m1, rot_m2 = Realign_coordinates.determine_alignment.calculate_rotation_matrices(coordinates_inital_predictions)
        verts, faces, normals = Segmentation.Facial_segmentation.segment(folder_path, scan_file, translation, rot_m1, rot_m2, save_segmented_mesh)
        preds_final_DiffNet = Final_DiffusionNet.Predictions_Final_DiffusionNet.Predict(verts, faces, normals)
        coordinates_final_predictions = Predictions_to_coordinates_Refined.predictions_to_coordinates.determine_coordinates(verts, preds_final_DiffNet.T)
        realigned_predictions, translation2, rot_m3, rot_m4 = Realign_coordinates.determine_alignment.calculate_rotation_matrices(coordinates_final_predictions)
        
        # transform the predictions to the coordinate system of the original scan file
        prediction_original_location = np.dot(coordinates_final_predictions, -rot_m2[:3,:3])
        prediction_original_location2 = np.dot(prediction_original_location, -rot_m1[:3,:3])

        prediction_original_location2_x = prediction_original_location2.copy()[:,0] + translation[0]
        prediction_original_location2_y = prediction_original_location2.copy()[:,1] + translation[1]
        prediction_original_location2_z = prediction_original_location2.copy()[:,2] + translation[2]
        prediction_original_location3 = np.asarray([prediction_original_location2_x, prediction_original_location2_y, prediction_original_location2_z]).T

        # save landmarks refined landmarks in original position
        csv_file = []
        csv_file.append(['Right_exocanthion', prediction_original_location3[0,0], prediction_original_location3[0,1], prediction_original_location3[0,2]])
        csv_file.append(['Left_exocanthion', prediction_original_location3[1,0], prediction_original_location3[1,1], prediction_original_location3[1,2]])
        csv_file.append(['Right_endocanthion', prediction_original_location3[2,0], prediction_original_location3[2,1], prediction_original_location3[2,2]])
        csv_file.append(['Left_endocanthion', prediction_original_location3[3,0], prediction_original_location3[3,1], prediction_original_location3[3,2]])
        csv_file.append(['Nasion', prediction_original_location3[4,0], prediction_original_location3[4,1], prediction_original_location3[4,2]])
        csv_file.append(['Nose_tip', prediction_original_location3[5,0], prediction_original_location3[5,1], prediction_original_location3[5,2]])
        csv_file.append(['Right_alare', prediction_original_location3[6,0], prediction_original_location3[6,1], prediction_original_location3[6,2]])
        csv_file.append(['Left_alare', prediction_original_location3[7,0], prediction_original_location3[7,1], prediction_original_location3[7,2]])
        csv_file.append(['Right_cheilion', prediction_original_location3[8,0], prediction_original_location3[8,1], prediction_original_location3[8,2]])
        csv_file.append(['Left_cheilion', prediction_original_location3[9,0], prediction_original_location3[9,1], prediction_original_location3[9,2]])
        pd.DataFrame(csv_file).to_csv(os.path.join(output_folder, scan_file[:-4] + '_refined_predictions_original.csv'), sep=',', header=False, index=False)

        if args.export_realigned_mesh:
            # realign  mesh 
            ms = pymeshlab.MeshSet()
            ms.load_new_mesh(os.path.join(folder_path, scan_file))
            ms.compute_matrix_from_translation(axisx = -translation[0], axisy = -translation[1], axisz = -translation[2])
            ms.set_matrix(transformmatrix = rot_m1)
            ms.set_matrix(transformmatrix = rot_m2)
            ms.compute_matrix_from_translation(axisx = -translation2[0], axisy = -translation2[1], axisz = -translation2[2])
            ms.set_matrix(transformmatrix = rot_m3)
            ms.set_matrix(transformmatrix = rot_m4)
            ms.save_current_mesh(os.path.join(output_folder, scan_file[:-4] + '_refined_realigned_mesh.obj'))
            ms.clear()

            # save refined landmarks in realigned position
            csv_file = []
            csv_file.append(['Right_exocanthion', realigned_predictions[0,0], realigned_predictions[0,1], realigned_predictions[0,2]])
            csv_file.append(['Left_exocanthion', realigned_predictions[1,0], realigned_predictions[1,1], realigned_predictions[1,2]])
            csv_file.append(['Right_endocanthion', realigned_predictions[2,0], realigned_predictions[2,1], realigned_predictions[2,2]])
            csv_file.append(['Left_endocanthion', realigned_predictions[3,0], realigned_predictions[3,1], realigned_predictions[3,2]])
            csv_file.append(['Nasion', realigned_predictions[4,0], realigned_predictions[4,1], realigned_predictions[4,2]])
            csv_file.append(['Nose_tip', realigned_predictions[5,0], realigned_predictions[5,1], realigned_predictions[5,2]])
            csv_file.append(['Right_alare', realigned_predictions[6,0], realigned_predictions[6,1], realigned_predictions[6,2]])
            csv_file.append(['Left_alare', realigned_predictions[7,0], realigned_predictions[7,1], realigned_predictions[7,2]])
            csv_file.append(['Right_cheilion', realigned_predictions[8,0], realigned_predictions[8,1], realigned_predictions[8,2]])
            csv_file.append(['Left_cheilion', realigned_predictions[9,0], realigned_predictions[9,1], realigned_predictions[9,2]])
            pd.DataFrame(csv_file).to_csv(os.path.join(output_folder, scan_file[:-4] + '_refined_predictions_realigned.csv'), sep=',', header=False, index=False)

        

    
