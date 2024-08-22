# spike_info.py
# this script defines functions
# which determine properties of
# spikes from signal data
# Authored by: Alexander Coxe

#####################################################################
import numpy as np
import scipy as sp
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
#####################################################################


def load_spk(path_to_mat):
    """
    Load a .mat file found at path_to_mat
    resulting from matlab processing 
    of a .spk file
    """
    spk_array = sp.io.loadmat(path_to_mat)
    spk_array = spk_array["data"]
    return spk_array

#####################################################################

def get_peaks(volts, time, amp_threshold=0):
    """
    Finds the peaks in a (time, voltage) data set subject to an 
    amplitude threshold and filter out (but save) rebound 
    information
    
    Arguments:
    * volts:          float64 array of voltages
    * time:           float64 array of time signatures (should be same length as volts)
    * amp_threshold:  float64 threshold for what is a spike and what is noise,
                      defaults to 65% of the largest amplitude in the signal

    Return Type: Dict
    Dict Keys:
    * "num_spikes":     integer number of peaks discovered
    * "num_reflect":    integer number of reflections
    * "spike_data":     array of spike dictionaries {"index", "time_signature", "Amplitude"}
    * "reflect_data:
    """
    exm = np.max(np.abs(volts)) # grab the absolute maximum unsigned voltage
    if amp_threshold == 0:
        amp_threshold = 0.65 * exm # set the default amplitude threshold
    
    bad_ix = []
    # generate a list of all peaks which satisfy the threshold
    peak_info = list(sp.signal.find_peaks(np.abs(volts)))
    for i in range(len(peak_info[1]["prominences"])):
        if peak_info[1]["prominences"][i] < amp_threshold:
            bad_ix.append(i)
    peak_info[0] = np.delete(peak_info[0], bad_ix)
    peak_info[1]["prominences"] = np.delete(peak_info[1]["prominences"], bad_ix)
    peak_info[1]["left_bases"] = np.delete(peak_info[1]["left_bases"], bad_ix)
    peak_info[1]["right_bases"] = np.delete(peak_info[1]["right_bases"], bad_ix)
    reflections = dict() # initialize array for rebound peaks
    ref_ix = []
    # iterate over all of the peak indices
    if len(peak_info[0]) > 1:
        for i in range(len(peak_info[0])-1):
            # check if adjacent peaks have opposite signs
            if np.sign(volts[peak_info[0][i]]) != np.sign(volts[peak_info[0][i+1]]):
                # if they do, assign the flipped sign peak to a rebound
                reflections["Indices"] = peak_info[0][i+1],
                reflections["Time_signature"]= time[peak_info[0][i+1]],
                reflections["Ampltiude"]= peak_info[1]["prominences"][i+1]

                ref_ix.append(i+1)
                i = i+1
        # remove the reflection information from the list of peaks
        peak_info[0] = np.delete(peak_info[0], ref_ix)
        peak_info[1]["prominences"] = np.delete(peak_info[1]["prominences"], ref_ix)
        peak_info[1]["left_bases"] = np.delete(peak_info[1]["left_bases"], ref_ix)
        peak_info[1]["right_bases"] = np.delete(peak_info[1]["right_bases"], ref_ix)
           
    
    spikes = dict() # initialize list of major spikes
    
    # for peak in range(len(peak_info[0])):
        # store the information in a dictionary and append it to the list
    spikes["Indices"] = peak_info[0]
    spikes["Time_signatures"]= [time[peak_info[0][i]] for i in range(len(peak_info[0]))]
    spikes["Amplitudes"]= peak_info[1]["prominences"]
    
    # generate a dictionary of info about the whole signal
    signal_info = {"num_spikes": len(spikes["Indices"]),
                   "num_reflect": len(reflections),
                   "spike_data": spikes,
                   "reflect_data": reflections}
    
    # return the info about the whole signal
    return signal_info


#####################################################################


def electrode_mean(spk_array, wr, wc, er, ec):
    num_signals = len(spk_array[wr][wc][er][ec])
    if num_signals > 1:
        avg = np.average([spk_array[wr][wc][er][ec][w][1] for w in range(len(spk_array[wr][wc][er][ec]))], axis=0)
        return avg

    

#####################################################################



def plot_electrode(spk_array, wr, wc, er, ec):
    """
    plots every signal on an electrode
    time signatures are flattened so that
    all signals are plotted on the same range
    starting at 0.

    Arguments:
    * spk_array:    array of all the data for all the wells
                    has dimensions (well_rows, well_columns, electrode_rows, electrode_columns)
    * wr:           int specifying the well row
    * wc:           int specifying the well column
    * er:           int specifying the electrode row
    * ec:           int specifying the electrode row
    """

    waves = plt.figure(figsize = (12,8)) # figure backdrop
    waves.suptitle(f"Signals on well ({wr+1},{wc+1}): electrode ({er+1},{ec+1})", fontsize = 20)
    ax = plt.subplot(111)


    # check if there are any signals on the electrode
    if len(spk_array[wr][wc][er][ec]) > 1:
        
        # ax[er*erows+ec].set_xlim([0,xaxis[-1]])
        for wave in range(len(spk_array[wr][wc][er][ec])):
            xaxis = np.linspace(0,
                np.max(spk_array[wr][wc][er][ec][wave][0])-np.min(spk_array[wr][wc][er][ec][wave][0]),
                len(spk_array[wr][wc][er][ec][wave][0]))
            # ymax = np.max(np.abs(spk_array[wr][wc][er][ec][wave][1]))
            
            # flatten the time signature to its length starting at 0
            
            # plot the whole signal against flattened time
            ax.plot(xaxis, spk_array[wr][wc][er][ec][wave][1])

    else: # This handles electrodes with no signal
        ax.text(0.15,0.5,"No signal on this electrode")
    plt.tight_layout(pad=2.)
    plt.show()


def plot_electrode_mean(spk_array, wr, wc, er, ec):
    num_signals = len(spk_array[wr][wc][er][ec])
    if num_signals > 1:
        flat_time = np.linspace(0,
                        np.max(spk_array[wr][wc][er][ec][0][0])-np.min(spk_array[wr][wc][er][ec][0][0]),
                        38)
        avg = electrode_mean(spk_array,wr,wc,er,ec)
        fig = plt.figure(figsize=(12,8))
        fig.suptitle(f"Average signal on well ({wr},{wc}), electrode ({er},{ec})", fontsize = 20)
        ax = plt.subplot(111)
        ax.plot(flat_time, avg, c='black', lw=2)

    else:
        print("No signals to average over")
        return



#####################################################################


def plot_well(spk_array, wr, wc):
    """
    Generate a 4x4 array of plots
    plots every signal on every electrode
    time signatures are flattened so that
    all signals are plotted on the same range
    starting at 0.

    Arguments:
    * spk_array:    array of all the data for all the wells
                    has dimensions (well_rows, well_columns, electrode_rows, electrode_columns)
    * wr:           int specifying the well row
    * wc:           int specifying the well column
    """
    erows = len(spk_array[wr][wc]) # number of rows of electrodes
    ecols = len(spk_array[wr][wc][0]) # number of columns of electrodes

    waves = plt.figure(figsize = (16,14)) # figure backdrop
    waves.suptitle(f"Signals on well ({wr+1},{wc+1})", fontsize = 20)
    ax = [] # array for different subplots

    # double loop over the rectangular array of electrodes
    for er in range(erows):
        for ec in range(ecols):

            # generate subplot for electrode
            ax.append(plt.subplot(erows,ecols,erows*er+ec+1)) 
            # indicate which electrode
            ax[er*erows+ec].set_title(f"Electrode ({er+1},{ec+1})", fontsize=18)
            # check if there are any signals on the electrode
            if len(spk_array[wr][wc][er][ec]) > 1:
                
                # ax[er*erows+ec].set_xlim([0,xaxis[-1]])
                for wave in range(len(spk_array[wr][wc][er][ec])):
                    xaxis = np.linspace(0,
                        np.max(spk_array[wr][wc][er][ec][wave][0])-np.min(spk_array[wr][wc][er][ec][wave][0]),
                        len(spk_array[wr][wc][er][ec][wave][0]))
                    # ymax = np.max(np.abs(spk_array[wr][wc][er][ec][wave][1]))
                    
                    # flatten the time signature to its length starting at 0
                    
                    # plot the whole signal against flattened time
                    ax[er*erows+ec].plot(xaxis, spk_array[wr][wc][er][ec][wave][1])

            else: # This handles electrodes with no signal
                ax[erows*er+ec].text(0.15,0.5,"No signal on this electrode")
    plt.tight_layout(pad=2.)
    plt.show()



#####################################################################


def record_electrode(spk_array, wr, wc, er, ec, amp_threshold = 0):
    """
    Generate array of 'get_peaks' dictionaries corresponding
    to every signal on a particular electrode

    Arguments:
    * spk_array:        array of all the data for all the wells
                        has dimensions (well_rows, well_columns, electrode_rows, electrode_columns)
    * wr:               int specifying the well row
    * wc:               int specifying the well column
    * er:               int specifying the electrode row
    * ec:               int specifying the electrode row
    * amp_threshold:    float64 which determines the amplitude noise cutoff
                        - defaults to zero which is taken to be 65% of the maximum amplitude
    """
    sensor = []
    if len(spk_array[wr][wc][er][ec]) > 1:
        waves = []
        for w in range(len(spk_array[wr][wc][er][ec])):
            waves.append(get_peaks(spk_array[wr][wc][er][ec][w][1],
                            spk_array[wr][wc][er][ec][w][0],
                            amp_threshold=amp_threshold))
            
        for w in range(len(waves)):
            sensor.append(dict())
            k = waves[w]["num_spikes"]
            sensor[w]["Number of peaks"] = k
            amplis = waves[w]["spike_data"]["Amplitudes"]
            sensor[w]["Amplitudes"] = amplis
            times = waves[w]["spike_data"]["Time_signatures"]
            sensor[w]["Time Signatures"] = times
    
    return sensor


#####################################################################


def record_well(spk_array, wr, wc, csvname="", amp_threshold = 0):
    """
    Generate array of 'get_peaks' dictionaries corresponding
    to every signal on every electrode in a well, put it in a 
    dataframe, and save it to a csv

    Arguments:
    * spk_array:        array of all the data for all the wells
                        has dimensions (well_rows, well_columns, electrode_rows, electrode_columns)
    * wr:               int specifying the well row
    * wc:               int specifying the well column
    * er:               int specifying the electrode row
    * ec:               int specifying the electrode row
    * csvname:          string to use as csv filename
    * amp_threshold:    float64 which determines the amplitude noise cutoff
                        - defaults to zero which is taken to be 65% of the maximum amplitude

    Returned object is dict of arrays of dicts, i.e.
    top level keys dictname.keys() are 'electrode (row, col)"
    then each of those keys matches to an array of signals, 
    each index of which gives a dictionary of info about that signal,
    eg well26["electrode (1,3)][4]["Amplitudes"] will give you a list 
    of the amplitudes of the peaks on the fifth signal on the electrode in 
    row 1 columns three of whichever well26 is. They will appear in time 
    order, so if you look at well26["electrode (1,3)][4]["Time signatures"]
    each time will correspond to the amplitude in the same position.
    """
    erows = len(spk_array[wr][wc])
    ecols = len(spk_array[wr][wc][0])
    
    sensors = dict()
    for er in range(erows):
        for ec in range(ecols):

            sensors[f"electrode ({er+1},{ec+1})"] = record_electrode(spk_array,wr,wc,er,ec,amp_threshold=amp_threshold)

            
    return sensors
