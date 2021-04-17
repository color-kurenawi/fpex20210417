import csv
import datetime
import argparse
from collections import defaultdict

LOG_PATH = "surveillance.csv"
LOG_PATH = "surveillance_q4_02.csv"

def get_all_server_list(log_path):
    all_server_set = set()
    with open(log_path) as f:
        reader = csv.reader(f)
        for line in reader:
            t, address, response = line
            all_server_set.add(address) 
    
    all_server_list = list(all_server_set)
    return all_server_list

def get_subnet(address):
    ipv4_address, prefix = address.split("/")
        
    prefix = int(prefix)
        
    subnet = ".".join(ipv4_address.split(".")[:prefix//8])
    
    return subnet

def get_all_subnet_list(all_server_list):
    all_subnet_set = set()
    
    for address in all_server_list:
        subnet = get_subnet(address)
        all_subnet_set.add(subnet)
    
    all_subnet_list = list(all_subnet_set)
    return all_subnet_list

def get_failure_server_list(log_path, N):
    """
    ログのパスを入力に取り，故障しているサーバアドレスと故障が判明した時間のリストのリストを返す．
    Args:
        log_path (string): ログのパス
        N (int):サーバの故障だとみなすpingの連続タイムアウト回数
    Returns:
        failure_server_list (list):[
            [server address 1, detected time(YYYYMMDDhhmmss)],
            [server address 2, detected time],
            ...,
        ]
    """
    
    failure_server_set = set()
    failure_server_dict = defaultdict(int)
    failure_server_list = []
    
    with open(log_path) as f:
        reader = csv.reader(f)
        for line in reader:
            t, address, response = line
            if response == "-":
                failure_server_dict[address] += 1
                if failure_server_dict[address] >= N and address not in failure_server_set:
                    failure_server_list.append([address, t])
                    failure_server_set.add(address)
            else:
                failure_server_dict[address] = 0
    
    return failure_server_list

def get_failure_switch_list(all_server_list, failure_server_list):
    """
    すべてのサーバーのアドレスのリストと，故障したサーバーのリストを元に，故障したスイッチを検出する．
    Args:
        all_server_list (list)): すべてのサーバーのアドレスのリスト
        failure_server_list (list): 故障したサーバーのアドレスのリスト

    Returns:
        list: 故障したスイッチのリスト
    """
    
    # サブネットのリスト
    all_subnet_list = get_all_subnet_list(all_server_list)
    
    # 各サブネットに属するすべてのアドレスの集合
    address_set_by_subnet = {subnet:set() for subnet in all_subnet_list}
    
    for address in all_server_list:
        subnet = get_subnet(address)
        address_set_by_subnet[subnet].add(address)
    
    # 各サブネットに属する故障したアドレスの集合
    failure_set_by_subnet = {subnet:set() for subnet in all_subnet_list}
    failure_switch_list = []
    
    for address, detected_time in failure_server_list:
        subnet = get_subnet(address)
        failure_set_by_subnet[subnet].add(address)
        
        # 各サブネットについて，故障したアドレス集合とすべてのアドレス集合が一致する場合
        if failure_set_by_subnet[subnet] == address_set_by_subnet[subnet]:
            failure_switch_list.append([subnet, detected_time])
    
    return failure_switch_list

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
        
def show_filure_switch_list(failure_switch_list):
    print("サブネット 故障してからの経過時間")
    for subnet, detected_time in failure_switch_list:
        elapsed_time = get_elapsed_time(detected_time)
        print(subnet, elapsed_time)

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--N", type=int, help="サーバの故障だとみなすpingの連続タイムアウト回数", default=1)
    args = parser.parse_args()
    return args

def main():
    args = get_args()
    failure_server_list = get_failure_server_list(LOG_PATH, args.N)
    show_failure_server_list(failure_server_list)
    
    all_server_list = get_all_server_list(LOG_PATH)
    failire_switch_list = get_failure_switch_list(all_server_list, failure_server_list)
    show_filure_switch_list(failire_switch_list)
    
if __name__ == "__main__":
    main()