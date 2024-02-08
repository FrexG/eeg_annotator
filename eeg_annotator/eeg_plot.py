import mne
import math
import numpy as np
import pandas as pd
from matplotlib.figure import Figure


class EEGPlot:
    def __init__(self):
        self.max_x_lim = 10
        self.scale_factor = 0.0004
        self.y_tick_pos = []

    def set_max_x_lim(self, x_lim: int):
        self.max_x_lim = x_lim

    def create_axes(self, fig, raw_eeg):
        # calculate y_limit from the input raw
        # eeg signal

        pwr = np.abs(raw_eeg.get_data())
        mean_pwr = np.mean(pwr)
        std_pwr = np.std(pwr)
        self.scale_factor = (mean_pwr + std_pwr) * 3
        print(f"{self.scale_factor=}")

        ax = fig.add_subplot(1, 1, 1)
        ax.set_xlim(0, self.max_x_lim)
        ax.set_ylim(-self.scale_factor, 22 * self.scale_factor)

        return ax

    def create_figure(self, n_subplots, figsize): 
        # n_subplots default it to 19 for EEG
        fig = Figure(figsize=figsize, dpi=100)
        axes = self.create_axes(n_subplots, fig)
        return fig, axes

    def get_signal_length_seconds(self, raw_eeg):
        s_freq = raw_eeg.info["sfreq"]
        signal_length = raw_eeg.get_data().shape[-1]

        return signal_length / s_freq
    
    def read_excel(self,excel_path:str,s_freq:int = 256):
        """ Read eeg data stored in excel format, specifically made for imports from `Haleluya Hospital` 
            - this files don't have information about the sampling frequency (so it is assumed)
            - contain patient and other unneeded info.
            - are already stored in `Bipolar montage`, thus no conversion required
            - have fewer channels (17)
            args:
                - excel_path(str): abs path to the excel file
                - s_freq(int): sampling_frequenct, defaults to 256
        """
        print("Debug `read_excel`")
        eeg_df = pd.read_excel(excel_path)
        print(eeg_df.head())
        # clean patient and other info
        eeg_df = eeg_df.iloc[16:]
        print("Cleaning patient data")
        print(eeg_df.head())
        # get channel names
        channel_pair_names = eeg_df.columns.to_list()
        # calcuate signal duration
        signal_length_seconds = len(eeg_df) // s_freq
        # convert signal to MNE format for compatibility
        mne_info = mne.create_info(
                ch_names=channel_pair_names,
                sfreq=s_freq,
                ch_types="eeg"
                )
        mne_data = mne.io.RawArray(eeg_df.values,info=mne_info,verbose=False)

        return(
                mne_data,signal_length_seconds
                )

    def read_edf(self, edf_path: str, differential_array):
        """Read raw EEG signal stored in .edf format"""
        raw_eeg = mne.io.read_raw_edf(edf_path, preload=True)

        raw_eeg.filter(None, 30.0, verbose=False)

        return self.raw_to_bipolar(
            raw_eeg, differential_array
        ), self.get_signal_length_seconds(raw_eeg)

    def read_eeg(self, edf_path: str, differential_array):
        """Read raw EEG signal stored in .eeg format"""
        raw_eeg = mne.io.read_raw_nihon(edf_path, preload=True)

        # add a low-pass filter
        raw_eeg.filter(None, 30.0, verbose=False)

        return self.raw_to_bipolar(
            raw_eeg, differential_array
        ), self.get_signal_length_seconds(raw_eeg)

    def raw_to_bipolar(self, raw_eeg, channel_pair_dict):
        bipolar_diff = []
        channel_pair_names = []
        # chanel_names = raw_eeg.info["ch_names"]

        for key, value in channel_pair_dict.items():
            c_1 = raw_eeg[value[0].strip()][0][0].astype(np.float16)
            c_2 = raw_eeg[value[1].strip()][0][0].astype(np.float16)
            bipolar_diff.append(c_1 - c_2)
            channel_pair_names.append(key)

        # create a mne eef data
        bipolar_montage_info = mne.create_info(
            ch_names=channel_pair_names, sfreq=raw_eeg.info["sfreq"], ch_types="eeg"
        )
        bipolar_montage_raw = mne.io.RawArray(
            bipolar_diff, info=bipolar_montage_info, verbose=False
        )

        return bipolar_montage_raw

    def label_figure(self, axes, channel_names):
        # label the last axes
        axes.set_xlabel("time/s")
        # give each axes a y-label corresponding to teh channel
        # or bipolar montage pair name
        self.y_tick_pos = [i * self.scale_factor for i in range(len(channel_names))]
        print(f"{self.y_tick_pos=}")
        print(f"{channel_names=}")

        axes.set_yticks(self.y_tick_pos)
        axes.set_yticklabels(channel_names)

        # disable yticks
        # axs.yaxis.set_major_locator(NullLocator())
        # axs.yaxis.set_minor_locator(NullLocator())

        return axes

    def plot_signal(self, raw_eeg, axes):
        """Plot EEG signal
        - Xticks should represent seconds
        """
        channel_names = raw_eeg.info["ch_names"]

        # label the axes
        axes = self.label_figure(axes, channel_names)
        s_freq = raw_eeg.info["sfreq"]

        # get the numpy array signal
        signal = raw_eeg.get_data()
        signal_length = signal.shape[-1]  # int(s_freq * 10)

        # in samples
        t = np.linspace(0, signal_length - 1, signal_length) / s_freq

        # just plot on each exes for now
        for i in range(signal.shape[0]):
            axes.plot(t, i * self.scale_factor + signal[i, :signal_length], linewidth=1)
