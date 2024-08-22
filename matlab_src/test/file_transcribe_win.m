% add the path to the open source Axion tools
addpath("c:\/d %userprofile%\Desktop\openAxios\matlab src\AxionFileLoader\AxionFileLoader")
% add the path to the current directory so 
% functions defined there are available
addpath("c:\/d %userprofile%\Desktop\openAxios\matlab src\")

% define a list of axion spk files
% they must be in the 'spks' folder
spk_files = dir('./spks/*.spk')

% iterate over the spk files
for file = spk_files'
    % generate path strings to the spk and the file
    % to be generated for processing with Python
    path_to_spk = strcat('spks\',file.name)
    path_to_mat = strcat('mats\',replace(file.name, '.spk','.mat'))
    % send that data out
    exportSpikes(path_to_spk,path_to_mat)
end
