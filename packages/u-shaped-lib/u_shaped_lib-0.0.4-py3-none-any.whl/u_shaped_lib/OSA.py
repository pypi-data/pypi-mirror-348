"""
Optical Spectrum Analyzer (OSA) Data Processing Module

This module provides functionality for loading, processing, and visualizing data from Optical Spectrum Analyzers.
It includes tools for:
- Loading OSA data from single files or directories
- Processing wavelength and power measurements
- Plotting optical spectra with customizable parameters
- Handling metadata from OSA measurements

The module supports data in standard OSA formats and provides utilities for both single-file
and batch processing of multiple measurements.
"""

import numpy as np
import matplotlib.pyplot as plt
import os
from pathlib import Path
from typing import Union, List, Tuple, Optional

def load_osa_data(file_path: Union[str, Path]) -> Tuple[np.ndarray, np.ndarray, dict]:
    """
    Load OSA data from a single file.
    
    This function reads an OSA data file, extracts wavelength and power measurements,
    and parses any metadata from the file header. The power values are converted to dBm.
    
    Parameters
    ----------
    file_path : Union[str, Path]
        Path to the OSA data file
        
    Returns
    -------
    Tuple[np.ndarray, np.ndarray, dict]
        A tuple containing:
        - wavelengths : np.ndarray
            Array of wavelength values in nm
        - power : np.ndarray
            Array of power values in dBm
        - metadata : dict
            Dictionary containing metadata from the file header
            
    Notes
    -----
    The function assumes the file has a 4-line header followed by comma-separated data.
    Power values are automatically converted to dBm scale.
    """
    with open(file_path, 'r') as f:
        # Read header lines
        header_lines = []
        for _ in range(4):  # Assuming 4 header lines as per the original format
            header_lines.append(f.readline().strip())
        
        # Parse metadata
        metadata = {}
        for line in header_lines:
            if ':' in line:
                key, value = line.split(':')
                metadata[key.strip()] = float(value.split('[')[0].strip())
        
        # Read data
        data = np.loadtxt(f, delimiter=',')
        wavelengths = data[:, 0]
        power = data[:, 1]

        power = 10*np.log10(power)
        
    return wavelengths, power, metadata

def process_osa_directory(directory_path: Union[str, Path]) -> List[Tuple[np.ndarray, np.ndarray, dict, str]]:
    """
    Process all OSA data files in a directory.
    
    This function scans a directory for OSA data files and processes each one,
    collecting the results into a list. It handles errors gracefully and skips
    any files that cannot be processed.
    
    Parameters
    ----------
    directory_path : Union[str, Path]
        Path to directory containing OSA data files
        
    Returns
    -------
    List[Tuple[np.ndarray, np.ndarray, dict, str]]
        List of tuples, each containing:
        - wavelengths : np.ndarray
            Array of wavelength values in nm
        - power : np.ndarray
            Array of power values in dBm
        - metadata : dict
            Dictionary containing metadata from the file header
        - filename : str
            Name of the processed file
            
    Notes
    -----
    Only files with .txt extension are processed. Errors during processing
    are printed but don't stop the overall process.
    """
    directory_path = Path(directory_path)
    results = []
    
    for file_path in directory_path.glob('*'):
        if file_path.is_file() and file_path.suffix == '.txt':
            try:
                wavelengths, power, metadata = load_osa_data(file_path)
                results.append((wavelengths, power, metadata, file_path.name))
            except Exception as e:
                print(f"Error processing {file_path}: {str(e)}")
                
    return results

def plot_osa_spectrum(wavelengths: np.ndarray, 
                     power: np.ndarray, 
                     title: Optional[str] = None,
                     ylim: Optional[Tuple[float, float]] = None,
                     save_path: Optional[Union[str, Path]] = None) -> None:
    """
    Plot OSA spectrum with wavelength vs power.
    
    Creates a standardized plot of optical spectrum data with proper labeling
    and optional customization parameters.
    
    Parameters
    ----------
    wavelengths : np.ndarray
        Array of wavelength values in nm
    power : np.ndarray
        Array of power values in dBm
    title : Optional[str], optional
        Title for the plot. If None, uses default title 'OSA Spectrum'
    ylim : Optional[Tuple[float, float]], optional
        Tuple of (ymin, ymax) for y-axis limits
    save_path : Optional[Union[str, Path]], optional
        Path to save the plot. If None, plot is only displayed
        
    Notes
    -----
    The plot includes a grid and proper axis labels. If save_path is provided,
    the plot is saved before being displayed.
    """
    plt.figure(figsize=(10, 6))
    plt.plot(wavelengths, power)
    plt.xlabel('Wavelength [nm]')
    plt.ylabel('Power [dBm]')
    plt.title(title or 'OSA Spectrum')
    plt.grid(True)
    
    if ylim:
        plt.ylim(ylim)
    
    if save_path:
        plt.savefig(save_path)

    plt.show()

def process_and_plot_osa_data(data_path: Union[str, Path], 
                             plot: bool = True,
                             save_plots: bool = False,
                             output_dir: Optional[Union[str, Path]] = None) -> Union[Tuple[np.ndarray, np.ndarray, dict], List[Tuple[np.ndarray, np.ndarray, dict, str]]]:
    """
    Process OSA data from either a single file or directory and optionally plot the results.
    
    This is a high-level function that combines loading, processing, and plotting
    functionality. It can handle both single files and directories of files.
    
    Parameters
    ----------
    data_path : Union[str, Path]
        Path to either a single OSA data file or directory containing OSA data files
    plot : bool, optional
        Whether to plot the spectra, by default True
    save_plots : bool, optional
        Whether to save the plots, by default False
    output_dir : Optional[Union[str, Path]], optional
        Directory to save plots if save_plots is True
        
    Returns
    -------
    Union[Tuple[np.ndarray, np.ndarray, dict], List[Tuple[np.ndarray, np.ndarray, dict, str]]]
        For single file: Tuple of (wavelengths, power, metadata)
        For directory: List of tuples containing (wavelengths, power, metadata, filename)
        
    Raises
    ------
    ValueError
        If the provided path does not exist
        
    Notes
    -----
    The function automatically detects whether the input is a file or directory
    and processes accordingly. For directories, each file is processed and plotted
    separately if plotting is enabled.
    """
    data_path = Path(data_path)
    
    if data_path.is_file():
        wavelengths, power, metadata = load_osa_data(data_path)
        
        if plot:
            plot_osa_spectrum(wavelengths, power, 
                            title=f"OSA Spectrum - {data_path.name}",
                            save_path=output_dir / f"{data_path.stem}_plot.png" if save_plots else None)
        
        return wavelengths, power, metadata
        
    elif data_path.is_dir():
        results = process_osa_directory(data_path)
        
        if plot:
            for wavelengths, power, metadata, filename in results:
                plot_osa_spectrum(wavelengths, power,
                                title=f"OSA Spectrum - {filename}",
                                save_path=output_dir / f"{Path(filename).stem}_plot.png" if save_plots else None)
        
        return results
    
    else:
        raise ValueError(f"Path {data_path} does not exist") 