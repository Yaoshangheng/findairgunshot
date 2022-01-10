import os
from obspy import UTCDateTime
import shutil
MIN_SECONDS = 0
MAX_SECONDS = 1
temp_root = '/home/yaoyuan/Desktop/myproject2_MESS/MESS/output/tmp/Templates'
out_dir = '/home/yaoyuan/Desktop/myproject2_MESS/MESS/output/tmp/Templates_new'
date_filename = '/home/yaoyuan/Desktop/myprogram/convertcltg2cutpha/airgunshot2014'
in_date_filename = '/home/yaoyuan/Desktop/myprogram/convertcltg2cutpha/ZDYhypoinv_2014.pha'
in_data_filename = '/home/yaoyuan/Desktop/myprogram/convertcltg2cutpha/phase_2014.dat'
out_filename = '/home/yaoyuan/Desktop/myprogram/convertcltg2cutpha/phase_2014airgun.dat'
date_list = []
in_data_dict = {}
def get_date_list():
    with open(date_filename, 'r') as f:
        for line in f:
            d = line.split(',')[0].strip()
            if len(d) > 0:
                date_list.append(UTCDateTime(d))
    date_file = open(in_date_filename, 'r')
    date_lines = date_file.readlines()
    date_file.close()
    with open(in_data_filename, 'r') as f:
        data_lines = f.readlines()
        i = 0
        while i < len(data_lines):
            if data_lines[i][0].isdigit():
                key = date_lines[i].split(',')[0] #取ZDYhypoinv_2014.pha里的日期像20140101192215.60
                block_lines = []
                #把ZDYhypoinv_2014.pha里的日期像20140101192215.60转换成2014-01-01T19:22:15.60Z
                first_line = str(UTCDateTime(key)) + "," + ','.join(data_lines[i].split(',')[1:])
                block_lines.append(first_line)
                i += 1
                while i < len(data_lines) and not data_lines[i][0].isdigit():
                    block_lines.append(data_lines[i])
                    i += 1
                in_data_dict[key] = ''.join(block_lines)
            else:
                i += 1
             
def is_match(dir_name):
    dir_date = UTCDateTime(dir_name)
    diff_seconds = [abs(d - dir_date) for d in date_list]
    min_diff = min(diff_seconds)
    return min_diff >= MIN_SECONDS and min_diff <= MAX_SECONDS

def get_dirnames():
    dirs = []
    for d in os.listdir(temp_root):
        if is_match(d):
            dirs.append(d)
    return dirs

def copy_data(dirs, out_file):
    if not os.path.isdir(out_dir):
        os.makedirs(out_dir)
    for d in dirs:
        try:
            out_file.write(in_data_dict[d])
        except:
            pass
        try:
            print('copy to', os.path.join(out_dir, d))
            shutil.copytree(os.path.join(temp_root, d), os.path.join(out_dir, d))
        except:
            pass
out_file = open(out_filename, 'w')
get_date_list()
dirs = get_dirnames()
copy_data(dirs, out_file)
out_file.close()

