"""
Relative Intensity Noise (RIN) Analysis Module

This module provides comprehensive tools for analyzing Relative Intensity Noise (RIN) in optical systems.
Key features include:
- Calibration of optical-to-electrical conversion
- Processing of RIN measurements from ESA (Electrical Spectrum Analyzer) data
- Calculation of single RIN values and statistical analysis
- Visualization of RIN spectra with background comparison
- Conversion utilities between linear and dB scales

The module handles both single measurements and batch processing of multiple RIN measurements,
including background subtraction and proper RBW (Resolution Bandwidth) correction.
"""

import os
from typing import List, Tuple, Union, Optional
import numpy as np
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt



def calibrate_conversion(power_uW: np.ndarray, voltage_mV: np.ndarray) -> float:
    """
    Perform calibration using power and voltage measurements.
    
    This function performs a linear fit to determine the conversion factor
    between optical power and electrical voltage measurements.
    
    Parameters
    ----------
    power_uW : np.ndarray
        Array of optical power measurements in µW
    voltage_mV : np.ndarray
        Array of corresponding voltage measurements in mV
        
    Returns
    -------
    float
        Conversion factor in V/µW
        
    Notes
    -----
    Uses scipy's curve_fit to perform a linear fit with zero intercept.
    The conversion factor represents the slope of the linear relationship
    between optical power and electrical voltage.
    """
    def lin_func(x: np.ndarray, a: float) -> np.ndarray:
        """Linear function for curve fitting."""
        return x * a
        
    popt, _ = curve_fit(lin_func, power_uW, voltage_mV)
    return popt[0]


def convert_optical_to_electrical(
    power: float,
    conversion_factor: float,
    impedance: float = 50,
    ret_V: bool = False
) -> float:
    """
    Convert optical power to electrical power or voltage.
    
    This function converts optical power measurements to either electrical
    power (in dBm) or voltage (in V) using a calibration factor.
    
    Parameters
    ----------
    power : float
        Optical power in µW
    conversion_factor : float
        Conversion factor (V/µW)
    impedance : float, optional
        Electrical impedance in Ohms, by default 50.0
    ret_V : bool, optional
        If True, return voltage instead of power, by default False
        
    Returns
    -------
    float
        Electrical power in dBm or voltage in V depending on ret_V parameter
        
    Notes
    -----
    The conversion assumes a linear relationship between optical power
    and electrical voltage, with the given conversion factor.
    """
    volts = conversion_factor * power  # V
    
    if ret_V:
        return volts
        
    elec_power = volts ** 2 / impedance  # W/Hz
    elec_power_mW = 1e3 * elec_power  # mW/Hz
    return 10 * np.log10(elec_power_mW)  # dBm

# --- File and data utilities ---
def get_paths_intensity(directory: str) -> List[str]:
    """
    Get paths to all ESA files in directory.
    
    Parameters
    ----------
    directory : str
        Directory path to search for ESA files
        
    Returns
    -------
    List[str]
        List of full paths to all .esa.txt files in the directory
        
    Notes
    -----
    Only files ending with 'esa.txt' are included in the results.
    """
    filenames = os.listdir(directory)
    return [os.path.join(directory, e) for e in filenames if e.endswith("esa.txt")]


def get_data(path: str, length: int = 1) -> Tuple[np.ndarray, np.ndarray]:
    """
    Load data from file, skipping header rows.
    
    Parameters
    ----------
    path : str
        Path to the data file
    length : int, optional
        Number of header rows to skip, by default 1
        
    Returns
    -------
    Tuple[np.ndarray, np.ndarray]
        Tuple containing:
        - xs : np.ndarray
            Array of x-values (typically frequency)
        - ys : np.ndarray
            Array of y-values (typically power)
            
    Notes
    -----
    The function assumes space-delimited data after the header.
    """
    return np.loadtxt(path, encoding="unicode_escape", skiprows=1, delimiter=' ')


def get_header(path: str, length: int = 1) -> List[List[str]]:
    """
    Read header lines from file.
    
    Parameters
    ----------
    path : str
        Path to the file
    length : int, optional
        Number of header lines to read, by default 1
        
    Returns
    -------
    List[List[str]]
        List of header lines, each split into a list of strings
        
    Notes
    -----
    The function uses ISO-8859-1 encoding to handle special characters.
    """
    lines = []
    with open(path, encoding="ISO-8859-1") as file:
        for _ in range(length):
            line = file.readline()
            lines.append(line[1:].split(','))
    return lines


def parse_rbw(rbw_str: str) -> float:
    """
    Parse RBW string to float value in Hz.
    
    Parameters
    ----------
    rbw_str : str
        Resolution bandwidth string (e.g., 'RBW 1MHz' or 'RBW 10kHz')
        
    Returns
    -------
    float
        Resolution bandwidth in Hz
        
    Notes
    -----
    Supports MHz and kHz units. The input string should start with 'RBW '.
    """
    if 'MHz' in rbw_str:
        return float(rbw_str[4:-3]) * 1e6
    elif 'kHz' in rbw_str:
        return float(rbw_str[4:-3]) * 1e3
    return float(rbw_str[4:-2])


def esa_header_data(header: List[List[str]]) -> Tuple[float, float, str, str, float]:
    """
    Extract data from ESA header.
    
    Parameters
    ----------
    header : List[List[str]]
        List of header lines, each split into a list of strings
        
    Returns
    -------
    Tuple[float, float, str, str, float]
        Tuple containing:
        - output_power : float
            Output power value
        - fb_level : float
            Feedback level value
        - gain : str
            Gain setting
        - pol : str
            Polarization state
        - rbw : float
            Resolution bandwidth in Hz
            
    Notes
    -----
    Handles different header formats and normalizes polarization values.
    """
    header_line = header[0]
    output_power = float(header_line[0].split(" ")[1][:-2])
    fb_level = float(header_line[1].split(" ")[3][:-2])
    
    # Handle different header formats
    if len(header_line) == 6:
        gain = header_line[2][1:]
        pol = header_line[3].split(" ")[2]
        rbw = parse_rbw(header_line[4].split(" ")[1])
    else:  # len == 5
        pol = header_line[2].split(" ")[2]
        rbw = parse_rbw(header_line[3].split(" ")[1])
        gain = 'None'
    
    # Normalize polarization values
    pol = pol.lower() if pol in ['Misaligned', 'Aligned', 'None'] else pol
    
    return output_power, fb_level, gain, pol, rbw


# --- Math and conversion utilities ---
def ratio_to_db(feedback_power: float, output_power: float, min_power: float = 0.000003) -> float:
    """
    Convert power ratio to dB.
    
    Parameters
    ----------
    feedback_power : float
        Feedback power value
    output_power : float
        Output power value
    min_power : float, optional
        Minimum power value to avoid log(0), by default 0.000003
        
    Returns
    -------
    float
        Power ratio in dB
        
    Notes
    -----
    Uses a minimum power value to avoid taking log of zero.
    """
    feedback_power = max(feedback_power, min_power)
    output_power = max(output_power, min_power)
    return 10 * np.log10(feedback_power / output_power)


def linear_to_dB(datapoint_linear: Union[float, np.ndarray]) -> Union[float, np.ndarray]:
    """
    Convert linear power to dB.
    
    Parameters
    ----------
    datapoint_linear : Union[float, np.ndarray]
        Power value(s) in linear scale
        
    Returns
    -------
    Union[float, np.ndarray]
        Power value(s) in dB scale
        
    Notes
    -----
    Uses the formula: dB = 10 * log10(power)
    """
    return 10 * np.log10(datapoint_linear)


def dB_to_linear(power: Union[float, np.ndarray]) -> Union[float, np.ndarray]:
    """
    Convert dB to linear power.
    
    Parameters
    ----------
    power : Union[float, np.ndarray]
        Power value(s) in dB scale
        
    Returns
    -------
    Union[float, np.ndarray]
        Power value(s) in linear scale
        
    Notes
    -----
    Uses the formula: linear = 10^(dB/10)
    """
    return 10 ** (power / 10)


def scientific(x: float, pos: int) -> str:
    """
    Format number in scientific notation for plotting.
    
    Parameters
    ----------
    x : float
        Number to format
    pos : int
        Position parameter (required by matplotlib formatter)
        
    Returns
    -------
    str
        Formatted string in LaTeX scientific notation
        
    Notes
    -----
    Special cases for common powers of 10 (1e5, 1e6, 1e7) are handled separately.
    """
    if x == 1e5:
        return r'$10^5$'
    elif x == 1e6:
        return r'$10^6$'
    elif x == 1e7:
        return r'$10^7$'
    else:
        return r'$%d \\times 10^{%d}$' % (
            int(x / (10 ** int(np.log10(x)))),
            int(np.log10(x))
        ) 
    

def process_intensity_data(
    path: str, 
    conversion_factor: float,
    power: Optional[float] = None, 
) -> Tuple[np.ndarray, np.ndarray]:
    """
    Process intensity data from a single file, applying RBW correction and conversion.
    
    Parameters
    ----------
    path : str
        Path to the data file
    conversion_factor : float
        Conversion factor for optical to electrical conversion
    power : Optional[float], optional
        Optional power value to override the one from header
        
    Returns
    -------
    Tuple[np.ndarray, np.ndarray]
        Tuple containing:
        - xs : np.ndarray
            Array of frequency values
        - ys : np.ndarray
            Array of processed RIN values
        - rbw : float
            Resolution bandwidth used
            
    Notes
    -----
    Applies RBW correction and optical-to-electrical conversion.
    Uses provided power for background measurements or header power otherwise.
    """
    header = get_header(path, length=1)
    header_power, fb_level, gain, pol, rbw = esa_header_data(header)
    
    # Use provided power for background or header power if not provided
    power = power if power is not None else header_power
    
    # Get raw data
    xs, ys = get_data(path)  # Hz, dBm
    
    # Apply RBW correction
    rbw_db = 10 * np.log10(rbw)  # Hz
    ys += -rbw_db  # dBm/Hz - Remove raw data dependence on bandwidth
    
    # Apply conversion. For background input power is used, everything else is header power
    conversion_factor_V = conversion_factor *1e-3 #conversion factor in V/µW
    # voltage_mV = conversion_factor_V * power
    ys += -convert_optical_to_electrical(power, conversion_factor=conversion_factor_V)
    
    return xs, ys, rbw

def calculate_single_RIN(xs: np.ndarray, ys: np.ndarray, start_idx: int = 10) -> float:
    """
    Calculate single RIN value from frequency and RIN data.
    
    Parameters
    ----------
    xs : np.ndarray
        Frequency array
    ys : np.ndarray
        RIN values array
    start_idx : int, optional
        Index to start integration from, by default 10
        
    Returns
    -------
    float
        Single RIN value in dB
        
    Notes
    -----
    Integrates the RIN spectrum from start_idx to the end.
    """
    diff = xs[1] - xs[0]
    return linear_to_dB(sum(dB_to_linear(ys[start_idx:])) * diff)

def plot_RIN_data(xs_list: List[np.ndarray], ys_list: List[np.ndarray], rbw: float,
                 background_idx: Optional[int] = None) -> None:
    """
    Plot RIN data with proper formatting.
    
    Parameters
    ----------
    xs_list : List[np.ndarray]
        List of frequency arrays
    ys_list : List[np.ndarray]
        List of RIN value arrays
    rbw : float
        Resolution bandwidth for x-axis limit
    background_idx : Optional[int], optional
        Index of background measurement in the lists
        
    Notes
    -----
    Creates two plots if background_idx is provided:
    1. Main plot with all measurements
    2. Background comparison plot
    """
    
    # Main plot
    plt.figure(0)
    
    for i, (xs, ys) in enumerate(zip(xs_list, ys_list)):

        if i == background_idx:
            plt.plot(xs, ys, alpha=0.5, label='Background')
        else:
            plt.plot(xs, ys, alpha=0.5, label=f'RIN{i}')
    
    indices= [xs > rbw]
    minima = [min(ys[indices[0]]) for ys in ys_list if min(ys[indices[0]]) != np.Inf]
    
    maxima = [max(ys[indices[0]]) for ys in ys_list if max(ys[indices[0]]) != np.Inf]

    print(minima,maxima)


    plt.xlabel('Frequency [Hz]')
    plt.xscale('log')
    plt.grid()
    plt.xlim(left=rbw,right=xs[-1])
    plt.ylim([min(minima)-5, max(maxima)+5])
    plt.legend()
    plt.ylabel('RIN [dBc/Hz]')
    
    # Background comparison plot
    if background_idx is not None:
        plt.figure(1)
        plt.plot(xs_list[background_idx], ys_list[background_idx], color='#e41a1c',label='Background')
        plt.xlabel('Frequency [Hz]')
        plt.xscale('log')
        plt.grid()
        plt.ylabel('RIN [dBc/Hz]')
        plt.legend(loc=(0.5525, 0.405), handletextpad=0.3, handlelength=0.95, fontsize=14)

def get_RIN_data(
    directory: str, 
    conversion_factor: float,
    background_identifier: str = '2025-04-30_17-53-11-876395esa',
    background_power: float = 580, # µW 
    plot: bool = True,
    start_idx: Optional[int] = 10
) -> Tuple[List[float], List[float], List[float]]:
    """
    Process and get RIN data from a directory.
    
    Parameters
    ----------
    directory : str
        Directory containing the data files
    conversion_factor : float
        Conversion factor for optical to electrical conversion
    background_identifier : str, optional
        String to identify background measurement files
    background_power : float, optional
        Optical power value in µW to use for background measurement
    plot : bool, optional
        Whether to plot the data
    start_idx : Optional[int], optional
        Index to start integration from
        
    Returns
    -------
    Tuple[List[float], List[float], List[float]]
        Tuple containing:
        - xs_list : List[float]
            List of frequency arrays
        - ys_list : List[float]
            List of RIN value arrays
        - single_RIN_values : List[float]
            List of calculated single RIN values
            
    Notes
    -----
    Processes all ESA files in the directory, handling background measurements
    separately. Optionally plots the results.
    """
    paths = get_paths_intensity(directory)
    print(paths)
    
    # Process all data
    xs_list = []
    ys_list = []
    single_RIN_values = []
    
    for path in paths:
        # Check if this is the background measurement
        is_background = background_identifier in path
        power = background_power if is_background else None #The process intensity data function will use the header power for non-background measurements
        
        xs, ys, rbw = process_intensity_data(
            path, 
            conversion_factor=conversion_factor,
            power=power)

        xs_list.append(xs)
        ys_list.append(ys)
        
        # Calculate single RIN value
        single_RIN = calculate_single_RIN(xs, ys, start_idx=start_idx)
        single_RIN_values.append(single_RIN)
    
    # Plot the data
    if plot:
        background_idx = next((i for i, path in enumerate(paths) 
                            if background_identifier in path), None)
        plot_RIN_data(xs_list, ys_list, rbw, background_idx)
    
    return xs_list, ys_list, single_RIN_values