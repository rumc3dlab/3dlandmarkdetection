clear all; close all;

%% SETTINGS

% Change path to your meshmonk installation
path2meshmonk = '..\meshmonk\';

% Directory to perform meshmonk template on
dirName = '..\demo\demo\'; 

% Overwrite 
overwrite = false;

SEP = '\';  % Choose your type of path seperator based on your OS

%% Setup paths
if path2meshmonk(end) ~= SEP
    path2meshmonk = [path2meshmonk SEP];
end

if dirName(end) ~= SEP
    dirName = [dirName SEP];
end

addpath(genpath(path2meshmonk)) % Ensure meshmonk is on your MATLAB path. 

%% Template config
% Change this if you require a different template. We use the one from the
% repository now
templateDir = [path2meshmonk 'demo' SEP];
templateFile = 'Template.obj'; 
templateLMCsv = 'TemplateLandmarks.csv';

%% Get applicable files for MeshMonk

fileExtension = ['output' SEP '*.obj'];
exclusion = '_mm.obj';

fileList = getAllFilesWithExclusion(dirName, fileExtension, SEP, exclusion, true);

%% Meshmonk settings
% See:  - https://www.nature.com/articles/s41598-021-91465-z
%       - https://www.nature.com/articles/s41598-019-42533-y
%       - https://gitlab.kuleuven.be/mirc/meshmonk
%       - https://github.com/harrymatthews50/3DGrowthCurves/

RM= ShapeMapper;
RM.NumIterations = 30;

RM.TransformationType = 'rigid';
RM.UseScaling = true;
RM.CorrespondencesNumNeighbours = 3;
RM.CorrespondencesFlagThreshold = 0.9; 
RM.CorrespondencesSymmetric = true;
RM.CorrespondencesEqualizePushPull = false;
RM.InlierKappa = 4;
RM.InlierUseOrientation = true;
RM.FlagFloatingBoundary = true;
RM.FlagTargetBoundary = true;
RM.FlagTargetBadlySizedTriangles = true;
RM.TriangleSizeZscore = 6;
RM.UpSampleTarget = false;
  
NRM = ShapeMapper;
NRM.TransformationType = 'nonrigid';
NRM.NumIterations = 80; 
NRM.CorrespondencesSymmetric = false;
NRM.CorrespondencesNumNeighbours = 3;
NRM.CorrespondencesFlagThreshold = 0.9;
NRM.CorrespondencesUseOrientation = true;
NRM.CorrespondencesEqualizePushPull = false;
NRM.InlierKappa = 12;
NRM.InlierUseOrientation = true;
NRM.FlagFloatingBoundary = true;
NRM.FlagTargetBoundary = true;
NRM.FlagTargetBadlySizedTriangles = true;
NRM.TriangleSizeZscore = 6;
NRM.UpSampleTarget = false;

NRM.TransformSigma = 3;
NRM.TransformNumViscousIterationsStart = 200;
NRM.TransformNumViscousIterationsEnd = 1;
NRM.TransformNumElasticIterationsStart = 200;
NRM.TransformNumElasticIterationsEnd = 1;
NRM.TransformNumNeighbors = 80;

%% Load template
TemplateRef = shape3D; 
TemplateRef.importWavefront(templateFile, templateDir);
disp("Loading template done!")
%%
h = waitbar(0,'Initializing...');

nFiles = length(fileList);
for i=1:nFiles
    filePercentage = i/nFiles;
    progressString = sprintf('%d/%d',i,nFiles);
    waitbar(filePercentage,h,progressString);

    curFile = fileList{i};
    [curDirName, curFileName] = getDirFromPath(curFile, SEP);
    target_file_split = split(curFile,'.obj');
    target_file = [target_file_split{1} '_mm.obj'];
    
    if overwrite == false && exist(target_file,'file') ~= 0
       continue 
    end
    
    [~, targetFileName] = getDirFromPath(target_file, SEP);
    
    if contains(curFile,'realigned_mesh.obj')
        csvFile = replace(curFile,'realigned_mesh.obj','predictions_realigned.csv');
    else
        csvFile = replace(curFile,'_original.obj','_rough_predictions_original.csv');
    end

    templateLandmarks = readTextLandmarkFile([templateDir templateLMCsv],',',1,3,1,5);
    targetLandmarks = readTextLandmarkFile(csvFile,',',2,4,1,10);

    selLandmarks = [1, 2, 7, 9, 10]; 
    targetLandmarks = targetLandmarks(selLandmarks,:);

    T = computeTransform(templateLandmarks,targetLandmarks,true);
    
    Template = clone(TemplateRef);
    Template = applyTransform(Template,T);
    
    Target = shape3D;
    Target.importWavefront(curFileName,curDirName);

    forRM = clone(RM);
    forRM.FloatingShape = Template;
    forRM.TargetShape = Target;
    forRM.Display = false;
    forRM.map();

    forNRM = clone(NRM);
    forNRM.FloatingShape = clone(forRM.FloatingShape);
    forNRM.TargetShape = Target;
    forNRM.Display = false;
    forNRM.map()

    forNRM.FloatingShape.exportWavefront(targetFileName,curDirName);
end

close(h)

disp("Meshmonk process done!")