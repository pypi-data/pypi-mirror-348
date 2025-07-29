import multiprocessing
import numpy as np
import pandas as pd
from matplotlib.backends.backend_pdf import PdfPages
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.axes._axes import Axes 
from datetime import datetime, timezone
from shapely import get_coordinates

from typing import Optional, Tuple, Dict, List, Any, Union
from abc import ABC, abstractmethod

from .input import DataLoader, RecordingLoader, Recording, ROILoader, ROI, GridWrapperROILoader
from . import results
from .analysis import AnalysisROI


def process_analysis_rois(analysis_roi: AnalysisROI, configs: Dict[str, Any]) -> AnalysisROI:
    analysis_roi.compute_mean_intensity_timeseries(configs['limit_analysis_to_frame_interval'], configs['start_frame_idx'], configs['end_frame_idx'])
    if np.mean(analysis_roi.mean_intensity_over_time) >= configs['signal_average_threshold']:
        analysis_roi.detect_peaks(configs['signal_to_noise_ratio'], configs['octaves_ridge_needs_to_spann'], configs['noise_window_size'])
        analysis_roi.estimate_baseline(configs['baseline_estimation_method'])
        analysis_roi.compute_area_under_curve()
        analysis_roi.compute_amplitude_and_delta_f_over_f()
        analysis_roi.compute_variance_area(configs['variance'])
    return analysis_roi
    


class AnalysisJob:

    def __init__(self, 
                 number_of_parallel_processes: int,
                 data_loaders: Dict[str, Union[DataLoader, List[DataLoader]]]
                ) -> None:
        self.number_of_parallel_processes = number_of_parallel_processes
        self.recording_loader = data_loaders['recording']
        self.parent_dir_path = self.recording_loader.filepath.parent  
        if 'rois' in data_loaders.keys():
            self.rois_source = 'file'
            self.roi_loaders = data_loaders['rois']
        else:
            self.rois_source = 'grid'
            self.roi_loaders = [GridWrapperROILoader(self.recording_loader.filepath)]
        if 'focus_area' in data_loaders.keys():
            self.focus_area_enabled = True
            self.focus_area_loader = data_loaders['focus_area']
        else:
            self.focus_area_enabled = False
            self.focus_area = None

    
    def preview_window_size(self, window_size: int) -> Tuple[Figure, Axes]:
        self.load_data_into_memory(window_size)
        grid_configs = self.roi_loaders[0].configs
        fig, ax = results.plot_window_size_preview(self.recording.preview, grid_configs, self.focus_area)
        return fig, ax

    
    def load_data_into_memory(self, window_size: int) -> None:
        if hasattr(self, 'recording') == False:
            self.recording = self.recording_loader.load_and_parse_file_content()
        if hasattr(self, 'all_analysis_rois') == False:
            self.all_analysis_rois = self._create_all_analysis_rois(window_size)
        elif self.rois_source == 'grid':
            if self.roi_loaders[0].window_size != window_size:
                self.all_analysis_rois = self._create_all_analysis_rois(window_size)


    def _create_all_analysis_rois(self, window_size: int) -> List[AnalysisROI]:     
        self.all_rois = self._load_data_from_all_roi_loaders(window_size)
        if self.focus_area_enabled == True:
            self.focus_area = self.focus_area_loader.load_and_parse_file_content()[0]
            self.all_rois = self._filter_rois_by_focus_area()
        return self._create_analysis_rois()

    
    def _load_data_from_all_roi_loaders(self, window_size: int) -> List[ROI]:
        all_rois = []
        for roi_loader in self.roi_loaders:
            if type(roi_loader) == GridWrapperROILoader:
                roi_loader.set_configs_for_grid_creation(self.recording.preview.shape[1], self.recording.preview.shape[0], window_size)
            all_rois += roi_loader.load_and_parse_file_content()
        if self.rois_source == 'grid':
            self.grid_configs = self.roi_loaders[0].configs
        else:
            self.grid_configs = None
        return all_rois
    

    def _filter_rois_by_focus_area(self) -> List[ROI]:
        filtered_rois = [roi for roi in self.all_rois if roi.as_polygon.within(self.focus_area.as_polygon)]
        return filtered_rois
        

    def _create_analysis_rois(self) -> List[AnalysisROI]:
        all_analysis_rois = []
        if self.rois_source == 'file':
            self._create_and_add_label_ids_to_all_rois_from_file()
        for roi in self.all_rois:
            roi_bounding_box_row_col_coords = get_coordinates(roi.as_polygon.envelope).astype('int')
            row_min, col_min = roi_bounding_box_row_col_coords.min(axis=0)
            row_max, col_max = roi_bounding_box_row_col_coords.max(axis=0)   
            zstack = self.recording.zstack[:, row_min:row_max, col_min:col_max, :]
            analysis_roi = AnalysisROI(roi, (row_min, col_min), zstack)
            all_analysis_rois.append(analysis_roi)
        return all_analysis_rois


    def _create_and_add_label_ids_to_all_rois_from_file(self) -> List[str]:
        roi_count = len(self.all_rois)
        zfill_factor = int(np.log10(roi_count)) + 1
        for idx, roi in enumerate(self.all_rois):
            label_id = str(idx + 1).zfill(zfill_factor)
            roi.add_label_id(label_id)

    
    def run_analysis(self,
                     window_size: int,
                     limit_analysis_to_frame_interval: bool,
                     start_frame_idx: int,
                     end_frame_idx: int,
                     signal_average_threshold: float,
                     signal_to_noise_ratio: float,
                     octaves_ridge_needs_to_spann: float,
                     noise_window_size: int,
                     baseline_estimation_method: str,                     
                     include_variance: bool,
                     variance: int
                    ) -> None:
        self._set_analysis_start_datetime()
        self.load_data_into_memory(window_size)
        configs = locals()
        configs.pop('self')
        copy_of_all_analysis_rois = self.all_analysis_rois.copy()
        with multiprocessing.Pool(processes = self.number_of_parallel_processes) as pool:
            processed_analysis_rois = pool.starmap(process_analysis_rois, [(analysis_roi, configs) for analysis_roi in copy_of_all_analysis_rois])
        self.all_analysis_rois = processed_analysis_rois


    def _set_analysis_start_datetime(self) -> None:
            users_local_timezone = datetime.now().astimezone().tzinfo
            self.analysis_start_datetime = datetime.now(users_local_timezone) 


    def create_results(self, 
                       save_overview_png: bool,
                       save_detailed_results: bool,
                       minimum_activity_counts: int, 
                       signal_average_threshold: float, 
                       signal_to_noise_ratio: float
                      ) -> None:
        self._ensure_results_dir_exists()
        activity_filtered_analysis_rois = [roi for roi in self.all_analysis_rois if roi.peaks_count >= minimum_activity_counts]
        
        self.activity_overview_plot = results.plot_activity_overview(analysis_rois_with_sufficient_activity = activity_filtered_analysis_rois,
                                                                     preview_image = self.recording.preview,
                                                                     indicate_activity = True,
                                                                     focus_area = self.focus_area,
                                                                     grid_configs = self.grid_configs)
        if save_overview_png == True:
            self.activity_overview_plot[0].savefig(self.results_dir_path.joinpath('activity_overview.png'), dpi = 300)
            label_id_overview_fig, label_id_overview_ax = results.plot_rois_with_label_id_overview(analysis_rois_with_sufficient_activity = activity_filtered_analysis_rois,
                                                                                                   preview_image = self.recording.preview,
                                                                                                   focus_area = self.focus_area,
                                                                                                   grid_configs = self.grid_configs)
            label_id_overview_fig.savefig(self.results_dir_path.joinpath('ROI_label_IDs_overview.png'), dpi = 300)
            plt.close()
        if save_detailed_results == True:
            self._create_and_save_csv_result_files(activity_filtered_analysis_rois)
            self._create_and_save_individual_traces_pdf_result_file(activity_filtered_analysis_rois)


    def _ensure_results_dir_exists(self) -> None:
        if hasattr(self, 'results_dir_path') == False:
            prefix_with_datetime = self.analysis_start_datetime.strftime('%Y_%m_%d_%H-%M-%S_results_for')
            recording_filename_without_extension = self.recording.filepath.name.replace(self.recording.filepath.suffix, '')
            if self.focus_area_enabled == True:
                focus_area_filename_without_extension = self.focus_area.filepath.name.replace(self.focus_area.filepath.suffix, '')
                results_dir_name = f'{prefix_with_datetime}_{recording_filename_without_extension}_with_{focus_area_filename_without_extension}'                
            else:
                results_dir_name = f'{prefix_with_datetime}_{recording_filename_without_extension}'
            self.results_dir_path = self.parent_dir_path.joinpath(results_dir_name)
            self.results_dir_path.mkdir()       


    def _create_variance_area_dataframe(self, filtered_rois: List[AnalysisROI]) -> pd.DataFrame:
        data = {'ROI label ID': [],
                'Variance Area': []}
        for roi in filtered_rois:
            data['ROI label ID'].append(roi.label_id)
            data['Variance Area'].append(roi.variance_area)
        df = pd.DataFrame(data = data)
        return df
    
    
    def _create_and_save_csv_result_files(self, filtered_rois: List[AnalysisROI]) -> None:
        if len(filtered_rois) > 0:
            df_variance_areas = self._create_variance_area_dataframe(filtered_rois)
            df_variance_areas.to_csv(self.results_dir_path.joinpath('Variance_area_results.csv'), index = False)
            peak_results_per_roi = [results.export_peak_results_df_from_analysis_roi(roi) for roi in filtered_rois]
            df_all_peak_results = pd.concat(peak_results_per_roi, ignore_index = True)
            max_peak_count_across_all_rois = df_all_peak_results.groupby('ROI label ID').count()['peak frame index'].max()
            zfill_factor = int(np.log10(max_peak_count_across_all_rois)) + 1
            amplitude_and_delta_f_over_f_results_all_rois = []
            auc_results_all_rois = []
            for roi_label_id in df_all_peak_results['ROI label ID'].unique():
                tmp_df_single_roi = df_all_peak_results[df_all_peak_results['ROI label ID'] == roi_label_id].copy()
                amplitude_and_delta_f_over_f_results_all_rois.append(results.create_single_roi_amplitude_and_delta_f_over_f_results(tmp_df_single_roi, zfill_factor))
                auc_results_all_rois.append(results.create_single_roi_auc_results(tmp_df_single_roi, zfill_factor))
            df_all_amplitude_and_delta_f_over_f_results = pd.concat(amplitude_and_delta_f_over_f_results_all_rois, ignore_index = True)
            df_all_auc_results = pd.concat(auc_results_all_rois, ignore_index = True)
            # Once all DataFrames are created successfully, write them to disk 
            df_all_peak_results.to_csv(self.results_dir_path.joinpath('all_peak_results.csv'), index = False)
            df_all_amplitude_and_delta_f_over_f_results.to_csv(self.results_dir_path.joinpath('Amplitude_and_dF_over_F_results.csv'), index = False)
            df_all_auc_results.to_csv(self.results_dir_path.joinpath('AUC_results.csv'), index = False)

    
    def _create_and_save_individual_traces_pdf_result_file(self, filtered_rois: List[AnalysisROI]) -> None:
            filepath = self.results_dir_path.joinpath('Individual_traces_with_identified_events.pdf')
            with PdfPages(filepath) as pdf:
                for indicate_activity in [True, False]:
                    overview_fig, ax = results.plot_activity_overview(filtered_rois, self.recording.preview, indicate_activity, self.focus_area, self.grid_configs)
                    pdf.savefig(overview_fig)
                    plt.close()
                label_ids_overview_fig, ax = results.plot_rois_with_label_id_overview(filtered_rois, self.recording.preview, self.focus_area, self.grid_configs)
                pdf.savefig(label_ids_overview_fig)
                plt.close()
                for roi in filtered_rois:
                    fig = results.plot_intensity_trace_with_identified_peaks_for_individual_roi(roi)
                    pdf.savefig(fig)
                    plt.close()