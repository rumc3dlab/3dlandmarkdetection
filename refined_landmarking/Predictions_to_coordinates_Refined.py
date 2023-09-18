import numpy as np
import open3d as o3d
from sympy import Plane, Point3D

class predictions_to_coordinates():
    def determine_coordinates(verts, pred):
        coordinates_predictions = np.zeros([10,3])
            
        for i in range(pred.shape[0]):
            indcs_highest_activations = np.where(pred[i,:] > 0)
            activations = pred[i,indcs_highest_activations]
            activations = 10 ** activations
            vertices = np.squeeze(verts[indcs_highest_activations,:])
            
            if vertices.size > 60:
                pcd = []
                pcd = o3d.geometry.PointCloud()
                pcd.points = o3d.utility.Vector3dVector(np.asarray(vertices))
                
                cl, ind = pcd.remove_statistical_outlier(nb_neighbors=15,
                                                            std_ratio=2.0)
                coords_pred_without_outliers = np.array(np.asarray(cl.points))

                if np.array(coords_pred_without_outliers).size == 0:
                    coords_pred_without_outliers = vertices
                if np.array(coords_pred_without_outliers).size == 0:
                    coords_mean_vertex_pred = verts[pred[i,:].argmax(),:]
                else:
                    activations2 = np.squeeze(activations)[ind]
                    coords_mean_vertex_pred = np.sum((np.asarray(np.squeeze([activations2, activations2, activations2])).T * coords_pred_without_outliers),axis=0) / np.sum(activations2)
                
            else: 
                if np.array(vertices).size > 3:
                    coords_mean_vertex_pred = np.sum((np.asarray(np.squeeze([activations, activations, activations])).T * vertices),axis=0) / np.sum(activations)
                else:
                    coords_mean_vertex_pred = verts[pred[i,:].argmax(),:]
            coordinates_predictions[i,:] = coords_mean_vertex_pred
        return coordinates_predictions