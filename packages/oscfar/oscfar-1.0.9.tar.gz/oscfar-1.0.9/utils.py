from fitburst.backend.generic import DataReader
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


class NpzReader(DataReader):
    """
    Class for reading .npz files containing spectrogram data.

    Inherits from fitburst.backend.generic.DataReader.

    Attributes:
        metadata (dict): Metadata associated with the data.
        downsampling_factor (int): Factor by which the data has been downsampled.
    """

    def __init__(self, fname, factor):
        """
        Initializes the NpzReader with the given file and downsampling factor.

        Args:
            fname (str): Path to the .npz file.
            factor (int): Downsampling factor applied to the data.
        """

        self.__fname = fname

        temp = np.load(fname, allow_pickle=True)
        self.metadata = temp["metadata"].tolist()
        temp.close()

        super().__init__(fname)
        self.downsampling_factor = factor

    def __repr__(self):
        """
        Returns a string representation of the NpzReader object.
        """

        return f"{self.__class__.__name__}(fname='{self.__fname}', file_downsampling={self.downsampling_factor})"

    def __str__(self):
        """
        Returns a string representation of the NpzReader object.
        """

        return f"(fname='{self.__fname}', file_downsampling={self.downsampling_factor})"


class NpzWriter:
    """
    Class for writing data to .npz files, typically after processing.

    Attributes:
        reader (NpzReader): An instance of NpzReader containing the original data.
        burst_parameters (dict): Dictionary of burst parameters to be saved.
    """

    dm_index = -2
    scattering_index = -4
    spectral_index = 0
    ref_freq = 400

    def __init__(self, original_data: NpzReader):
        """
        Initializes the NpzWriter with the given NpzReader instance.

        Args:
            original_data (NpzReader): An instance of NpzReader containing the
                                       original data to be processed and saved.
        """

        self.reader = original_data
        if self.reader.data_full is None:
            self.reader.load_data()

        self.burst_parameters = self.reader.burst_parameters

    def update_burst_parameters(self, **kwargs):
        """
        Updates the burst parameters with the provided keyword arguments.

        Args:
            **kwargs: Keyword arguments representing burst parameters to update.
                      Possible keys include:
                      - 'amplitude': Amplitude of the burst.
                      - 'dm': Dispersion measure of the burst.
                      - 'scattering_timescale': Scattering timescale of the burst.
                      - 'arrival_time': Arrival time of the burst.
                      - 'burst_width': Intrinsic width of the burst.
                      - 'spectral_running': Spectral index of the burst.
        """
        if "arrival_time" not in kwargs:
            raise KeyError(
                f"Cannot update parameters if number of ToAs is not provided. Please use the key 'arrival_time'."
            )

        # if "amplitude" in kwargs:
        #     self.burst_parameters["amplitude"] = kwargs["amplitude"]
        # if "dm" in kwargs:
        #     self.burst_parameters["dm"] = kwargs["dm"]
        # if "scattering_timescale" in kwargs:
        #     self.burst_parameters["scattering_timescale"] = kwargs[
        #         "scattering_timescale"
        #     ]
        # if "arrival_time" in kwargs:
        #     self.burst_parameters["arrival_time"] = kwargs["arrival_time"]
        # if "burst_width" in kwargs:
        #     self.burst_parameters["burst_width"] = kwargs["burst_width"]
        # if "spectral_running" in kwargs:
        #     self.burst_parameters["spectral_running"] = kwargs["spectral_running"]

        number_of_components = len(kwargs["arrival_time"])

        for param in self.burst_parameters:
            if param in kwargs:
                if len(kwargs[param]) != number_of_components:
                    raise ValueError(
                        f"Unexpected length of {len(kwargs[param])} for parameter {param} when {number_of_components} expected."
                    )

                self.burst_parameters[param] = kwargs[
                    param
                ]  # Safely put the kwargs' data into the burst parameters
            else:
                if type(self.burst_parameters[param]) != list:
                    self.burst_parameters[param] = [
                        self.burst_parameters[param]
                    ] * number_of_components
                else:
                    self.burst_parameters[param] += [
                        self.burst_parameters[param][-1]
                    ] * (number_of_components - len(self.burst_parameters[param]))

    def save(self, new_filepath: str):
        """
        Saves the processed data and burst parameters to a new .npz file.

        Args:
            new_filepath (str): Path to the new .npz file where the data
                                will be saved.
        """

        print(f"Saving file at {new_filepath}...")

        with open(new_filepath, "wb") as f:
            np.savez(
                f,
                data_full=self.reader.data_full,
                burst_parameters=self.burst_parameters,
                metadata=self.reader.metadata,
            )
        print(f"Saved file at {new_filepath} successfully.")


class Peaks:
    """
    Class to hold results from OS-CFAR.

    Attributes:
        peaks (np.array): First half of the OS-CFAR results containing the peaks resulting from the algorithm.
        threshold (np.array): Second half of the OS-CFAR results containing the threshold used by the algorithm.
    """

    def __init__(self, oscfar_result):
        """
        Initializes the Peaks object with the result from OS-CFAR.

        Args:
            oscfar_result (tuple): A tuple containing the detected peak indices
                                   and the threshold array.
        """

        self.peaks = np.array(oscfar_result[0])
        self.threshold = np.array(oscfar_result[1])


class WaterFallAxes:
    """
    Class to create axes for waterfall plots (spectrograms).

    Attributes:
        _data (DataReader): DataReader object containing the spectrogram data.
        show_ts (bool): Whether to show the time series plot.
        show_spec (bool): Whether to show the spectrum plot.
        im (matplotlib.axes._subplots.AxesSubplot): Axes for the spectrogram.
        ts (matplotlib.axes._subplots.AxesSubplot): Axes for the time series plot.
        spec (matplotlib.axes._subplots.AxesSubplot): Axes for the spectrum plot.
        time_series (np.ndarray): Time series data (sum over frequencies).
        freq_series (np.ndarray): Frequency series data (sum over time).
    """

    def __init__(
        self,
        data: DataReader,
        width: float,
        height: float,
        bottom: float,
        left: float = None,
        hratio: float = 1,
        vratio: float = 1,
        show_ts=True,
        show_spec=True,
        labels_on=[True, True],
        title="",
        readjust_title=0,
    ):
        """
        Initializes the WaterFallAxes object.

        Args:
            data (DataReader): DataReader object containing the spectrogram data.
            width (float): Width of the main spectrogram plot.
            height (float): Height of the main spectrogram plot.
            bottom (float): Bottom position of the main spectrogram plot.
            left (float, optional): Left position of the main spectrogram plot.
                                    Defaults to the value of 'bottom'.
            hratio (float, optional): Horizontal ratio for plot dimensions. Defaults to 1.
            vratio (float, optional): Vertical ratio for plot dimensions. Defaults to 1.
            show_ts (bool, optional): Whether to show the time series plot. Defaults to True.
            show_spec (bool, optional): Whether to show the spectrum plot. Defaults to True.
            labels_on (list, optional): List of two booleans indicating whether to
                                        show labels on the x and y axes, respectively.
                                        Defaults to [True, True].
            title (str, optional): Title of the plot. Defaults to "".
            readjust_title (int, optional): Vertical adjustment for the title position. Defaults to 0.
        """

        self._data = data
        self.show_ts = show_ts
        self.show_spec = show_spec

        if labels_on[0] or labels_on[1]:
            width = 0.6
            height = 0.6

        bot = bottom
        if left is None:
            left = bot

        im_w = width / hratio
        im_h = height / vratio

        self.im = plt.axes((left, bot, im_w, im_h))
        if self.show_ts:
            self.ts = plt.axes((left, im_h + bot, im_w, 0.2 / vratio), sharex=self.im)
            plt.text(
                1,  # - len(title) * 0.025,
                0.85 - readjust_title,
                title,
                transform=self.ts.transAxes,
                ha="right",
                va="bottom",
            )
        if self.show_spec:
            self.spec = plt.axes((im_w + left, bot, 0.2 / hratio, im_h), sharey=self.im)

        if labels_on[0] or labels_on[1]:
            if labels_on[0]:
                self.im.set_xlabel("Time (s)")
            if labels_on[1]:
                self.im.set_ylabel("Observing frequency (MHz)")
        else:
            plt.setp(self.im.get_xticklabels(), visible=False)
            plt.setp(self.im.get_xticklines(), visible=False)
            plt.setp(self.im.get_yticklabels(), visible=False)
            plt.setp(self.im.get_yticklines(), visible=False)

        if self.show_ts:
            plt.setp(self.ts.get_xticklabels(), visible=False)
            plt.setp(self.ts.get_xticklines(), visible=False)
            plt.setp(self.ts.get_yticklabels(), visible=False)
            plt.setp(self.ts.get_yticklines(), visible=False)
        if self.show_spec:
            plt.setp(self.spec.get_xticklabels(), visible=False)
            plt.setp(self.spec.get_xticklines(), visible=False)
            plt.setp(self.spec.get_yticklabels(), visible=False)
            plt.setp(self.spec.get_yticklines(), visible=False)

        self.time_series = np.sum(self._data.data_full, 0)
        self.freq_series = np.sum(self._data.data_full, 1)

    def plot(self):
        """
        Plots the spectrogram.
        """
        self.im.imshow(
            self._data.data_full,
            cmap="gist_yarg",
            aspect="auto",
            origin="lower",
            extent=[
                self._data.times[0],
                self._data.times[-1],
                self._data.freqs[0],
                self._data.freqs[-1],
            ],
        )
        if self.show_ts:
            self.ts.plot(self._data.times, self.time_series)
        if self.show_spec:
            self.spec.plot(self.freq_series, self._data.freqs)

    def plot_time_peaks(self, peaks: Peaks, color, show_thres=False):
        """
        Plots vertical lines on the spectrogram at the time indices of the detected peaks.
        Also plots the peaks on the time series plot if it is shown.

        Args:
            peaks (Peaks): An object containing the peak indices and threshold.
            color (str): Color for the vertical lines and scatter points.
            show_thres (bool): Whether to show the threshold on the time series plot.
        """

        for x in peaks.peaks:
            self.im.axvline(self._data.times[x], color=color, linestyle="--", alpha=0.5)

        if self.show_ts:
            self.ts.scatter(
                self._data.times[peaks.peaks],
                self.time_series[peaks.peaks],
                marker="o",
                color=color,
                zorder=10,
            )

        if show_thres:
            self.ts.plot(self._data.times, peaks.threshold, c="grey", linestyle="--")


class WaterFallGrid:
    """
    Class to create a grid of waterfall plots (spectrograms).

    Attributes:
        nrows (int): Number of rows in the grid.
        ncols (int): Number of columns in the grid.
        axes (np.ndarray): 2D array of WaterFallAxes objects representing the grid.
        vs (float): Vertical spacing between plots.
        hs (float): Horizontal spacing between plots.
    """

    def __init__(self, nrows: int, ncols: int, vspacing=0.1, hspacing=0.1):
        """
        Initializes the WaterFallGrid object.

        Args:
            nrows (int): Number of rows in the grid.
            ncols (int): Number of columns in the grid.
            vspacing (float, optional): Vertical spacing between plots. Defaults to 0.1.
            hspacing (float, optional): Horizontal spacing between plots. Defaults to 0.1.
        """

        # Spacing is actually an offset oops
        self.nrows = nrows
        self.ncols = ncols
        self.axes = np.zeros((nrows, ncols), dtype=object)
        self.vs = vspacing
        self.hs = hspacing

    def plot(
        self,
        data: list,
        peaks: list,
        titles: list,
        color,
        labels=[True, False],
        adjust_t=0,
        show_thres=False,
    ):
        """
        Plots the waterfall grid with the provided data, peaks, and titles.

        Args:
            data (list): List of DataReader objects, one for each subplot.
            peaks (list): List of Peaks objects, one for each subplot.
            titles (list): List of titles for each subplot.
            color (str): Color for the peak markers.
            labels (list, optional): List of two booleans indicating whether to
                                     show labels on the x and y axes, respectively.
                                     Defaults to [True, False].
            adjust_t (int, optional): Vertical adjustment for the title position. Defaults to 0.
            show_thres (bool): Whether to show the threshold on the time series plot.
        """

        if type(data) == list or type(peaks) == list or type(titles) == list:
            data = np.array(data).reshape((self.nrows, self.ncols))
            peaks = np.array(peaks).reshape((self.nrows, self.ncols))
            titles = np.array(titles).reshape((self.nrows, self.ncols))

        lefts = np.arange(0, 1, 1 / (self.ncols)) + self.hs
        bottoms = np.arange(0, 1, 1 / (self.nrows)) + self.vs
        for i in range(self.nrows):
            for j in range(self.ncols):
                ax = WaterFallAxes(
                    data[i, j],
                    0.75,
                    0.75,
                    bottoms[i],
                    left=lefts[j],
                    hratio=self.ncols,
                    vratio=self.nrows,
                    show_ts=True,
                    show_spec=True,
                    labels_on=labels,
                    title=titles[i, j],
                    readjust_title=adjust_t,
                )
                ax.plot()
                ax.plot_time_peaks(peaks[i, j], color, show_thres)
                self.axes[i, j] = ax

    def add_info(self, info: pd.DataFrame):
        """
        Adds a table with additional information below the grid.

        Args:
            info (pd.DataFrame): DataFrame containing the information to be displayed.
        """

        ax = plt.axes((0, 0, 1, self.vs - 0.1))
        plt.setp(ax.get_xticklabels(), visible=False)
        plt.setp(ax.get_yticklabels(), visible=False)
        plt.setp(ax.get_xticklines(), visible=False)
        plt.setp(ax.get_yticklines(), visible=False)

        table = ax.table(
            info.values,
            colLabels=info.columns,
            rowLabels=info.index,
            loc="bottom",
            cellLoc="center",
            rowLoc="center",
            bbox=[0, 0, 1, 1],
        )
