import os
import re
import shutil
import time
from datetime import datetime, timedelta

def find_last_in_day(folder_path):
    # 获取文件夹下所有文件
    files = os.listdir(folder_path)
    
    # 筛选出符合格式的文件并排序
    pattern = re.compile(r'(\d{4})(\d{2})(\d{2})_(\d{2})(\d{2})(\d{2})\.png')
    file_list = []
    
    for file in files:
        match = pattern.match(file)
        if match:
            year, month, day, hour, minute, second = match.groups()
            file_datetime = datetime(int(year), int(month), int(day), int(hour), int(minute), int(second))
            file_list.append((file_datetime, os.path.join(folder_path, file)))
    
    # 按时间排序
    file_list.sort(key=lambda x: x[0])
    
    # 创建字典
    result = {}
    
    # 如果没有文件，返回空字典
    if not file_list:
        return result
    
    # 获取日期范围
    first_date = file_list[0][0].date()
    last_date = file_list[-1][0].date()
    
    # 遍历每一天
    current_date = first_date
    while current_date <= last_date:
        # 构造日期键
        date_key = current_date.strftime("%Y%m%d")
        
        # 构造当日+1天的时间点（即下一天的0点）
        next_day = current_date + timedelta(days=1)
        next_day_midnight = datetime(next_day.year, next_day.month, next_day.day)
        
        # 将current_date转换为datetime对象，以便与file_datetime比较
        current_datetime = datetime(current_date.year, current_date.month, current_date.day)

        # 寻找最接近下一天0点的文件（即当天最新的文件）
        closest_file = None
        min_diff = None

        for file_datetime, filepath in file_list:
            # 只考虑当天和下一天0点之前的文件
            if current_datetime <= file_datetime < next_day_midnight:
                diff = next_day_midnight - file_datetime
                if min_diff is None or diff < min_diff:
                    min_diff = diff
                    closest_file = filepath
        
        if closest_file:
            result[date_key] = closest_file
        
        # 移动到下一天
        current_date = next_day
    
    return result


def find_last_in_hours(folder_path):
    # 正则表达式匹配文件名格式
    pattern = re.compile(r'^(\d{8})_(\d{6})\.png$')

    # 读取文件夹下所有文件
    files = os.listdir(folder_path)
    
    # 筛选出符合格式的文件并排序
    valid_files = []
    for file in files:
        match = pattern.match(file)
        if match:
            date_str, time_str = match.groups()
            file_datetime = datetime.strptime(date_str + time_str, '%Y%m%d%H%M%S')
            file_path = os.path.join(folder_path, file)
            valid_files.append((file_datetime, file_path))

    valid_files.sort()  # 按时间排序

    # 创建字典并填入数据
    result_dict = {}
    if valid_files:
        current_date = valid_files[0][0].replace(minute=0, second=0, microsecond=0)
        end_date = valid_files[-1][0]

        while current_date <= end_date:
            # 寻找每个整点前最接近的文件
            closest_file = None
            for file_datetime, file_path in valid_files:
                if file_datetime <= current_date:
                    closest_file = file_path
                else:
                    break

            if closest_file:
                key = current_date.strftime('%Y%m%d_%H')
                result_dict[key] = closest_file

            # 增加一小时
            current_date += timedelta(hours=1)

    return result_dict

def find_last_one(folder_path, regex=None):
    # 正则表达式匹配文件名格式
    if regex is None:
        regex = r'^mask_all_(\d{8})_(\d{6})\.png$'
    pattern = re.compile(regex)

    # 读取文件夹下所有文件
    files = os.listdir(folder_path)

    # 筛选出符合格式的文件并排序
    valid_files = []
    for file in files:
        match = pattern.match(file)
        if match:
            date_str, time_str = match.groups()
            file_datetime = datetime.strptime(date_str + time_str, '%Y%m%d%H%M%S')
            file_path = os.path.join(folder_path, file)
            valid_files.append((file_datetime, file_path))

    valid_files.sort()  # 按时间排序

    # 返回最新的一个文件
    if valid_files:
        return valid_files[-1][1]
    else:
        return None

def find_color(folder_path, regex=None):
    # 正则表达式匹配文件名格式
    if regex is None:
        regex = r'^_mask_#(\d{2})*\.png$'
    pattern = re.compile(regex)

    # 读取文件夹下所有文件
    files = os.listdir(folder_path)

    # 筛选出符合格式的文件并排序
    valid_files = []
    for file in files:
        match = pattern.match(file)
        if match:
            file_path = os.path.join(folder_path, file)
            valid_files.append(file_path)

    # 返回最新的一个文件
    if valid_files:
        return valid_files
    else:
        return None

def copy_and_rename(filename, output_folder):
    if filename:
        basename = os.path.basename(filename)
        new_filename = 'mask_all.png'
        new_filepath = os.path.join(output_folder, new_filename)
        shutil.copy2(filename, new_filepath)
        print(f"Copied and renamed {filename} to {new_filepath}")
    else:
        print("No valid files found to copy.")

if __name__ == "__main__":
    # folder_path = 'timeline'

    # result = find_last_in_hours(folder_path)
    # print(result)

    # result = find_last_in_day(folder_path)
    # print(result)

    folder_path = 'timeline'
    result = find_last_one(folder_path, '^(\\d{8})_(\\d{6})\\.png$')
    print(f"Latest file: {result}")

    folder_path = 'timeline_cropped_png'
    result = find_last_one(folder_path, '^(\\d{8})_(\\d{6})\\.png$')
    print(f"Latest file in cropped folder: {result}")

    folder_path = 'timeline_color'
    result = find_last_one(folder_path, '^finish_all_(\\d{8})_(\\d{6})\\.png$')
    print(f"Latest file in color folder: {result}")
    result = find_last_one(folder_path, '^mask_all_(\\d{8})_(\\d{6})\\.png$')
    print(f"Latest mask_all file in color folder: {result}")
    result = find_last_one(folder_path, '^todo_all_(\\d{8})_(\\d{6})\\.png$')
    print(f"Latest todo_all file in color folder: {result}")
