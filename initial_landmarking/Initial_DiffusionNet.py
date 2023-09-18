import numpy as np
import torch
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), "../diffusion-net/src/"))  # add the path to the DiffusionNet src
import diffusion_net


class Predictions_Initial_DiffusionNet():
      
    def Predict(verts, faces, normals):
        verts = torch.tensor(np.ascontiguousarray(verts)).float()
        faces = torch.tensor(np.ascontiguousarray(faces)).long()
        normals = torch.tensor(np.ascontiguousarray(normals)).float()

        weights_initial_DiffusionNet = os.path.dirname(__file__) + '/../models/Weights_initial_DiffusionNet.pth'

        if torch.cuda.is_available():
            device = torch.device('cuda')
        else:
            device = torch.device('cpu')
    
        # center and unit scale
        verts = diffusion_net.geometry.normalize_positions(verts)

        outputs = diffusion_net.geometry.get_operators(verts, faces, k_eig=128, op_cache_dir=None, normals=normals)
        frames = outputs[0].to(device)
        mass = outputs[1].to(device)
        L = outputs[2].to(device)
        evals = outputs[3].to(device)
        evecs = outputs[4].to(device)
        gradX = outputs[5].to(device)
        gradY = outputs[6].to(device)

        features = diffusion_net.geometry.compute_hks_autoscale(evals, evecs, 16) 

        model = diffusion_net.layers.DiffusionNet(C_in=16,
                                                    C_out=6,
                                                    C_width= 256,
                                                    N_block= 12,
                                                    outputs_at='vertices')
                                                    
        model = model.to(device)

        if torch.cuda.is_available():
            model.load_state_dict(torch.load(weights_initial_DiffusionNet))
        else:
            model.load_state_dict(torch.load(weights_initial_DiffusionNet, map_location=torch.device('cpu')))

        model.eval()

        # Apply the model
        pred_initial_DiffusionNet = model(features, mass, L=L, evals=evals, evecs=evecs, gradX=gradX, gradY=gradY, faces=faces)
        pred_initial_DiffusionNet = np.asarray(pred_initial_DiffusionNet.cpu().detach().numpy())
        return pred_initial_DiffusionNet