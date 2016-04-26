%% Import data from text file.
% Script for importing data from the following text file:
%
%    /Users/pratikprakash/Documents/MATLAB/train-position-data-benson.txt
%
% To extend the code to different selected data or a different text file,
% generate a function instead of a script.

% Auto-generated by MATLAB on 2016/04/25 19:56:32

%% Initialize variables.
filename = '/Users/pratikprakash/Documents/MATLAB/train-position-data-benson.txt';
delimiter = ',';
startRow = 2;

%% Read columns of data as strings:
% For more information, see the TEXTSCAN documentation.
formatSpec = '%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%[^\n\r]';

%% Open the text file.
fileID = fopen(filename,'r');

%% Read columns of data according to format string.
% This call is based on the structure of the file used to generate this
% code. If an error occurs for a different file, try regenerating the code
% from the Import Tool.
dataArray = textscan(fileID, formatSpec, 'Delimiter', delimiter, 'HeaderLines' ,startRow-1, 'ReturnOnError', false);

%% Close the text file.
fclose(fileID);

%% Convert the contents of columns containing numeric strings to numbers.
% Replace non-numeric strings with NaN.
raw = repmat({''},length(dataArray{1}),length(dataArray)-1);
for col=1:length(dataArray)-1
    raw(1:length(dataArray{col}),col) = dataArray{col};
end
numericData = NaN(size(dataArray{1},1),size(dataArray,2));

for col=[2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21]
    % Converts strings in the input cell array to numbers. Replaced non-numeric
    % strings with NaN.
    rawData = dataArray{col};
    for row=1:size(rawData, 1);
        % Create a regular expression to detect and remove non-numeric prefixes and
        % suffixes.
        regexstr = '(?<prefix>.*?)(?<numbers>([-]*(\d+[\,]*)+[\.]{0,1}\d*[eEdD]{0,1}[-+]*\d*[i]{0,1})|([-]*(\d+[\,]*)*[\.]{1,1}\d+[eEdD]{0,1}[-+]*\d*[i]{0,1}))(?<suffix>.*)';
        try
            result = regexp(rawData{row}, regexstr, 'names');
            numbers = result.numbers;
            
            % Detected commas in non-thousand locations.
            invalidThousandsSeparator = false;
            if any(numbers==',');
                thousandsRegExp = '^\d+?(\,\d{3})*\.{0,1}\d*$';
                if isempty(regexp(thousandsRegExp, ',', 'once'));
                    numbers = NaN;
                    invalidThousandsSeparator = true;
                end
            end
            % Convert numeric strings to numbers.
            if ~invalidThousandsSeparator;
                numbers = textscan(strrep(numbers, ',', ''), '%f');
                numericData(row, col) = numbers{1};
                raw{row, col} = numbers{1};
            end
        catch me
        end
    end
end


%% Split data into numeric and cell columns.
rawNumericColumns = raw(:, [2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21]);
rawCellColumns = raw(:, 1);


%% Allocate imported array to column variable names

position = rawCellColumns(:, 1);
accelx = cell2mat(rawNumericColumns(:, 1));
accely = cell2mat(rawNumericColumns(:, 2));
accelz = cell2mat(rawNumericColumns(:, 3));

micro = cell2mat(rawNumericColumns(:, 8));
vel1 = cell2mat(rawNumericColumns(:, 9));
vel2 = cell2mat(rawNumericColumns(:, 10));
vel3 = cell2mat(rawNumericColumns(:, 11));
vel4 = cell2mat(rawNumericColumns(:, 12));
vel5 = cell2mat(rawNumericColumns(:, 13));
vel6 = cell2mat(rawNumericColumns(:, 14));
vel7 = cell2mat(rawNumericColumns(:, 15));
vel8 = cell2mat(rawNumericColumns(:, 16));
vel9 = cell2mat(rawNumericColumns(:, 17));
vel10 = cell2mat(rawNumericColumns(:, 18));
vel11 = cell2mat(rawNumericColumns(:, 19));
vel12 = cell2mat(rawNumericColumns(:, 20));

colLength = length(vel12);
index = (1:colLength)';

%% Clear temporary variables
clearvars filename delimiter startRow formatSpec fileID dataArray ans raw col numericData rawData row regexstr result numbers invalidThousandsSeparator thousandsRegExp me rawNumericColumns rawCellColumns;


%% Plot scatterplot of Accel and Micro
figure
subplot(4, 1, 1)
gscatter(index, accelx, position);
title('Accel x-axis')

subplot(4, 1, 2)
gscatter(index, accely, position);
title('Accel y-axis')

subplot(4, 1, 3)
gscatter(index, accelz, position);
title('Accel z-axis')

subplot(4, 1, 4)
gscatter(index, micro, position);
title('Microphone')

%% Plot scatterplot of velostats
figure
subplot(4, 3, 1)
gscatter(index, vel1, position);
title('Velostat 1')

subplot(4, 3, 2)
gscatter(index, vel2, position);
title('Velostat 2')

subplot(4, 3, 3)
gscatter(index, vel3, position);
title('Velostat 3')

subplot(4, 3, 4)
gscatter(index, vel4, position);
title('Velostat 4')

% Second four
subplot(4, 3, 5)
gscatter(index, vel5, position);
title('Velostat 5')

subplot(4, 3, 6)
gscatter(index, vel6, position);
title('Velostat 6')

subplot(4, 3, 7)
gscatter(index, vel7, position);
title('Velostat 7')

subplot(4, 3, 8)
gscatter(index, vel8, position);
title('Velostat 8')

% third four
subplot(4, 3, 9)
gscatter(index, vel9, position);
title('Velostat 9')

subplot(4, 3, 10)
gscatter(index, vel10, position);
title('Velostat 10')

subplot(4, 3, 11)
gscatter(index, vel11, position);
title('Velostat 11')

subplot(4, 3, 12)
gscatter(index, vel12, position);
title('Velostat 12')