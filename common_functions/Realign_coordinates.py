import numpy as np

class determine_alignment():

    def calculate_rotation_matrices(coordinates_predictions):
        
        def rotation_matrix_from_vectors(vec1, vec2):
            a, b = (vec1 / np.linalg.norm(vec1)).reshape(3), (vec2 / np.linalg.norm(vec2)).reshape(3)
            v = np.cross(a, b)
            c = np.dot(a, b)
            s = np.linalg.norm(v)
            kmat = np.array([[0, -v[2], v[1]], [v[2], 0, -v[0]], [-v[1], v[0], 0]])
            rotation_matrix = np.eye(3) + kmat + kmat.dot(kmat) * ((1 - c) / (s ** 2))   
            return rotation_matrix     
        

        translation = coordinates_predictions[4,:]

        landmarks_x = coordinates_predictions.copy()[:,0] - coordinates_predictions[4,0]
        landmarks_y = coordinates_predictions.copy()[:,1] - coordinates_predictions[4,1]
        landmarks_z = coordinates_predictions.copy()[:,2] - coordinates_predictions[4,2]
        coordinates_predictions2 = np.asarray([landmarks_x,landmarks_y, landmarks_z]).T

        middle_cheilions = np.mean([coordinates_predictions2[8,:],coordinates_predictions2[9,:]],axis=0)

        # Align OBJ Z-axis with aortic_valve -> apex
        R_Z = rotation_matrix_from_vectors(np.array([coordinates_predictions2[4,0] - middle_cheilions[0], coordinates_predictions2[4,1] - middle_cheilions[1], coordinates_predictions2[4,2] - middle_cheilions[2]]), np.array([0, 0, 1]))
        R_Z2 = np.zeros([4,4])
        R_Z2[:3,:3] = R_Z
        R_Z2[3,3] = 1

        coordinates_predictions3 = np.dot(coordinates_predictions2, R_Z.T)
    
        # Align OBJ x-axis with aortic_valve -> mitral_valve
        R_X = rotation_matrix_from_vectors(np.array([coordinates_predictions3[1,0] - coordinates_predictions3[0,0], coordinates_predictions3[1,1] - coordinates_predictions3[0,1], coordinates_predictions3[1,2] - coordinates_predictions3[0,2]]), np.array([1, 0, 0]))
        R_X2 = np.zeros([4,4])
        R_X2[:3,:3] = R_X
        R_X2[3,3] = 1
        
        realigned_predictions = np.dot(coordinates_predictions3, R_X.T)

        return realigned_predictions, translation, R_Z2, R_X2