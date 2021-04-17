from q4 import get_failure_server_list, get_all_server_list, get_failure_switch_list

TEST_01_PATH = "surveillance_q4_01.csv"
TEST_02_PATH = "surveillance_q4_02.csv"
TEST_03_PATH = "surveillance_q4_03.csv"


# 以下故障のテスト(設問2と同じ)
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
    
# 以下スイッチの故障のテスト

def test_q4_01_01():
    expected = [
    ]
    N = 1
    failure_server_list = get_failure_server_list(TEST_01_PATH, N)
    all_server_list = get_all_server_list(TEST_01_PATH)
    assert expected == get_failure_switch_list(all_server_list, failure_server_list)

def test_q4_02_01():
    expected = [
        ["10.20", "20201019133125"]
    ]
    N = 1
    failure_server_list = get_failure_server_list(TEST_02_PATH, N)
    all_server_list = get_all_server_list(TEST_02_PATH)
    assert expected == get_failure_switch_list(all_server_list, failure_server_list)

def test_q4_02_02():
    expected = [
    ]
    N = 2
    failure_server_list = get_failure_server_list(TEST_02_PATH, N)
    all_server_list = get_all_server_list(TEST_02_PATH)
    assert expected == get_failure_switch_list(all_server_list, failure_server_list)

def test_q4_03_01():
    expected = [
    ]
    N = 1
    failure_server_list = get_failure_server_list(TEST_03_PATH, N)
    all_server_list = get_all_server_list(TEST_03_PATH)
    assert expected == get_failure_switch_list(all_server_list, failure_server_list)