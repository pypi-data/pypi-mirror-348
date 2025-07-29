import numpy as np
import pandas as pd
from scipy import signal
from pybaselines import Baseline
from collections import Counter
from shapely import Polygon, get_coordinates
from skimage.measure import grid_points_in_poly

from typing import Optional, Tuple, Dict, List, Callable
from dataclasses import dataclass

from .input import ROI


class BaselineEstimatorFactory:
        
    @property
    def supported_baseline_estimation_methods(self) -> Dict[str, Callable]:
        supported_baseline_estimation_methods = {'asls': Baseline().asls,
                                                 'fabc': Baseline().fabc,
                                                 'psalsa': Baseline().psalsa,
                                                 'std_distribution': Baseline().std_distribution}
        return supported_baseline_estimation_methods

    def get_baseline_estimation_callable(self, algorithm_acronym: str) -> Callable:
        baseline_estimation_method = self.supported_baseline_estimation_methods[algorithm_acronym]
        return baseline_estimation_method



@dataclass
class Peak:

    frame_idx: int
    intensity: float
    amplitude: Optional[float]=None
    delta_f_over_f: Optional[float]=None
    has_neighboring_intersections: Optional[bool]=None
    frame_idxs_of_neighboring_intersections: Optional[Tuple[int, int]]=None
    area_under_curve: Optional[float]=None
    peak_type: Optional[str]=None



class AnalysisROI:
    
    def __init__(self, roi: ROI, row_col_offset: Tuple[int, int], zstack: np.ndarray):
        self.label_id = roi.label_id
        self.as_polygon = roi.as_polygon
        self.boundary_row_col_coords = roi.boundary_row_col_coords
        self.row_offset = row_col_offset[0]
        self.col_offset = row_col_offset[1]
        self.zstack = zstack
        self.centroid_row_col_coords = get_coordinates(self.as_polygon.centroid).astype('int')[0]
        self.as_mask = self._convert_polygon_to_mask()
        self.peaks_count = 0


    def _convert_polygon_to_mask(self) -> np.ndarray:
        roi_row_col_coords = [(row_idx - self.row_offset, col_idx - self.col_offset) for (row_idx, col_idx) in get_coordinates(self.as_polygon).astype('int')]
        grid_shape = (self.zstack.shape[1], self.zstack.shape[2])
        mask = grid_points_in_poly(grid_shape, roi_row_col_coords)
        dimension_adjusted_mask = np.expand_dims(mask, axis = (0, 3))
        return dimension_adjusted_mask

    
    def compute_mean_intensity_timeseries(self, limit_analysis_to_frame_interval: bool, start_frame_idx: int, end_frame_idx: int) -> None:
        if limit_analysis_to_frame_interval == True:
            self.mean_intensity_over_time = np.mean(self.zstack[start_frame_idx:end_frame_idx], axis = (1,2,3), where = self.as_mask)
        else:
            self.mean_intensity_over_time = np.mean(self.zstack, axis = (1,2,3), where = self.as_mask)


    def detect_peaks(self, signal_to_noise_ratio: float, octaves_ridge_needs_to_spann: float, noise_window_size: int) -> None:
        widths = np.logspace(np.log10(1), np.log10(self.mean_intensity_over_time.shape[0]), 100)
        min_length = octaves_ridge_needs_to_spann / np.log2(widths[1] / widths[0])
        n_padded_frames = int(np.median(widths)) + 1
        signal_padded_with_reflection = np.pad(self.mean_intensity_over_time, n_padded_frames, 'reflect')
        frame_idxs_of_peaks_in_padded_signal = signal.find_peaks_cwt(vector = signal_padded_with_reflection, 
                                                         wavelet = signal.ricker, 
                                                         widths = widths, 
                                                         min_length = min_length,
                                                         max_distances = widths / 4, # default
                                                         gap_thresh = 0.0,
                                                         noise_perc = 5, # default: 10
                                                         min_snr = signal_to_noise_ratio,
                                                         window_size = noise_window_size
                                                        )
        frame_idxs_of_peaks_in_padded_signal = frame_idxs_of_peaks_in_padded_signal[((frame_idxs_of_peaks_in_padded_signal >= n_padded_frames) & 
                                                                                     (frame_idxs_of_peaks_in_padded_signal < self.mean_intensity_over_time.shape[0] + n_padded_frames))]
        self.frame_idxs_of_peaks = frame_idxs_of_peaks_in_padded_signal - n_padded_frames
        self.peaks = {}
        for peak_frame_idx in self.frame_idxs_of_peaks:
            self.peaks[peak_frame_idx] = Peak(frame_idx = peak_frame_idx, intensity = self.mean_intensity_over_time[peak_frame_idx]) 
        self.peaks_count = self.frame_idxs_of_peaks.shape[0]


    def estimate_baseline(self, algorithm_acronym: str) -> None:
        baseline_estimation_method = BaselineEstimatorFactory().get_baseline_estimation_callable(algorithm_acronym)
        self.baseline = baseline_estimation_method(data = self.mean_intensity_over_time)[0]


    def compute_area_under_curve(self) -> None:
        self._get_unique_frame_idxs_of_intersections_between_signal_and_baseline()
        self._add_information_about_neighboring_intersections_to_peaks()
        area_under_curve_classification = {'peaks_with_auc': [], 'all_intersection_frame_idxs_pairs': []}
        for peak_frame_idx, peak in self.peaks.items():
            if peak.has_neighboring_intersections == True:
                idx_before_peak, idx_after_peak = peak.frame_idxs_of_neighboring_intersections
                peak.area_under_curve = np.trapz(self.mean_intensity_over_time[idx_before_peak:idx_after_peak + 1] - self.baseline[idx_before_peak:idx_after_peak + 1])
                area_under_curve_classification['peaks_with_auc'].append(peak)
                area_under_curve_classification['all_intersection_frame_idxs_pairs'].append(peak.frame_idxs_of_neighboring_intersections)
        self._classify_area_under_curve_types(area_under_curve_classification)

    
    def _get_unique_frame_idxs_of_intersections_between_signal_and_baseline(self) -> None:
        quick_estimate_of_intersection_frame_idxs = np.argwhere(np.diff(np.sign(self.mean_intensity_over_time - self.baseline))).flatten()
        intersection_frame_idxs = np.asarray([self._improve_intersection_frame_idx_estimation_by_interpolation(idx) for idx in quick_estimate_of_intersection_frame_idxs])
        self.unique_intersection_frame_idxs = np.unique(intersection_frame_idxs)


    def _add_information_about_neighboring_intersections_to_peaks(self) -> None:
        for peak_frame_idx, peak in self.peaks.items():
            if (peak_frame_idx > self.unique_intersection_frame_idxs[0]) & (peak_frame_idx < self.unique_intersection_frame_idxs[-1]):
                peak.has_neighboring_intersections = True
                idx_pre_peak = self.unique_intersection_frame_idxs[self.unique_intersection_frame_idxs < peak_frame_idx][-1]
                idx_post_peak = self.unique_intersection_frame_idxs[self.unique_intersection_frame_idxs > peak_frame_idx][0]
                peak.frame_idxs_of_neighboring_intersections = (idx_pre_peak, idx_post_peak)
            else:
                peak.has_neighboring_intersections = False


    def _improve_intersection_frame_idx_estimation_by_interpolation(self, idx_frame_0: int) -> int:
        """
        Designed to resolve the bias of the quick estimation of intersection points, which will always 
        return the first index of two frames between which an intersection was determined. This is done 
        by interpolating the data (for both signal & baseline) to a sub-frame resolution between the 
        previously identified intersection frame index, and the following frame index - as the intersection 
        might actually happen closer to this following frame. If interpolation estimates the intersection 
        precisely in the middle between the two frames, the later frame is returned (0.5 is rounded up).
        """
        idx_frame_1 = idx_frame_0 + 1
        num_interpolated_steps = 7
        # interpolate signal & baseline to sub-frame resolution:
        interpolated_signal_intensities = np.linspace(self.mean_intensity_over_time[idx_frame_0], self.mean_intensity_over_time[idx_frame_1], num = num_interpolated_steps)
        interpolated_baseline = np.linspace(self.baseline[idx_frame_0], self.baseline[idx_frame_1], num = num_interpolated_steps)
        # identify whether frame_idx_0 or frame_idx_1 is closer to interpolated intersection point
        signed_differences = np.sign(interpolated_signal_intensities - interpolated_baseline)
        if 0 in signed_differences: #intersection exactly at one or multiple interpolated index
            intersection_idx_in_interpolation = np.argwhere(signed_differences == 0).flatten()[0]
        else: 
            results_for_intersection_idxs = np.argwhere(np.diff(signed_differences)).flatten()
            assert results_for_intersection_idxs.size != 0, ('get_improved_intersection_idx_estimation_by_interpolation() expected an intersection between frames '
                                                             f'{idx_frame_0} and {idx_frame_1} in the provided arrays, but none were found!')
            intersection_idx_in_interpolation = results_for_intersection_idxs[0]
        # Based on interpolation, select whether intersection is closer to frame_idx_0 or frame_idx_1
        if intersection_idx_in_interpolation < np.median(np.arange(0, num_interpolated_steps, 1)):
            interpolation_evaluated_intersection_frame_idx = idx_frame_0
        else:
            interpolation_evaluated_intersection_frame_idx = idx_frame_1
        return interpolation_evaluated_intersection_frame_idx
    

    def _classify_area_under_curve_types(self, data_for_auc_classification: Dict[str, List]) -> None:
        if len(data_for_auc_classification['all_intersection_frame_idxs_pairs']) != len(set(data_for_auc_classification['all_intersection_frame_idxs_pairs'])):
            counter = Counter(data_for_auc_classification['all_intersection_frame_idxs_pairs'])
            reoccuring_intersection_frame_idxs = [pair_of_intersection_frame_idxs for pair_of_intersection_frame_idxs, count in counter.items() if count > 1]
        else:
            reoccuring_intersection_frame_idxs = []
        for peak in self.peaks.values():
            if peak in data_for_auc_classification['peaks_with_auc']:
                if peak.frame_idxs_of_neighboring_intersections in reoccuring_intersection_frame_idxs:
                    peak.peak_type = 'clustered'
                else:
                    peak.peak_type = 'singular'
            else:
                peak.peak_type = 'isolated'

    
    def compute_amplitude_and_delta_f_over_f(self):
        for peak in self.peaks.values():
            peak.amplitude = self.mean_intensity_over_time[peak.frame_idx] - self.baseline[peak.frame_idx]
            peak.delta_f_over_f = peak.amplitude / self.baseline[peak.frame_idx]


    def compute_variance_area(self, variance_window_size: int) -> None:
        mean_intensity_over_time_as_series = pd.Series(self.mean_intensity_over_time)
        rolling_means = mean_intensity_over_time_as_series.rolling(window=variance_window_size, min_periods=1).mean().values
        rolling_variances = mean_intensity_over_time_as_series.rolling(window=variance_window_size, min_periods=1).var().values
        variance_area_upper_border = rolling_means[1:] + rolling_variances[1:]
        variance_area_lower_border = rolling_means[1:] - rolling_variances[1:]
        self.variance_area = np.trapz(variance_area_upper_border - variance_area_lower_border)
