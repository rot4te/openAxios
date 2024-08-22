% % This is a testing file to export on of the .spk files to .hdf5
% 
% baseline = AxisFile("~/code/For_Whoredor/spks/HD Neuron Pulsing 09MAY2024_Baseline(000).spk").SpikeData.LoadData;
% % hr1 = AxisFile("~/code/For_Whoredor/spks/HD Neuron Pulsing 09MAY2024_01 Hour(000).spk").SpikeData.LoadData;
% % hr4 = AxisFile("~/code/For_Whoredor/spks/HD Neuron Pulsing 09MAY2024_04 Hours(000).spk").SpikeData.LoadData;
% % hr12 = AxisFile("~/code/For_Whoredor/spks/HD Neuron Pulsing 09MAY2024_12 Hours(000).spk").SpikeData.LoadData;
% % hr24 = AxisFile("~/code/For_Whoredor/spks/HD Neuron Pulsing 09MAY2024_24 Hours(000).spk").SpikeData.LoadData;
% 
% % save("/Users/alexcoxe/code/For_Whoredor/spks/base.mat", "baseline")
% % save("/Users/alexcoxe/code/For_Whoredor/spks/1hr.mat", "hr1")
% % save("/Users/alexcoxe/code/For_Whoredor/spks/4hr.mat", "hr4")
% % save("/Users/alexcoxe/code/For_Whoredor/spks/12hr.mat", "hr12")
% % save("/Users/alexcoxe/code/For_Whoredor/spks/24hr.mat", "hr24")
% 
% 
% % there is a 4 by 6 grid of wells, and each well has a 4 by 4 grid of
% % electrodes. access them individually by 
% % baseline(w_col, w_row, el_row, el_col)
% % but these still contain n-many waveforms. to get the nth wave, access
% % with baseline{w_col, w_row, el_row, el_col}(n).GetSomeValues
% 
% % code should look something like:
% % for wc in wcols
% %   for wr in wrows
% %       for ec in ecols
% %           for er in erows
% %               len = size(baseline{wr, wc, ec, er})
% %               if len(2) > 0
% %                   for wave in len(2)
% %                       timevec = baseline{wr, wc, ec, er}(wave).GetTimeVector
% %                       voltvec = baseline{wr, wc, ec, er}(wave).GetVoltageVector
% 
% 
% for wr = 1:4
%     for wc = 1:6
%         for ec = 1:4
%             for er = 1:4
%                 len = size(baseline{wr,wc,ec,er});
%                 if len(2) > 0
%                     spikes = zeros(len(2),2,38);
%                     for wave = 1:len(2)
%                         spikes(wave,1,:) = baseline{wr,wc,ec,er}(wave).GetTimeVector;
%                         spikes(wave,2,:) = baseline{wr,wc,ec,er}(wave).GetVoltageVector;
%                     end
%                     electrode{wr, wc, er, ec} = spikes
%                 end
%             end
%         end
%     end
% end
% 
% save("/Users/alexcoxe/code/For_Whoredor/spks/base.mat","electrode")
% 
exportSpikes("~/code/For_Whoredor/spks/HD Neuron Pulsing 09MAY2024_01 Hour(000).spk", "one_hour.mat")