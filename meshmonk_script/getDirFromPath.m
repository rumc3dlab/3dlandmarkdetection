function [dirName, fileName] = getDirFromPath(path, SEP)
    slashpos = strfind(path,SEP);
    dirName = path(1:slashpos(end));
    fileName = path(slashpos(end)+1:end);
end