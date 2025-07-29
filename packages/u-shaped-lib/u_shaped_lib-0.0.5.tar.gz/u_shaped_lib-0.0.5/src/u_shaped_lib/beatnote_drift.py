#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Beatnote Drift Analysis Module

This module provides tools for analyzing and visualizing beatnote drift measurements in optical systems.
Key features include:
- Loading and parsing beatnote measurement data
- Processing time-dependent frequency and power measurements
- Statistical analysis of frequency drift (mean, standard deviation, peak-to-peak)
- Visualization of drift and power data with customizable units
- Support for various data formats and conversion factors

The module is particularly useful for long-term stability analysis of optical systems
and can handle both frequency and power measurements simultaneously.
"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from typing import Tuple, Optional, Dict

def load_beatnote_data(filepath: str) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """
    Load beatnote data from a file.
    
    This function reads a beatnote measurement file and extracts timestamps,
    frequencies, and power values. It handles date parsing and data formatting.
    
    Parameters
    ----------
    filepath : str
        Path to the beatnote data file
        
    Returns
    -------
    Tuple[np.ndarray, np.ndarray, np.ndarray]
        Tuple containing:
        - timestamps : np.ndarray
            Array of timestamps as numpy datetime64 objects
        - frequencies : np.ndarray
            Array of frequencies in Hz
        - powers : np.ndarray
            Array of power values in dBm
            
    Notes
    -----
    The function assumes the file has a header row followed by space-delimited data
    with columns: Date, Time, Frequency, Power. Dates are parsed in day-first format.
    """
    df = pd.read_csv(
        filepath,
        sep=' ',
        names=['Date', 'Time', 'Frequency', 'Power'],
        parse_dates={'Timestamp': ['Date', 'Time']},
        dayfirst=True,
        skiprows=1
    )
    
    return df['Timestamp'].values, df['Frequency'].values, df['Power'].values

def process_beatnote_data(
    timestamps: np.ndarray,
    frequencies: np.ndarray,
    powers: np.ndarray,
    freq_conversion: float = 1e-9,  # Hz to GHz
    power_conversion: float = 20/1000  # Powermeter power to actual power in mW
) -> Dict[str, np.ndarray]:
    """
    Process beatnote data to calculate time and frequency drift.
    
    This function processes raw beatnote measurements to calculate time-based
    drift and convert units as needed.
    
    Parameters
    ----------
    timestamps : np.ndarray
        Array of timestamps
    frequencies : np.ndarray
        Array of frequencies in Hz
    powers : np.ndarray
        Array of power values in dBm
    freq_conversion : float, optional
        Conversion factor from Hz to desired frequency unit (default: 1e-9 for GHz)
    power_conversion : float, optional
        Conversion factor from dBm to desired power unit (default: 20/1000 for mW)
        
    Returns
    -------
    Dict[str, np.ndarray]
        Dictionary containing processed data:
        - hours : np.ndarray
            Time in hours from start
        - freq_drift : np.ndarray
            Frequency drift in converted units
        - power_converted : np.ndarray
            Power in converted units
            
    Notes
    -----
    Time is converted to hours from the start of the measurement.
    Frequency drift is calculated relative to the first measurement.
    """
    hours = (timestamps - timestamps[0]).astype('timedelta64[s]').astype(float) / 3600
    freq_drift = (frequencies - frequencies[0]) * freq_conversion
    power_converted = powers * power_conversion
    
    return {
        'hours': hours,
        'freq_drift': freq_drift,
        'power_converted': power_converted
    }

def analyze_beatnote_drift(freq_drift: np.ndarray) -> Dict[str, float]:
    """
    Analyze beatnote drift statistics.
    
    This function calculates key statistical measures of frequency drift,
    including mean drift, standard deviation, and peak-to-peak variation.
    
    Parameters
    ----------
    freq_drift : np.ndarray
        Array of frequency drift values in GHz
        
    Returns
    -------
    Dict[str, float]
        Dictionary containing analysis results:
        - mean : float
            Mean drift in GHz
        - std : float
            Standard deviation in GHz
        - peak_to_peak : float
            Peak-to-peak variation in GHz
            
    Notes
    -----
    All statistics are calculated on the raw drift values without any filtering
    or outlier removal.
    """
    print(freq_drift)
    
    return {
        'mean': np.mean(freq_drift),
        'std': np.std(freq_drift),
        'peak_to_peak': np.max(freq_drift) - np.min(freq_drift)
    }

def plot_beatnote_data(
    processed_data: Dict[str, np.ndarray],
    freq_ylim: Optional[Tuple[float, float]] = None,
    power_ylim: Optional[Tuple[float, float]] = None,
    freq_unit: str = 'GHz',
    power_unit: str = 'mW',
    save_path: Optional[str] = None
) -> None:
    """
    Plot beatnote frequency drift and power data.
    
    This function creates a dual-axis plot showing both frequency drift
    and power measurements over time.
    
    Parameters
    ----------
    processed_data : Dict[str, np.ndarray]
        Dictionary containing processed data from process_beatnote_data
    freq_ylim : Optional[Tuple[float, float]], optional
        Y-axis limits for frequency plot
    power_ylim : Optional[Tuple[float, float]], optional
        Y-axis limits for power plot
    freq_unit : str, optional
        Unit for frequency axis, by default 'GHz'
    power_unit : str, optional
        Unit for power axis, by default 'mW'
    save_path : Optional[str], optional
        Path to save the plot
        
    Notes
    -----
    Creates a plot with frequency drift on the left axis and power on the right axis.
    If y-limits are not provided, they are automatically calculated with 10% padding.
    The plot includes a grid and proper axis labels.
    """
    fig, ax1 = plt.subplots()
    
    # Plot frequency drift
    ax1.plot(processed_data['hours'], processed_data['freq_drift'], 
             '.', color='tab:blue', label='Beatnote')
    ax1.set_xlabel('Time (hours)')
    ax1.set_ylabel(f'Frequency ({freq_unit})', color='tab:blue')
    ax1.tick_params(axis='y', labelcolor='tab:blue')
    
    # Set frequency y-limits if not provided
    if freq_ylim is None:
        freq_data = processed_data['freq_drift']
        max_abs = max(abs(np.min(freq_data)), abs(np.max(freq_data)))
        # Add 10% padding and make symmetric
        max_abs = max_abs * 1.1
        freq_ylim = (-max_abs, max_abs)
    ax1.set_ylim(freq_ylim)
    ax1.grid(True)
    
    # Plot power only if data exists and is not all NaN
    if 'power_converted' in processed_data:
        power_data = processed_data['power_converted']
        if not np.all(np.isnan(power_data)):
            ax2 = ax1.twinx()
            ax2.plot(processed_data['hours'], power_data, 
                     '.', color='tab:orange', label='Power')
            ax2.set_ylabel(f'Power ({power_unit})', color='tab:orange')
            ax2.tick_params(axis='y', labelcolor='tab:orange')
            
            # Set power y-limits if not provided
            if power_ylim is None:
                power_data = power_data[~np.isnan(power_data)]  # Remove NaN values
                min_power = np.nanmin(power_data)
                max_power = np.nanmax(power_data)
                power_range = max_power - min_power
                # Add 10% padding
                power_ylim = (
                    min_power - 0.1 * power_range,
                    max_power + 0.1 * power_range
                )
            ax2.set_ylim(power_ylim)
            
            # Add legend with both frequency and power
            lines1, labels1 = ax1.get_legend_handles_labels()
            lines2, labels2 = ax2.get_legend_handles_labels()
            ax1.legend(lines1 + lines2, ['Beatnote', 'Power'], loc='upper right')
        else:
            # Add legend with only frequency
            ax1.legend(['Beatnote'], loc='upper right')
    else:
        # Add legend with only frequency
        ax1.legend(['Beatnote'], loc='upper right')
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, bbox_inches='tight')

def analyze_and_plot_beatnote(
    filepath: str,
    freq_conversion: float = 1e-9,  # Hz to GHz
    power_conversion: float = 20/1000,  # Powermeter power to actual power in mW
    freq_unit: str = 'GHz',
    power_unit: str = 'mW',
    freq_ylim: Optional[Tuple[float, float]] = None,
    power_ylim: Optional[Tuple[float, float]] = None,
    save_path: Optional[str] = None
) -> Dict[str, float]:
    """
    Complete analysis and plotting of beatnote data from a single file.
    
    This is a high-level function that combines loading, processing, analysis,
    and plotting of beatnote measurements.
    
    Parameters
    ----------
    filepath : str
        Path to the beatnote data file
    freq_conversion : float, optional
        Conversion factor from Hz to desired frequency unit, by default 1e-9 (GHz)
    power_conversion : float, optional
        Conversion factor from dBm to desired power unit, by default 20/1000 (mW)
    freq_unit : str, optional
        Unit for frequency axis, by default 'GHz'
    power_unit : str, optional
        Unit for power axis, by default 'mW'
    freq_ylim : Optional[Tuple[float, float]], optional
        Y-axis limits for frequency plot
    power_ylim : Optional[Tuple[float, float]], optional
        Y-axis limits for power plot
    save_path : Optional[str], optional
        Path to save the plot
        
    Returns
    -------
    Dict[str, float]
        Dictionary containing analysis results:
        - mean : float
            Mean drift in specified frequency unit
        - std : float
            Standard deviation in specified frequency unit
        - peak_to_peak : float
            Peak-to-peak variation in specified frequency unit
            
    Notes
    -----
    This function provides a complete workflow from raw data to analysis and visualization.
    It handles all the intermediate steps automatically.
    """
    # Load and process data
    timestamps, frequencies, powers = load_beatnote_data(filepath)
    processed_data = process_beatnote_data(
        timestamps, 
        frequencies, 
        powers,
        freq_conversion=freq_conversion,
        power_conversion=power_conversion
    )
    
    # Analyze drift
    analysis_results = analyze_beatnote_drift(processed_data['freq_drift'])
    
    # Plot results
    plot_beatnote_data(
        processed_data, 
        freq_ylim=freq_ylim, 
        power_ylim=power_ylim,
        freq_unit=freq_unit,
        power_unit=power_unit,
        save_path=save_path
    )
    
    return analysis_results

if __name__ == "__main__":
    # Example usage
    filepath = r"path/to/beatnote/data.txt"
    results = analyze_and_plot_beatnote(
        filepath,
        freq_conversion=1e-6,  # Convert to MHz instead of GHz
        power_conversion=1,    # Keep in dBm
        freq_unit='MHz',
        power_unit='dBm',
        save_path="beatnote_analysis.pdf"
    )
    print("Analysis results:", results)