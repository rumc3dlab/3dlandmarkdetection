import numpy as np
import pymeshlab
import torch
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), "../../../../src/"))  # add the path to the DiffusionNet src
import diffusion_net
import diffusion_net_cuda as dnc


class Facial_segmentation():
    def segment(folder_path, scan_file, translation, rot_m1, rot_m2, save_segmented_mesh):
        ms = pymeshlab.MeshSet()
        ms.load_new_mesh(os.path.join(folder_path, 'output', scan_file[:-4] + '_original_mm.obj'))
        mesh = ms.current_mesh()
        vertices_mm = torch.from_numpy(mesh.vertex_matrix().astype(np.float32)).to('cuda:0')
        ms.clear()

        ms = pymeshlab.MeshSet()
        
        ms.load_new_mesh(os.path.join(folder_path, scan_file))
        mesh2 = ms.current_mesh()
        original_vertices_np = mesh2.vertex_matrix().astype(np.float32)
        original_vertices_torch = torch.from_numpy(mesh2.vertex_matrix().astype(np.float32)).to('cuda:0')
        faces_orig_torch = torch.from_numpy(mesh2.face_matrix().astype(np.float32)).to('cuda:0')
        faces_orig_np = mesh2.face_matrix()
        normals_orig_np = mesh2.vertex_normal_matrix()

        mapping = dnc.vertices_mapping_close(original_vertices_torch, vertices_mm, 15.0)
        mapping = mapping.to(torch.int8) # Compress for storage

        
        vertices_crop = original_vertices_torch[mapping==1]
        vertex_ids = torch.where(mapping==1)[0].cpu().numpy()

        vertex_map = torch.full((len(original_vertices_torch),),torch.tensor(-1),dtype=torch.long)
        vertex_map[vertex_ids] = torch.arange(len(vertex_ids))

        for i in range(len(original_vertices_np)):
            if i not in vertex_ids:
                original_vertices_np[i,0] = 10000001
        m = pymeshlab.Mesh(original_vertices_np, faces_orig_np, normals_orig_np)
        ms.add_mesh(m, set_as_current = True)
        ms.compute_selection_by_condition_per_vertex(condselect = ('x > 10000'))
        ms.meshing_remove_selected_vertices()

        if save_segmented_mesh == True:
            ms.save_current_mesh(os.path.join(folder_path, 'output', scan_file[:-4] + '_segmented.obj'))

        # Realign the segmented mesh
        ms.compute_matrix_from_translation(axisx = -translation[0], axisy = -translation[1], axisz = -translation[2])
        ms.set_matrix(transformmatrix = rot_m1)
        ms.set_matrix(transformmatrix = rot_m2)

        ms.meshing_remove_duplicate_faces()
        ms.meshing_remove_duplicate_vertices()
        ms.meshing_repair_non_manifold_edges(method = 'Remove Faces')
        ms.meshing_remove_connected_component_by_diameter(mincomponentdiag = pymeshlab.Percentage(5), removeunref = True)
        ms.meshing_close_holes(maxholesize = 100)
        ms.meshing_repair_non_manifold_edges(method = 'Remove Faces')

        mesh_segmentation = ms.current_mesh()
        vertices_segmentation = mesh_segmentation.vertex_matrix().astype(np.float32)
        faces_segmenation = mesh_segmentation.face_matrix()
        normals_segmentation = mesh_segmentation.vertex_normal_matrix()
        
        return vertices_segmentation, faces_segmenation, normals_segmentation

    