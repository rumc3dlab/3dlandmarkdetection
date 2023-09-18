import numpy as np
import open3d as o3d
from sympy import Plane, Point3D

class predictions_to_coordinates():
    def determine_coordinates(verts, pred):
        indices_exocanthions = np.squeeze(np.where(pred[0,:] > 0)) # determine the vertex numbers of the vertices that were predicted as belonging to the exocanthions
        indices_endocanthions = np.squeeze(np.where(pred[1,:] > 0)) # determine the vertex numbers of the vertices that were predicted as belonging to the endocanthions
        indices_nasion = np.squeeze(np.where(pred[2,:] > 0)) # determine the vertex numbers of the vertices that were predicted as belonging to the nasion
        indices_nose_tip = np.squeeze(np.where(pred[3,:] > 0)) # determine the vertex numbers of the vertices that were predicted as belonging to the nose tip
        indices_alares = np.squeeze(np.where(pred[4,:] > 0)) # determine the vertex numbers of the vertices that were predicted as belonging to the alares
        indices_cheilons = np.squeeze(np.where(pred[5,:] > 0)) # determine the vertex numbers of the vertices that were predicted as belonging to the cheilons
        
        vertices_exocanthions = verts[indices_exocanthions,:] # vertex coordinates of the exocanthion predictions
        vertices_endocanthions = verts[indices_endocanthions,:] # vertex coordinates of the endocanthion predictions
        vertices_nasion = verts[indices_nasion,:] # vertex coordinates of the nasion predictions
        vertices_nose_tip = verts[indices_nose_tip,:] # vertex coordinates of the nose tip predictions
        vertices_alares = verts[indices_alares,:] # vertex coordinates of the alares predictions
        vertices_cheilons = verts[indices_cheilons,:] # vertex coordinates of the cheilons predictions
        
        # -- exocanthions --
        # since both exocanthions are predicted at once, an clustering algorithm is used to distinguish the two biggest clusters (which removes outliers in the process)
        pcd = []
        pcd = o3d.geometry.PointCloud()
        pcd.points = o3d.utility.Vector3dVector(vertices_exocanthions) 
        
        # split clusters in L and R exocanthions. The variable 'eps' defines the cluster density which the DBSCAN algorithm uses to find clusters. 
        # If the density value is choosen too high, no clusters (with that density) might be found, whereas if the density value is too low, 
        # the entire point cloud might be recognized as one cluster instead of a cluster around the R and the L exocanthions. 
        # Therefore, a for loop is used that iterates through different density settings until 2 clusters are found by the algorithm (the L and R exocanthions).
        for i in range(10):
            a = [5, 4, 3, 2, 1, 6, 7, 8, 9, 10][i]
            exocanthions_labels = np.array(pcd.cluster_dbscan(eps=a, min_points=5)) 
            exocanthions_label1 = np.where(exocanthions_labels == 0)
            exocanthions_label2 = np.where(exocanthions_labels == 1)
            if np.array(exocanthions_label1).size > 0 and np.array(exocanthions_label2).size > 0:
                break
            
        # determine the vertices that belong to each cluster
        vertices_exocanthion1 = vertices_exocanthions[exocanthions_label1,:]
        vertices_exocanthion2 = vertices_exocanthions[exocanthions_label2,:]
            
        # determine the weighted mean vertex location of each cluster
        activations_exocanthion1 = pred[0,:][indices_exocanthions[exocanthions_label1]] 
        activations_exocanthion1 = 10 ** activations_exocanthion1
        exocanthion1_mean_vertex = np.sum(np.squeeze([activations_exocanthion1, activations_exocanthion1, activations_exocanthion1]).T * np.squeeze(vertices_exocanthion1), axis=0)/np.sum(activations_exocanthion1)
        
        activations_exocanthion2 =  pred[0,:][indices_exocanthions[exocanthions_label2]] 
        activations_exocanthion2 = 10 ** activations_exocanthion2
        exocanthion2_mean_vertex = np.sum(np.squeeze([activations_exocanthion2, activations_exocanthion2, activations_exocanthion2]).T * np.squeeze(vertices_exocanthion2), axis=0)/np.sum(activations_exocanthion2)
        
        # -- endocanthions --
        # since both exocanthions are predicted at once, an clustering algorithm is used to distinguish the two biggest clusters (which removes outliers in the process)
        pcd = []
        pcd = o3d.geometry.PointCloud()
        pcd.points = o3d.utility.Vector3dVector(vertices_endocanthions)

        # split clusters L en R endocanthions as was done for the exocanthions
        for i in range(10):
            a = [5, 4, 3, 2, 1, 6, 7, 8, 9, 10][i]
            endocanthions_labels = np.array(pcd.cluster_dbscan(eps=a, min_points=5)) 
            endocanthions_label1 = np.where(endocanthions_labels == 0)
            endocanthions_label2 = np.where(endocanthions_labels == 1)
            if np.array(endocanthions_label1).size > 0 and np.array(endocanthions_label2).size > 0:
                break

        # determine the vertices that belong to each cluster
        vertices_endocanthion1 = vertices_endocanthions[endocanthions_label1,:]
        vertices_endocanthion2 = vertices_endocanthions[endocanthions_label2,:]    
        
        # determine the weighted mean vertex location of each cluster
        activations_endocanthion1 = pred[1,:][indices_endocanthions[endocanthions_label1]] 
        activations_endocanthion1 = 10 ** activations_endocanthion1
        endocanthion1_mean_vertex = np.sum(np.squeeze([activations_endocanthion1, activations_endocanthion1, activations_endocanthion1]).T * np.squeeze(vertices_endocanthion1), axis=0)/np.sum(activations_endocanthion1)
        
        activations_endocanthion2 =  pred[1,:][indices_endocanthions[endocanthions_label2]] 
        activations_endocanthion2 = 10 ** activations_endocanthion2
        endocanthion2_mean_vertex = np.sum(np.squeeze([activations_endocanthion2, activations_endocanthion2, activations_endocanthion2]).T * np.squeeze(vertices_endocanthion2), axis=0)/np.sum(activations_endocanthion2)

        # -- alares --
        # split clusters L en R alares as was done for the exocanthions
        pcd = []
        pcd = o3d.geometry.PointCloud()
        pcd.points = o3d.utility.Vector3dVector(vertices_alares)
        for i in range(11):
            a = [5, 4, 3, 2, 1, 6, 7, 8, 9, 10, 5][i]
            alare_labels = np.array(pcd.cluster_dbscan(eps=a, min_points=10))
            alare_label1 = np.where(alare_labels.copy() == 0)
            alare_label2 = np.where(alare_labels == 1)
            if np.array(alare_label1).size > 0 and np.array(alare_label2).size > 0:
                break
        
        # determine the vertices that belong to each cluster
        vertices_alare1 = vertices_alares[alare_label1,:]
        vertices_alare2 = vertices_alares[alare_label2,:]
            
        # determine the weighted mean vertex location of each cluster    
        activations_alare1 =  pred[3,:][indices_alares[alare_label1]] 
        activations_alare1 = 10 ** activations_alare1
        alare1_mean_vertex = np.sum(np.squeeze([activations_alare1, activations_alare1, activations_alare1]).T * np.squeeze(vertices_alare1), axis=0)/np.sum(activations_alare1)
        
        activations_alare2 = pred[3,:][indices_alares[alare_label2]] 
        activations_alare2 = 10 ** activations_alare2
        alare2_mean_vertex = np.sum(np.squeeze([activations_alare2, activations_alare2, activations_alare2]).T * np.squeeze(vertices_alare2), axis=0)/np.sum(activations_alare2)


        # -- cheilons --
        # split clusters L en R cheilons as was done for the exocanthions
        pcd = []
        pcd = o3d.geometry.PointCloud()
        pcd.points = o3d.utility.Vector3dVector(vertices_cheilons)
        for i in range(11):
            a = [5, 4, 3, 2, 1, 6, 7, 8, 9, 10, 5][i]
            cheilon_labels = np.array(pcd.cluster_dbscan(eps=a, min_points=5))
            cheilon_label1 = np.where(cheilon_labels.copy() == 0)
            cheilon_label2 = np.where(cheilon_labels == 1)
            if np.array(cheilon_label1).size > 0 and np.array(cheilon_label2).size > 0:
                break
        
        # determine the vertices that belong to each cluster
        vertices_cheilon1 = vertices_cheilons[cheilon_label1,:]
        vertices_cheilon2 = vertices_cheilons[cheilon_label2,:]
            
        # determine the weighted mean vertex location of each cluster    
        activations_cheilon1 =  pred[5,:][indices_cheilons[cheilon_label1]] 
        activations_cheilon1 = 10 ** activations_cheilon1
        cheilon1_mean_vertex = np.sum(np.squeeze([activations_cheilon1, activations_cheilon1, activations_cheilon1]).T * np.squeeze(vertices_cheilon1), axis=0)/np.sum(activations_cheilon1)
        
        activations_cheilon2 = pred[5,:][indices_cheilons[cheilon_label2]] 
        activations_cheilon2 = 10 ** activations_cheilon2
        cheilon2_mean_vertex = np.sum(np.squeeze([activations_cheilon2, activations_cheilon2, activations_cheilon2]).T * np.squeeze(vertices_cheilon2), axis=0)/np.sum(activations_cheilon2)
        
        # determine the cheilon midpoint by computing the point between the L and R cheilons
        middle_cheilons = np.mean([cheilon1_mean_vertex, cheilon2_mean_vertex], 0)
        
        
        # -- nasion --
        # remove outliers predictions nasion
        pcd = []; cl = []
        pcd = o3d.geometry.PointCloud()
        pcd.points = o3d.utility.Vector3dVector(vertices_nasion)
        
        # outliers are removed if at least 15 vertices are predicted as belonging to the nasion
        if np.asarray(vertices_nasion).size > 45:
            cl, ind = pcd.remove_statistical_outlier(nb_neighbors=15,
                                                        std_ratio=0.2)
            vertices_nasion1 = np.asarray(cl.points)
            
            activations_nasion = pred[2,:][indices_nasion[ind]] # determine the heighest activation vertex after outlier removal
            activations_nasion = 10 ** activations_nasion
            nasion_mean_vertex = np.sum(np.squeeze([activations_nasion, activations_nasion, activations_nasion]).T * np.squeeze(vertices_nasion1), axis=0)/np.sum(activations_nasion) # determine the weighted mean vertex location
        else:
            # if no vertices are predicted as belonging to the nasion, the vertex with the highest activations is used as the weighted mean predicted nasion location
            if np.asarray(vertices_nasion).size == 0:
                nasion_mean_vertex = np.squeeze(verts[pred[2,:].argmax(),:])
            # if more than 0, but less than 15 vertices are predicted as belonging to the nasion the outlier removal is not used since otherwise too few vertices remain for the outlier removal algorithm to work
            else: 
                activations_nasion = pred[2,:][indices_nasion] 
                activations_nasion = 10 ** activations_nasion
                nasion_mean_vertex = np.sum(np.squeeze([activations_nasion, activations_nasion, activations_nasion]).T * np.squeeze(vertices_nasion), axis=0)/np.sum(activations_nasion)
        
        
        # -- nose tip --
        # remove outliers predictions nose tip
        pcd = []; cl = []
        pcd = o3d.geometry.PointCloud()
        pcd.points = o3d.utility.Vector3dVector(vertices_nose_tip)
        
        # outliers are removed if at least 15 vertices are predicted as belonging to the nose tip
        if np.asarray(vertices_nose_tip).size > 45:
            cl, ind = pcd.remove_statistical_outlier(nb_neighbors=15,
                                                        std_ratio=0.2)
            vertices_nose_tip1 = np.asarray(cl.points)
            
            activations_nose_tip = pred[3,:][indices_nose_tip[ind]] 
            activations_nose_tip = 10 ** activations_nose_tip
            nose_tip_mean_vertex = np.sum(np.squeeze([activations_nose_tip, activations_nose_tip, activations_nose_tip]).T * np.squeeze(vertices_nose_tip1), axis=0)/np.sum(activations_nose_tip)
        else:
            # if no vertices are predicted as belonging to the nasion, the vertex with the highest activations is used as the predicted nasion location
            if np.asarray(vertices_nose_tip).size == 0:
                nose_tip_mean_vertex = np.squeeze(verts[pred[3,:].argmax(),:])
                # if more than 0, but less than 15 vertices are predicted as belonging to the nose tip the outlier removal is not used since otherwise too few vertices remain for the outlier removal algorithm to work
            else: 
                activations_nose_tip = pred[3,:][indices_nose_tip] 
                activations_nose_tip = 10 ** activations_nose_tip
                nose_tip_mean_vertex = np.sum(np.squeeze([activations_nose_tip, activations_nose_tip, activations_nose_tip]).T * np.squeeze(vertices_nose_tip), axis=0)/np.sum(activations_nose_tip)
            

        # determine which symmetrical landmark is right and which is left (for cheilons and exocanthions) by using the plane equation
        plane = Plane(Point3D(nasion_mean_vertex), Point3D(nose_tip_mean_vertex), Point3D(middle_cheilons)) # creates a plane going through the nasion, nose tip and cheilon midpoint
        
        if plane.equation(exocanthion1_mean_vertex[0], exocanthion1_mean_vertex[1], exocanthion1_mean_vertex[2]) < 0:
            exocanthion_mean_right = exocanthion1_mean_vertex
            exocanthion_mean_left = exocanthion2_mean_vertex  
        else: 
            exocanthion_mean_right = exocanthion2_mean_vertex
            exocanthion_mean_left = exocanthion1_mean_vertex
        
        if plane.equation(endocanthion1_mean_vertex[0], endocanthion1_mean_vertex[1], endocanthion1_mean_vertex[2]) < 0:
            endocanthion_mean_right = endocanthion1_mean_vertex
            endocanthion_mean_left = endocanthion2_mean_vertex  
        else: 
            endocanthion_mean_right = endocanthion2_mean_vertex
            endocanthion_mean_left = endocanthion1_mean_vertex

        if plane.equation(alare1_mean_vertex[0], alare1_mean_vertex[1], alare1_mean_vertex[2]) < 0:
            alare_mean_right = alare1_mean_vertex
            alare_mean_left = alare2_mean_vertex  
        else: 
            alare_mean_right = alare2_mean_vertex
            alare_mean_left = alare1_mean_vertex

        if plane.equation(cheilon1_mean_vertex[0], cheilon1_mean_vertex[1], cheilon1_mean_vertex[2]) < 0:
            cheilon_mean_right = cheilon1_mean_vertex
            cheilon_mean_left = cheilon2_mean_vertex  
        else: 
            cheilon_mean_right = cheilon2_mean_vertex
            cheilon_mean_left = cheilon1_mean_vertex

        coordinates_predictions = np.array([exocanthion_mean_right, exocanthion_mean_left, endocanthion_mean_right, endocanthion_mean_left, nasion_mean_vertex, nose_tip_mean_vertex, alare_mean_right, alare_mean_left, cheilon_mean_right, cheilon_mean_left])
        return coordinates_predictions