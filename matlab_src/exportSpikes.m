% define a function that uses an extraction
% protocol to save axion.spk files into 
% matlab.mat files
function exportSpikes(path_to_spk, path_to_mat)
    data = extractSpikes(path_to_spk);
    save(path_to_mat, "data")
end

% define a function that loops over the information
% contained in .spk file and puts it in a friendly format
function spikeArray = extractSpikes(path_to_spk)
    % load the .spk
    filedata = AxisFile(path_to_spk).SpikeData.LoadData;
    % record the array dimensions
    elec_spec = size(filedata)
    
    % loop over wells and electrodes (and put them in a sensical order)
    for wr = 1:elec_spec(1)
        for wc = 1:elec_spec(2)
            for ec = 1:elec_spec(4)
                for er = 1:elec_spec(3)
                    % record num of signals on electrode
                    num_waves = size(filedata{wr,wc,ec,er});
                    % if there is at least one,
                    if num_waves(2) > 0
                        % use dimensions I happen to know to order the
                        % data
                        spikes = zeros(num_waves(2),2,38);
                        for wave = 1:num_waves(2)
                            spikes(wave, 1, :) = filedata{wr,wc,ec,er}(wave).GetTimeVector;
                            spikes(wave, 2, :) = filedata{wr,wc,ec,er}(wave).GetVoltageVector;
                        end
                        spikeArray{wr,wc,er,ec} = spikes;
                    end
                end
            end
        end 
    end
end