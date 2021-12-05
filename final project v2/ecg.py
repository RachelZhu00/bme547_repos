import math
import logging
import heartpy as hp
import json


def is_num(string):
    '''
    This function demonstrate if the string include
    ' ', and if the character in the string is not numeric, '.'
    ,or negetive, this string will return False.
    :param string: string in the list
    :return: bool
    '''
    if string == '':
        return False
    for character in string:
        if (not character.isnumeric()) and \
                character != '.' and character != '-':
            return False
    return True


def input_data(filename):
    with open(filename, 'r') as in_file:
        in_lines = in_file.readlines()
    return in_lines


def parse_data(in_line):
    '''
    In this function, the numbers from the
    list are seperated by ',', if there are any
    data miss, the function will transfer it as 'nan'.
    All the number will be modified as float.

    :param in_line: each line from the input file
    :return: list_float
    '''
    list_no_return = in_line.strip('\n')
    list_split = list_no_return.split(',')
    if (not is_num(list_split[0])) or (not is_num(list_split[1])):
        return [math.nan, math.nan]
    list_float = [float(x) for x in list_split]
    return list_float


def parse_list(a1):
    '''
    Open two lists for time and voltage.
    take out all the string from the list and put
    them into the new lists, with seperated by ','.
    :param a1: list of string, number
    :return: l_time, l_voltage
    '''
    l_time = []
    l_voltage = []
    for i in a1:
        b1 = parse_data(i)
        if math.isnan(b1[0]) or math.isnan(b1[1]):
            logging.error('nan happen')
            continue
        l_time.append(b1[0])
        l_voltage.append(b1[1])
    return l_time, l_voltage


def merge_peak(peak_list):
    '''
    if the two peak list are too close(<50),
    this function will put them into a single
    list, the new list a will contain the previous
    closing list b together.
    :param peak_list: peak_list
    :return: list group "a" for two close peak lists.
    '''
    i = 0
    a = []
    while (i < len(peak_list)):
        b = [peak_list[i]]
        j = i + 1
        while (j < len(peak_list)):
            if peak_list[j] - peak_list[i] < 50:
                b.append(peak_list[j])
                j += 1
            else:
                break
        i = j
        a.append(b)
    return a


def find_peak(a, l_voltage):
    '''
    the start max_vol is negetive infinite,
    if the function search a larger number,
    then record it as max_vol until finding
    the max voltage in the whole list.
    :param a: time
    :param l_voltage: voltage
    :return:peak
    '''
    peaks = []
    for i in a:
        max_vol = -999999
        peak = -1
        for point in i:
            if l_voltage[point] > max_vol:
                max_vol = l_voltage[point]
                peak = point
        peaks.append(peak)
    return peaks


def calculate_values(l_time, l_voltage, peaks):
    '''
    This function used to calculate the five variables
    in each files.
    duration: time duration of the ECG strip as a numeric value
    voltage_extremes: tuple in the form (min, max)
     where min and max are the minimum and maximum
    lead voltages found in the data file. min and max should be numeric values.
    num_beats: number of detected beats in the strip,
    as a numeric value
    mean_hr_bpm: estimated average heart rate over
    the length of the strip as a numeric value
    beats: list of times when a beat occurred.
    The individual times should be numeric values.
    Then, each value will be log in log info file.
    All five values is set into each file's dictionary.
    :param l_time: second
    :param l_voltage: voltage
    :param peaks: times
    :return: dic
    '''
    duration = l_time[-1] - l_time[0]
    logging.info('calculate duration')
    voltage_extremes = (min(l_voltage), max(l_voltage))
    logging.info('calculate voltage extremes')
    if voltage_extremes[1] - voltage_extremes[0] > 300:
        logging.warning('died')
    num_beats = len(peaks)
    logging.info('calculate num_beats')
    mean_hr_bpm = 60 / ((l_time[peaks[-1]]
                         - l_time[peaks[0]]) / (num_beats - 1))
    logging.info('calculate mean_hr_bpm')
    beats = []
    for peak in peaks:
        beats.append(l_time[peak])
    dic = {'duration': duration, 'voltage_extremes': voltage_extremes,
           'num_beats': num_beats, 'mean_hr_bpm': mean_hr_bpm,
           'beats': beats}
    return dic


def create_json(filename, dic):
    '''
    create the json file from the dictionary
    :return: json file
    '''
    out_file_name = filename.split('.')[0] + '.json'
    out_file = open(out_file_name, "w")
    json.dump(dic, out_file)
    out_file.close()


def config_logging(filename):
    filepath = 'test_data/' + filename
    name = filename.split('.')[0]
    print(filename)


def get_bpm(filename):
    a1 = input_data(filename)
    logging.info('new_ECG' + filename)

    l_time, l_voltage = parse_list(a1)

    SR = sample_rate = 10000 / l_time[-1]
    peak_list = hp.process(l_voltage, SR)[0]['peaklist']

    a = merge_peak(peak_list)
    peaks = find_peak(a, l_voltage)

    dic = calculate_values(l_time, l_voltage, peaks)
    return dic['mean_hr_bpm']


def fun(filename):
    '''
    invoking the previous functions for one single file.
    log all the info into a single log file.
    use heartpy to decrease the noise from the data
    in order to form a visible ECG graph for system to detect
    and analyze.
    :param filename: number of file
    :return: json file
    '''
    a1 = input_data(filename)
    logging.info('new_ECG' + filename)

    l_time, l_voltage = parse_list(a1)

    SR = sample_rate = 10000 / l_time[-1]
    peak_list = hp.process(l_voltage, SR)[0]['peaklist']

    a = merge_peak(peak_list)
    peaks = find_peak(a, l_voltage)
    print(len(peaks))

    dic = calculate_values(l_time, l_voltage, peaks)
    create_json(filename, dic)


def main():
    logging.basicConfig(filename='ECG_LOGGING.log',
                        filemode="w", level=logging.INFO)
    test_files = ["test_data1.csv"]
    for test_file in test_files:
        fun(test_file)


if __name__ == "__main__":
    main()
