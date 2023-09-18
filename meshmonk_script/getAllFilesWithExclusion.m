function fileList = getAllFilesWithExclusion(dirName, fileExtension, SEP, exclusion, appendFullPath)

  % If fileExtension contains additional path info like 'output/*.txt',
  % separate it from the actual extension
  additionalPath = '';
  slashIdx = strfind(fileExtension, SEP);
  if ~isempty(slashIdx)
    additionalPath = fileExtension(1:slashIdx(end));
    fileExtension = fileExtension(slashIdx(end)+1:end);
  end

  % Generate the full search path
  fullSearchPath = fullfile(dirName, additionalPath, fileExtension);
  
  dirData = dir(fullSearchPath);  % Get the data for the current directory
  dirWithSubFolders = dir(dirName);
  dirIndex = [dirWithSubFolders.isdir];  % Find the index for directories
  fileList = {dirData.name}';  % Get a list of the files
  
  if ~isempty(fileList)
    if appendFullPath
      fileList = cellfun(@(x) fullfile(dirName, additionalPath, x),...  % Prepend path to files
                         fileList,'UniformOutput',false);
    end
  end
  subDirs = {dirWithSubFolders(dirIndex).name};  % Get a list of the subdirectories
  validIndex = ~ismember(subDirs,{'.','..'});  % Find index of subdirectories
                                               % that are not '.' or '..'
  
  exclusionMask = cellfun(@(x) ~isempty(strfind(x, exclusion)), fileList);
  fileList = fileList(~exclusionMask);
  
  exclusionMaskTemplate = cellfun(@(x) ~isempty(strfind(x, 'Template.obj')), fileList);
  fileList = fileList(~exclusionMaskTemplate);
  
end
