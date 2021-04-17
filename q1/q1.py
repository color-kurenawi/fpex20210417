import csv
import time
import datetime

LOG_PATH = "surveillance.csv"

def get_failure_server_list(log_path):
    """
    ログのパスを入力に取り，故障しているサーバアドレスと故障が判明した時間のリストのリストを返す．
    Args:
        log_path (string): ログのパス
    Returns:
        failure_server_list (list):[
            [server address 1, detected time(YYYYMMDDhhmmss)],
            [server address 2, detected time],
            ...,
        ]
    """
    
    failure_server_set = set()
    failure_server_list = []
    
    with open(log_path) as f:
        reader = csv.reader(f)
        for line in reader:
            t, address, response = line
            if response == "-" and address not in failure_server_set:
                failure_server_set.add(address)
                failure_server_list.append([address, t])
    
    return failure_server_list

def time_parse(detected_time):
    year = int(detected_time[0:4])
    month = int(detected_time[4:6])
    day = int(detected_time[6:8])
    hour = int(detected_time[8:10])
    minute = int(detected_time[10:12])
    second = int(detected_time[12:14])
    
    parsed_dt = datetime.datetime(year=year, month=month, day=day, hour=hour, minute=minute, second=second)
    return parsed_dt

def get_elapsed_time(detected_time):
    dt_detected = time_parse(detected_time)
    dt_now = datetime.datetime.now()
    elapsed_time = dt_now - dt_detected
    return elapsed_time

def show_failure_server_list(failure_server_list):
    print("アドレス 故障してからの経過時間")
    for address, detected_time in failure_server_list:
        elapsed_time = get_elapsed_time(detected_time)
        print(address, elapsed_time)
    

def main():
    failure_server_list = get_failure_server_list(LOG_PATH)
    show_failure_server_list(failure_server_list)
    
if __name__ == "__main__":
    main()