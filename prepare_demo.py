import shutil
import os

demo_folder = ['meshmonk', 'demo']
demo_files = ['demoFace.obj',
              'demoFace.mat',
              'demoFace.mtl',
              'demoFace.png',
              'DemoFaceLandmarks.csv',
              'TemplateLandmarks.csv',
              'Template.obj',
              'Template.mat']

for file in demo_files:
    demo_file = os.path.join(demo_folder[0],demo_folder[1],file)
    if not os.path.exists(demo_file):
        raise Exception("Can't find the Meshmonk Demo file: {}. Check the readme!".format(demo_file)) 
    
target_folder = os.path.join('demo','demo')

if not os.path.exists('demo'):
    os.mkdir('demo')

if not os.path.exists(target_folder):
    os.mkdir(target_folder)

for file in demo_files:
    demo_file = os.path.join(demo_folder[0],demo_folder[1],file)
    demo_target_file = os.path.join(target_folder,file)
    shutil.copyfile(demo_file, demo_target_file)

print("Demo files copied succesfully!")