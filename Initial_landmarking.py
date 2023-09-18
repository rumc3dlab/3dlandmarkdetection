import sys
from initial_landmarking import Initial_DiffusionNet
from initial_landmarking import Predictions_to_coordinates
from common_functions import Realign_coordinates

import pandas as pd
import os
import pymeshlab
import argparse
import shutil
from tqdm import tqdm

default_demo_dir = 'demo'

parser = argparse.ArgumentParser()
parser.add_argument("--input_folder", type=str, help="Select the input folder", default=default_demo_dir)
parser.add_argument("--export_realigned_mesh", action="store_true", help="Export the realigned mesh", default=False)
args = parser.parse_args()


# scans should be in individual folders and in STL or obj format
input_folder = args.input_folder     # select the folder in which the obj/stl file is placed. The algorithm expects each obj/stl file to be in a different folder
folders = os.listdir(input_folder) # the folders in the input_folder in which the input obj/stlL files should be saved

print("Folders found: {}".format(len(folders)))

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
    if not os.path.exists(output_folder):
        os.mkdir(output_folder)
    
    for scan_file in tqdm(files):
        # Load mesh
        ms = pymeshlab.MeshSet()
        ms.load_new_mesh(os.path.join(folder_path, scan_file))
        ms.save_current_mesh(os.path.join(output_folder,scan_file[:-4] + '_original.obj'))

        # Preprocessing - Fix mesh 
        ms.meshing_decimation_quadric_edge_collapse(targetfacenum=50000, preservenormal=True, preservetopology=True, planarquadric=True, preserveboundary=True, autoclean=True) # down sample to 50.000 faces
        ms.meshing_remove_duplicate_faces() # remove duplicate faces
        ms.meshing_remove_duplicate_vertices() # remove duplicate vertices
        
        ms.meshing_repair_non_manifold_edges(method = 'Remove Faces') # repair non manifold edges
        ms.meshing_remove_connected_component_by_diameter(mincomponentdiag = pymeshlab.Percentage(5), removeunref = True) # remove small unconnected parts of the mesh 
        ms.meshing_close_holes(maxholesize = 100) # close holes 
        ms.meshing_repair_non_manifold_edges(method = 'Remove Faces') # repair non manifold edges
        
        # determine the vertices, faces, and normals of the mesh
        mesh = ms.current_mesh()
        verts = pymeshlab.Mesh.vertex_matrix(mesh) 
        faces = pymeshlab.Mesh.face_matrix(mesh) 
        normals = pymeshlab.Mesh.vertex_normal_matrix(mesh) #
        ms.clear()

        # use the initial DiffusionNet to roughly predict the landmarks 
        preds_initial_DiffNet = Initial_DiffusionNet.Predictions_Initial_DiffusionNet.Predict(verts, faces, normals)

        coordinates_inital_predictions = Predictions_to_coordinates.predictions_to_coordinates.determine_coordinates(verts, preds_initial_DiffNet.T)
        aligned_coordinates, translation, rot_m1, rot_m2 = Realign_coordinates.determine_alignment.calculate_rotation_matrices(coordinates_inital_predictions)

        # save the rough landmarks in the original mesh orientation 
        csv_file = []
        csv_file.append(['Right_exocanthion', coordinates_inital_predictions[0,0], coordinates_inital_predictions[0,1], coordinates_inital_predictions[0,2]])
        csv_file.append(['Left_exocanthion', coordinates_inital_predictions[1,0], coordinates_inital_predictions[1,1], coordinates_inital_predictions[1,2]])
        csv_file.append(['Right_endocanthion', coordinates_inital_predictions[2,0], coordinates_inital_predictions[2,1], coordinates_inital_predictions[2,2]])
        csv_file.append(['Left_endocanthion', coordinates_inital_predictions[3,0], coordinates_inital_predictions[3,1], coordinates_inital_predictions[3,2]])
        csv_file.append(['Nasion', coordinates_inital_predictions[4,0], coordinates_inital_predictions[4,1], coordinates_inital_predictions[4,2]])
        csv_file.append(['Nose_tip', coordinates_inital_predictions[5,0], coordinates_inital_predictions[5,1], coordinates_inital_predictions[5,2]])
        csv_file.append(['Right_alare', coordinates_inital_predictions[6,0], coordinates_inital_predictions[6,1], coordinates_inital_predictions[6,2]])
        csv_file.append(['Left_alare', coordinates_inital_predictions[7,0], coordinates_inital_predictions[7,1], coordinates_inital_predictions[7,2]])
        csv_file.append(['Right_cheilion', coordinates_inital_predictions[8,0], coordinates_inital_predictions[8,1], coordinates_inital_predictions[8,2]])
        csv_file.append(['Left_cheilion', coordinates_inital_predictions[9,0], coordinates_inital_predictions[9,1], coordinates_inital_predictions[9,2]])
        pd.DataFrame(csv_file).to_csv(os.path.join(output_folder, scan_file[:-4] + '_rough_predictions_original.csv'), sep=',', header=False, index=False)

        if args.export_realigned_mesh:
            # realign  mesh 
            ms = pymeshlab.MeshSet()
            ms.load_new_mesh(os.path.join(folder_path, scan_file))
            ms.compute_matrix_from_translation(axisx = -translation[0], axisy = -translation[1], axisz = -translation[2])
            ms.set_matrix(transformmatrix = rot_m1)
            ms.set_matrix(transformmatrix = rot_m2)
            ms.save_current_mesh(os.path.join(output_folder, scan_file[:-4] + '_rough_realigned_mesh.obj'))
            ms.clear()
        
            # save the realigned landmarks 
            csv_file = []
            csv_file.append(['Right_exocanthion', aligned_coordinates[0,0], aligned_coordinates[0,1], aligned_coordinates[0,2]])
            csv_file.append(['Left_exocanthion', aligned_coordinates[1,0], aligned_coordinates[1,1], aligned_coordinates[1,2]])
            csv_file.append(['Right_endocanthion', aligned_coordinates[2,0], aligned_coordinates[2,1], aligned_coordinates[2,2]])
            csv_file.append(['Left_endocanthion', aligned_coordinates[3,0], aligned_coordinates[3,1], aligned_coordinates[3,2]])
            csv_file.append(['Nasion', aligned_coordinates[4,0], aligned_coordinates[4,1], aligned_coordinates[4,2]])
            csv_file.append(['Nose_tip', aligned_coordinates[5,0], aligned_coordinates[5,1], aligned_coordinates[5,2]])
            csv_file.append(['Right_alare', aligned_coordinates[6,0], aligned_coordinates[6,1], aligned_coordinates[6,2]])
            csv_file.append(['Left_alare', aligned_coordinates[7,0], aligned_coordinates[7,1], aligned_coordinates[7,2]])
            csv_file.append(['Right_cheilion', aligned_coordinates[8,0], aligned_coordinates[8,1], aligned_coordinates[8,2]])
            csv_file.append(['Left_cheilion', aligned_coordinates[9,0], aligned_coordinates[9,1], aligned_coordinates[9,2]])
            pd.DataFrame(csv_file).to_csv(os.path.join(output_folder, scan_file[:-4] + '_rough_predictions_realigned.csv'), sep=',', header=False, index=False)
        
    
    