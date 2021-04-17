from q3 import get_failure_server_list, get_busy_server_list

TEST_01_PATH = "surveillance_q3_01.csv"
TEST_02_PATH = "surveillance_q3_02.csv"
TEST_03_PATH = "surveillance_q3_03.csv"

# 以下サーバ故障のテスト(設問2と同じ)

def test_01_01():
    expected = [
        ["10.20.30.1/16", "20201019133324"]
    ]
    N = 1
    assert expected == get_failure_server_list(TEST_01_PATH, N)
    
def test_01_02():
    expected = [
    ]
    N = 2
    assert expected == get_failure_server_list(TEST_01_PATH, N)

def test_02_01():
    expected = [
        ["10.20.30.1/16", "20201019133124"],
        ["10.20.30.2/16", "20201019133125"]
    ]
    N = 1
    assert expected == get_failure_server_list(TEST_02_PATH, N)

def test_02_02():
    expected = [
        ["10.20.30.2/16", "20201019133225"],
    ]
    N = 2
    assert expected == get_failure_server_list(TEST_02_PATH, N)

def test_02_03():
    expected = [
    ]
    N = 3
    assert expected == get_failure_server_list(TEST_02_PATH, N)


def test_03_01():
    expected = [
    ]
    N = 1
    assert expected == get_failure_server_list(TEST_03_PATH, N)


# 以下過負荷のテスト

def test_q3_01_01():
    expected = [
        ["10.20.30.1/16", "20201019133224"]
    ]
    m = 1
    t = 100
    assert expected == get_busy_server_list(TEST_01_PATH, m, t)

def test_q3_01_02():
    expected = [
        ["10.20.30.1/16", "20201019133324"]
    ]
    m = 3
    t = 100
    assert expected == get_busy_server_list(TEST_01_PATH, m, t)

def test_q3_02_01():
    expected = [
        ["10.20.30.1/16", "20201019133224"],
        ["10.20.30.2/16", "20201019133225"]
    ]
    m = 2
    t = 100
    assert expected == get_busy_server_list(TEST_02_PATH, m, t)

def test_q3_02_02():
    expected = [
        ["10.20.30.1/16", "20201019133124"]
    ]
    m = 1
    t = 100
    assert expected == get_busy_server_list(TEST_02_PATH, m, t)

def test_q3_03_01():
    expected = [
    ]
    m = 3
    t = 300
    assert expected == get_busy_server_list(TEST_03_PATH, m, t)

def test_q3_03_02():
    expected = [
        ["10.20.30.1/16", "20201019133224"],
        ["192.168.1.2/24", "20201019133235"]
    ]
    m = 2
    t = 10
    assert expected == get_busy_server_list(TEST_03_PATH, m, t)