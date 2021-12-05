import json
import logging
import numpy as np
import math
import matplotlib.pyplot as plt
import scipy.signal as signal
from statistics import mean


def read_file(filename):
    """Read the cvs file as list.

    Args:
        filename(str): name of the input file with ECG data


    Returns:
        lines(list): a long list containing all data without
        white spaces
    """
    # filename = 'data/' + 'test_data' + str(filename) + ".csv"
    with open(filename) as f:
        lines = f.readlines()
        lines = [line.rstrip() for line in lines]
    return lines


def parse(lines):
    """Separate the input list into two lists containing
    time and voltage values.

    Args:
        lines(list): a long list containing all data without
        white spaces


    Returns:
        time(numpyarray): an array contains the time values
        voltage(numpyarray): an array contains the voltage values
    """
    time = []
    voltage = []

    for i in range(len(lines)):
        line = lines[i].split(',')
        try:
            time.append(float(line[0]))
            voltage.append(float(line[1]))
            if math.isnan(float(line[0])) is True \
                    or math.isnan(float(line[1])) is True:
                logging.error("Encountered bad data, \
                                skip to the next data pair")
                time.pop()
                voltage.pop()

        except ValueError:
            logging.error("Encountered bad data, skip to the next data pair")

        if len(time) > len(voltage):
            time.pop()
        elif len(time) < len(voltage):
            voltage.pop()

    time = np.array(time)
    voltage = np.array(voltage)
    return time, voltage


def warn(v):
    """ Logging a warning.

    Args:
        v(numpyarray): an array contains the voltage values
    """
    maximum = max(v)
    minimum = min(v)
    if maximum > 300 or minimum < -300:
        logging.warning("The voltage in test_data" + str(num) +
                        ".csv is out of normal range -300~300mV.")


def sample_rate(time):
    """ Calculating the sampling rate for reference.

    Args:
        time(numpyarray): an array contains the time values


    Returns:
        fs(float): sampling rate of input test data
    """
    diff = []
    for i in range(len(time) - 1):
        a = time[i + 1] - time[i]
        diff.append(a)
    fs = 1 / mean(diff)
    return fs


def filter(voltage, fs, low, high):
    """ Creating a bandpass filter with specific filtering range.

    Args:
        voltage(numpyarray): an array contains the voltage values
        fs(float): sampling rate of input test data
        low(float): low limit of filtering frequency
        high(float): high limit of filtering frequency


    Returns:
        filtered_v(numpyarray): an array of filtered voltage
        smooth(numpyarray): an array of smoothed voltage
    """
    b, a = signal.butter(6, [low, high], 'bandpass', fs=fs)
    filtered_v = signal.lfilter(b, a, voltage)
    smooth = signal.cspline1d(filtered_v, 100)
    return filtered_v, smooth


def find(f_v, smooth):
    """ Finding the peaks of assigned voltage data.

    Args:
        f_v(numpyarray): an array of filtered voltage
        smooth(numpyarray): an array of smoothed voltage


    Returns:
        peaks2(list): a list of index in filtered voltage that peaks occur.
        peaks3(list): a list of index in smoothed voltage that peaks occur.
    """
    thre2 = max(f_v) * 0.6
    peaks2, _2 = signal.find_peaks(f_v, height=thre2, distance=50)
    thre2 = np.partition(f_v[peaks2].flatten(), -2)[-6] * 0.6
    peaks2, _2 = signal.find_peaks(f_v, height=thre2, distance=50)

    thre3 = max(smooth) * 0.6
    peaks3, _3 = signal.find_peaks(smooth, height=thre3, distance=50)
    thre3 = np.partition(smooth[peaks3].flatten(), -2)[-6] * 0.6
    peaks3, _3 = signal.find_peaks(smooth, height=thre3, distance=50)

    logging.info("Finding peaks in filtered and smooth voltage curve.")
    return peaks2, peaks3


def assign(time, smooth, peaks):
    """A dictionary is generated with assign values from calculations.

    Args:
        time(numpyarray): an array contains the time values
        smooth(numpyarray): an array of smoothed voltage
        peaks(list): a list of index in smoothed voltage that peaks occur.


    Returns:
        m(dictionary): a dictionary with information of the ECG
    """
    m = {}
    logging.info("Calculating the duration.")
    m["duration"] = time[-1] - time[0]
    logging.info("Calculating the voltage extremes.")
    m["voltage_extremes"] = [min(smooth), max(smooth)]
    logging.info("Counting the number of beats in the ECG strip.")
    m["num_beats"] = int(len(peaks))
    logging.info("Calculating the average beats per minute (bpm).")
    m["mean_hr_bpm"] = round(m["num_beats"] / m["duration"] * 60, 2)
    logging.info("Finding the time that beats occur.")
    pps = time[peaks]
    pps = np.ndarray.tolist(pps)
    m["beats"] = pps
    return m


def plot(num, time, voltage, f_v, smooth, peaks2, peaks3):
    """Plot the original, filtered, and smoothed voltage data with
        peaks marked

    Args:
        num(int): number of test data file
        time(numpyarray): an array contains the time values
        voltage(numpyarray): an array contains the voltage values
        f_v(numpyarray): an array of filtered voltage
        smooth(numpyarray): an array of smoothed voltage
        peaks2(list): a list of index in filtered voltage that peaks occur.
        peaks3(list): a list of index in smoothed voltage that peaks occur.
    """
    plt.subplot(3, 1, 1)
    plt.plot(time, voltage, 'b')
    plt.title("test data ")

    plt.subplot(3, 1, 2)
    plt.plot(time, f_v, 'g')
    plt.plot(time[peaks2], f_v[peaks2], 'x')
    plt.legend(['filtered', 'filtered peaks'])

    plt.subplot(3, 1, 3)
    plt.plot(time, smooth, 'r')
    plt.plot(time[peaks3], smooth[peaks3], 'o')
    plt.legend(['smooth', 'smooth peaks'])
    plt.savefig('image/new_image.jpg')
    # plt.show()

    logging.info("Plots with original, filtered, smooth voltage data,\
                    peaks are marked.")


def json_write(met, num):
    """Write json files with names corresponding to test data filename.

    Args:
        met(dictionary): a dictionary with information of the ECG
        num: num(int): number of test data file
    """
    filename = num + ".json"
    output = open(filename, 'w')
    json.dump(met, output)
    output.close()


def log(num):
    """Start a logging file with names corresponding to test data filename.

    Args:
        num: num(int): number of test data file
    """
    num = str(num)
    log_name = "test_data" + num + ".log"
    logging.basicConfig(filename=log_name, filemode="w", level=logging.INFO)
    logging.info("Start analyzing test_data" + num)
    logging.info("Generating data list for analysis")


def plot_data(filename):
    # log(num)
    input_lines = read_file(filename)
    t, v = parse(input_lines)
    try:
        low = 1
        high = 50
        f_v, smooth = filter(v, sample_rate(t), low, high)
        peaks2, peaks3 = find(f_v, smooth)
        # warn(smooth)
        metrics = assign(t, smooth, peaks3)
        # json_write(metrics, filename)
        plot(filename, t, v, f_v, smooth, peaks2, peaks3)
        return metrics['mean_hr_bpm']

    except IndexError:
        low = 1.5
        high = 100
        f_v, smooth = filter(v, sample_rate(t), low, high)
        peaks2, peaks3 = find(f_v, smooth)
        # warn(smooth)
        metrics = assign(t, smooth, peaks3)
        # json_write(metrics, num)
        plot(filename, t, v, f_v, smooth, peaks2, peaks3)

        return metrics['mean_hr_bpm']