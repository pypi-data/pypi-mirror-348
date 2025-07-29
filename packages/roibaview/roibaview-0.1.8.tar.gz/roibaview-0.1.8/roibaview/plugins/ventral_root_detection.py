import pyqtgraph as pg
import os
import numpy as np
from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import QVBoxLayout, QLabel, QSpacerItem, QSizePolicy, QMessageBox, QDialog, \
    QPushButton, QLineEdit
from roibaview.gui_utils import BrowseFileDialog
import pandas as pd
import scipy.signal as sig
from roibaview.plugins.base import BasePlugin


class VentralRootDetectionPlugin(BasePlugin):
    name = "Ventral Root Detection"
    category = "tool"

    def __init__(self, config=None, parent=None):
        self.config = config
        self.parent = parent
        self.roi_signal = getattr(parent, "signal_roi_idx_changed", None)
        self.dialog = None

    def apply(self, *_):
        try:
            controller = getattr(self.parent, "controller", None)
            if not controller or not controller.selected_data_sets:
                raise RuntimeError("No controller or dataset selected.")

            name = controller.selected_data_sets[0]
            dtype = controller.selected_data_sets_type[0]
            roi = controller.current_roi_idx
            data = controller.data_handler.get_data_set(dtype, name)
            meta = controller.data_handler.get_data_set_meta_data(dtype, name)
            fr = meta["sampling_rate"]
            master_plot = controller.data_plotter.master_plot

            self.dialog = VentralRootDetection(
                data=data + meta["y_offset"],
                fr=fr,
                master_plot=master_plot,
                roi=roi,
                parent=self.parent
            )

            if self.roi_signal:
                self.roi_signal.connect(self.dialog.roi_changed)

            self.dialog.finished.connect(self._on_dialog_closed)
            self.dialog.show()

        except Exception as e:
            QMessageBox.critical(self.parent, "Ventral Root Detection Error", str(e))

    def _on_dialog_closed(self):
        if self.roi_signal and hasattr(self, 'dialog'):
            try:
                self.roi_signal.disconnect(self.dialog.roi_changed)
            except Exception:
                pass
        if hasattr(self, 'dialog') and self.dialog:
            self.dialog.deleteLater()
            self.dialog = None


class VentralRootDetection(QDialog):
    signal_roi_changed = pyqtSignal(int)
    main_window_closing = pyqtSignal()
    def __init__(self, data, fr, master_plot, roi, parent=None, **kwargs):
        super().__init__(parent)
        self.roi_idx = roi
        self.data = data  # this is the data set
        self.data_trace = self.data[:, self.roi_idx]  # this is the roi trace
        self.fr = fr
        self.time_axis = self.compute_time_axis(self.data_trace.shape[0], self.fr)
        self.master_plot = master_plot
        self.parameters = dict()
        self.parameters_range = dict()
        self.vr_events = dict()
        self.env_trace = None
        self.set_parameters()
        self.min_range = 0
        self.max_range = 1000
        # self.set_parameters_range()
        self._init_ui()
        self.main_window_running = True
        self.signal_roi_changed.connect(self.roi_changed)
        self.main_window_closing.connect(self.main_window_is_closing)

    def export_peaks(self):
        file_browser = BrowseFileDialog(self)
        file_dir = file_browser.save_file_name('csv file, (*.csv)')
        if file_dir:
            result = pd.DataFrame()
            result['onset_time'] = self.vr_events['onset_times']
            result['offset_time'] = self.vr_events['offset_times']
            result['onset_idx'] = self.vr_events['onset_idx']
            result['offset_idx'] = self.vr_events['offset_idx']
            result.to_csv(file_dir, index=False)
            env = pd.DataFrame(self.env_trace)
            env_dir = os.path.split(file_dir)[0] + '/envelope_trace.csv'
            env.to_csv(env_dir, index=False, header=False)

    @staticmethod
    def compute_time_axis(data_size, fr):
        max_time = data_size / fr
        return np.linspace(0, max_time, data_size)

    def main_window_is_closing(self):
        self.main_window_running = False
        self.close()

    def roi_changed(self, new_roi_idx):
        print('ROI CHANGED')
        self.roi_idx = new_roi_idx
        self.data_trace = self.data[:, self.roi_idx]

        # Update find vr events
        self.find_vr_events(self.parameters)
        self.update_plot()

    def _init_ui(self):
        layout = QVBoxLayout()
        self.parameters_labels = dict()
        for param_name in self.parameters.keys():
            label = QLabel(param_name)
            # Add text field
            field = QLineEdit()

            self.parameters_labels[param_name] = QLabel('0')

            # Connect slider signal to update function
            # slider.valueChanged.connect(lambda value, param=param_name: self.update_parameter(param, value))
            field.textChanged.connect(lambda value, param=param_name: self.update_parameter_only(param, value))
            layout.addWidget(label)
            # layout.addWidget(slider)
            layout.addWidget(field)
            layout.addWidget(self.parameters_labels[param_name])
            # Add spacer (width, height)
            spacer = QSpacerItem(20, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
            layout.addItem(spacer)

        self.update_button = QPushButton('UPDATE')
        self.update_button.clicked.connect(self.update_detection)
        layout.addWidget(self.update_button)

        self.export_button = QPushButton('Export...')
        self.export_button.clicked.connect(self.export_peaks)
        layout.addWidget(self.export_button)

        self.setLayout(layout)
        self.setWindowTitle("Peak Detection Parameters")
        # self.show()

    def update_detection(self):
        # Update Value Label
        for param_name in self.parameters.keys():
            self.parameters_labels[param_name].setText(f'{self.parameters[param_name]:.2f}')

        # Update find vr events
        self.find_vr_events(self.parameters)

        # Update Plot
        self.update_plot()

    def update_parameter_only(self, param_name, value):
        try:
            val = float(value)
        except ValueError:
            val = 1

        # Update parameter value
        self.parameters[param_name] = val

    def update_parameter(self, param_name, value):
        # Update parameter value
        if value == 0:
            self.parameters[param_name] = None
        else:
            self.parameters[param_name] = value

        parameters = self.parameters
        if value is not None:
            parameters[param_name] = value
        else:
            parameters[param_name] = None

        # Update Value Label
        self.parameters_labels[param_name].setText(f'{parameters[param_name]:.2f}')

        # Update find vr events
        self.find_vr_events(parameters)

        # Update Plot
        self.update_plot()

    def clear_plot(self):
        # check if there is already roi data plotted and remove it
        item_list = self.master_plot.items.copy()
        for item in item_list:
            if item.name() is not None:
                if item.name().startswith('event'):
                    self.master_plot.removeItem(item)

        for item in item_list:
            if item.name() is not None:
                if item.name().startswith('env'):
                    self.master_plot.removeItem(item)

    def update_plot(self):
        # Check if there is already roi data plotted and remove it
        self.clear_plot()

        if self.env_trace is not None:
            # Plot the Envelope
            plot_data_item_env = pg.PlotDataItem(
                self.time_axis, self.env_trace,
                pen=pg.mkPen(color=(0, 255, 0)),
                name='env',
                skipFiniteCheck=True,
                tip=None,
            )
            self.master_plot.addItem(plot_data_item_env)

            # Plot event onsets/offsets only if present
            if 'onset_idx' in self.vr_events and 'offset_idx' in self.vr_events:
                if len(self.vr_events['onset_idx']) > 0:
                    onset_plot = pg.ScatterPlotItem(
                        self.time_axis[self.vr_events['onset_idx']], self.env_trace[self.vr_events['onset_idx']],
                        pen=pg.mkPen(color=(255, 0, 0)),
                        brush=pg.mkBrush(color=(255, 0, 0)),
                        size=50,
                        symbol='arrow_down',
                        name='event_onset',
                        skipFiniteCheck=True,
                        tip=None,
                        hoverable=True,
                        hoverSize=100
                    )
                    self.master_plot.addItem(onset_plot)

                if len(self.vr_events['offset_idx']) > 0:
                    offset_plot = pg.ScatterPlotItem(
                        self.time_axis[self.vr_events['offset_idx']], self.env_trace[self.vr_events['offset_idx']],
                        pen=pg.mkPen(color=(0, 0, 255)),
                        brush=pg.mkBrush(color=(0, 0, 255)),
                        size=50,
                        symbol='arrow_down',
                        name='event_offset',
                        skipFiniteCheck=True,
                        tip=None,
                        hoverable=True,
                        hoverSize=100
                    )
                    self.master_plot.addItem(offset_plot)

    def set_parameters(self):
        self.parameters['threshold'] = 5  # times std
        self.parameters['large_th_factor'] = 20
        # self.parameters['vr_fr'] = self.fr  # in Hz
        self.parameters['vr_cutoff'] = 5  # in Hz
        self.parameters['movingaverage_window'] = 2  # in samples
        self.parameters['duration_th_secs'] = 5  # in secs. Events longer than that will be ignored
        self.parameters['minimal_event_distance'] = 4  # in secs. Events with a distance of less that will be merged

    @staticmethod
    def map_range(value, from_min, from_max, to_min, to_max):
        # First, scale the value from the input range to a 0-1 range
        scaled_value = (value - from_min) / (from_max - from_min)

        # Then, scale the value to fit within the output range
        mapped_value = to_min + (to_max - to_min) * scaled_value

        return mapped_value

    @staticmethod
    def envelope(data, rate, freq):
        nyquist = rate / 2
        if freq >= nyquist:
            freq = nyquist * 0.99  # Clamp just below Nyquist
        if freq <= 0:
            freq = nyquist * 0.1  # Ensure it's > 0

        sos = sig.butter(2, freq, 'lowpass', fs=rate, output='sos')
        env = (np.sqrt(2) * sig.sosfiltfilt(sos, np.abs(data))) ** 2
        return env

    @staticmethod
    def moving_average_filter(data, window):
        return np.convolve(data, np.ones(int(window)) / int(window), mode='same')

    @staticmethod
    def z_transform(data):
        result = (data - np.mean(data, axis=0)) / np.std(data, axis=0)
        return result

    def find_vr_events(self, parameters):
        data = self.data_trace.copy()

        if parameters['threshold'] is None:
            # If there is no Detection Threshold set one like this
            # Standard Deviation of the trace times 5
            th = np.std(data) * 5
        else:
            th = np.std(data) * parameters['threshold']

        # Compute envelope
        env = self.envelope(data=data, rate=self.fr, freq=parameters['vr_cutoff'])

        # Low pass filter ventral root envelope with a moving average
        env_fil = self.moving_average_filter(env, window=parameters['movingaverage_window'])
        self.env_trace = env_fil.copy()
        env_vr_z = self.z_transform(env_fil)

        # Create Binary
        binary = np.zeros_like(env_vr_z)
        binary[env_vr_z > th] = 1

        # Find onsets and offsets of ventral root activity
        onsets_offsets = np.diff(binary, append=0)
        time_axis = self.time_axis
        onset_idx = np.where(onsets_offsets > 0)[0]
        offset_idx = np.where(onsets_offsets < 0)[0]
        onset_times = time_axis[onset_idx]
        offset_times = time_axis[offset_idx]

        # check for motor activity that is too long (artifacts due to concatenating recordings) and remove it
        if len(offset_times) == len(onset_times):
            event_duration = offset_times - onset_times
            idx_remove = event_duration > parameters['duration_th_secs']
            onset_times = onset_times[np.invert(idx_remove)]
            offset_times = offset_times[np.invert(idx_remove)]
        else:
            print('WARNING: Number of onset times and offset times do not match!')

        # Merge Events that are to close to each other
        # Combine event information into a single list of tuples
        events = list(zip(onset_times, offset_times, onset_idx, offset_idx))
        # Sort events by their onset time
        events = sorted(events, key=lambda x: x[0])

        # Initialize lists to store merged events and their indices
        merged_onset_indices = []
        merged_offset_indices = []
        merged_onset_times = []
        merged_offset_times = []

        if not events:
            # No events detected, clear result and exit early
            self.vr_events.clear()
            return
        # Initialize the first event as the current event to merge
        current_onset_time, current_offset_time, current_onset_index, current_offset_index = events[0]

        for onset_time, offset_time, onset_index, offset_index in events[1:]:
            # Check if the current event is close to the previous one
            if onset_time - current_offset_time <= parameters['minimal_event_distance']:
                # Merge the events by extending the offset time and updating indices
                current_offset_time = max(current_offset_time, offset_time)
                current_offset_index = offset_index
            else:
                # If not close, save the current event and start a new one
                merged_onset_times.append(current_onset_time)
                merged_offset_times.append(current_offset_time)
                merged_onset_indices.append(current_onset_index)
                merged_offset_indices.append(current_offset_index)
                current_onset_time, current_offset_time = onset_time, offset_time
                current_onset_index, current_offset_index = onset_index, offset_index

        # Append the last merged event
        merged_onset_times.append(current_onset_time)
        merged_offset_times.append(current_offset_time)
        merged_onset_indices.append(current_onset_index)
        merged_offset_indices.append(current_offset_index)

        # Convert lists to numpy arrays
        merged_onset_times = np.array(merged_onset_times)
        merged_offset_times = np.array(merged_offset_times)
        merged_onset_indices = np.array(merged_onset_indices)
        merged_offset_indices = np.array(merged_offset_indices)

        # Collect results
        self.vr_events['onset_idx'] = merged_onset_indices
        self.vr_events['offset_idx'] = merged_offset_indices
        self.vr_events['onset_times'] = merged_onset_times
        self.vr_events['offset_times'] = merged_offset_times

    def closeEvent(self, event):
        self._cleanup()
        self.done(QDialog.DialogCode.Accepted)
        event.accept()
        # import gc
        # gc.collect()
        # print("Remaining VentralRootDetection instances:",
        #       [o for o in gc.get_objects() if isinstance(o, VentralRootDetection)])

    def _cleanup(self):
        try:
            if self.parent() and hasattr(self.parent(), "signal_roi_idx_changed"):
                self.parent().signal_roi_idx_changed.disconnect(self.roi_changed)
        except Exception:
            pass
        self.clear_plot()

    # def __del__(self):
    #     print("VentralRootDetection dialog deleted.")
