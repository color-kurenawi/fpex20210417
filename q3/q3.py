import csv
import datetime
import argparse
from collections import defaultdict, deque

LOG_PATH = "surveillance.csv"
INF = 10**17

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

def get_busy_server_list(log_path, m, t):
    """
    ログファイルを入力とし，過負荷状態のサーバと過負荷になった時刻を返す関数．
    Args:
        log_path (string): ログのパス
        m (int):過負荷状態を判断するために参考にする直近の応答回数
        t (int):過負荷状態を判断する閾値となる平均応答時間(ミリ秒)
    Returns:
        busy_server_list (list):[
            [server address 1, detected time(YYYYMMDDhhmmss)],
            [server address 2, detected time],
            ...,
        ]
    """
    
    busy_server_dict = {}
    server_response_queue = {}
    
    with open(log_path) as f:
        reader = csv.reader(f)
        for line in reader:
            time, address, response = line
            
            # 過去のレスポンスはアドレスごとにキューで管理する．
            if address not in server_response_queue:
                server_response_queue[address] = deque()
            
            # タイムアウトになった場合はINF時間でレスポンスがあったとみなす
            if response == "-":
                response = INF
            
            # キューにレスポンスを追加
            response = int(response)
            server_response_queue[address].append(response)
            
            # キューがmより多くなると古いレスポンスを捨てる．
            if len(server_response_queue[address]) > m:
                server_response_queue[address].popleft()
            
            # キューがちょうどm個の場合に過負荷かどうか判定する．
            if len(server_response_queue[address]) == m:
                average_response = sum(server_response_queue[address]) / m
                
                # 新しく過負荷になった場合
                if average_response >= t and address not in busy_server_dict:
                    busy_server_dict[address] = time
                # 過負荷ではなくなった場合
                if average_response < t and address in busy_server_dict:
                    del busy_server_dict[address]
    print(server_response_queue["10.20.30.1/16"])
    busy_server_list =  [[address, detected_time] for address, detected_time in busy_server_dict.items()]
    
    # 過負荷になった時間が早い順にソートする．
    busy_server_list.sort(key=lambda x:x[1])
    
    return busy_server_list

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

def show_busy_server_list(busy_server_list, failure_server_list):
    """
    過負荷状態にあるサーバーのリストを出力する．ただし，故障中のサーバーは出力しない．
    """
    
    # 有無判定の高速化のため集合型に変換しておく
    failure_server_set = set(address for address, detected_time in failure_server_list)
    
    print("アドレス 過負荷になってからの経過時間")
    for address, detected_time in busy_server_list:
        if address not in failure_server_set:
            elapsed_time = get_elapsed_time(detected_time)
            print(address, elapsed_time)

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--N", type=int, help="サーバの故障だとみなすpingの連続タイムアウト回数", default=1)
    parser.add_argument("--m", type=int, help="過負荷状態を判断するために参考にする直近の応答回数", default=1)
    parser.add_argument("--t", type=int, help="過負荷状態を判断する閾値となる平均応答時間(ミリ秒)", default=100)
    args = parser.parse_args()
    return args

def main():
    args = get_args()
    
    failure_server_list = get_failure_server_list(LOG_PATH, args.N)
    show_failure_server_list(failure_server_list)
    
    busy_server_list = get_busy_server_list(LOG_PATH, args.m, args.t)
    show_busy_server_list(busy_server_list, failure_server_list)
if __name__ == "__main__":
    main()