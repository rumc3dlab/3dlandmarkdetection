# # 3dlandmarkdetection
This code demonstrates the functionality as shown in:
**Paper url here**

## IMPORTANT: Additional License information
This work is published under the **Apache License Version 2.0**. There are additional conditions for using this model *beyond non-commercial reserach or educational use*. This model has partially been trained using the [HeadSpace Dataset](https://www-users.york.ac.uk/~np7/research/Headspace/). If you would use this work for any other purpose other than non-commercial or educational use, you must request permission at the HeadSpace team (see website).

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
conda install pytorch torchvision torchaudio pytorch-cuda=11.7 -c pytorch -c nvidia
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
