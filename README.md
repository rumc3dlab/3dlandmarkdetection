
# 3dlandmarkdetection
This code demonstrates the functionality as shown in:

B. Berends, F. Bielevelt, R. Schreurs, S. Vinayahalingam, T. Maal, and G. de Jong, “Fully automated landmarking and facial segmentation on 3D photographs,” arxiv, 2023.
[arXiv:2309.10472](https://arxiv.org/abs/2309.10472)

Please cite this paper when you use this work (see License).

## IMPORTANT: Additional License information
This work is published under the **Apache License Version 2.0**. There are additional conditions for using this model *beyond non-commercial reserach or educational use*. This model has partially been trained using the [HeadSpace Dataset](https://www-users.york.ac.uk/~np7/research/Headspace/). If you would use this work for any other purpose other than non-commercial or educational use, you must request permission at the HeadSpace team (see website).

# Method overview
![Automated landmarking workflow. Step 1: First instance segmentation task for rough
landmark prediction. Step 2: Realignment of the meshes using the roughly predicted landmarks. Step 3:
Facial region segmentation (white) using MeshMonk (blue wireframe). Step 4: Second instance
segmentation task for refined landmark prediction.](https://github.com/rumc3dlab/3dlandmarkdetection/blob/0df8c6cafa096650387ac51c31b1e8d058b41cdd/media/Figure_1.png)

# Installation
For the installation we have the following template instructions for a python 3.10 instruction.

 1. Install the python environment and requisites
```
conda create -n landmarking python=3.10
conda activate landmarking
```
 2. *(Optional) Some users reported a ClobberError regarding libnpp-dev when installing torch. You can fix this by:* `conda install -c nvidia libnpp-dev`
 3. The following packages need to be installed as following
```
conda install pytorch==2.0.1 torchvision==0.15.2 torchaudio==2.0.2 pytorch-cuda=11.7 -c pytorch -c nvidia
conda install -c anaconda pandas
conda install -c conda-forge scipy
conda install -c anaconda scikit-learn
conda install -c conda-forge tqdm
pip3 install open3d
pip3 install pymeshlab
pip3 install robust-laplacian
pip3 install potpourri3d
```
 4. Clone the repository to a local folder (e.g. `landmarking`)
 5. Clone the following repository `https://github.com/Goblaski/diffusion-net-cuda` [link](https://github.com/Goblaski/diffusion-net-cuda) and put it in the local folder under `diffusion-net`
 6. Navigate to `diffusion-net` and type `python setup.py install`
 7. Clone the following repository `https://gitlab.kuleuven.be/mirc/meshmonk` [link](https://gitlab.kuleuven.be/mirc/meshmonk) and put it in the local folder under  `meshmonk`
 8. Follow the [installation instructions of meshmonk](https://gitlab.kuleuven.be/mirc/meshmonk/-/blob/master/README.md)
You should now be set to run the demo.
## Folder structure
After installation you shoulw have the following folder structure:
```
/Landmarking/common_functions/
/Landmarking/diffusion-net/
/Landmarking/initial_landmarking/
/Landmarking/meshmonk/
/Landmarking/meshmonk_script/
/Landmarking/models/
/Landmarking/refined_landmarking/
```
# Demo
 1. Navigate to the root folder (e.g `landmarking`)
 2. run `python prepare_demo.py`
 3. run `python Initial_landmarking.py`
Optionally you can change `--input folder` and add `--export_realigned_mesh`
4. In Matlab, open `meshmonk_script/MeshMonkFolder.m` and run.
5. run `python Refined_landmarking.py`
Optionally you can change `--input folder` , add `--export_realigned_mesh` , and/or `--save_segmented_mesh`.
