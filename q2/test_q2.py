from q2 import get_failure_server_list

TEST_01_PATH = "surveillance_q2_01.csv"
TEST_02_PATH = "surveillance_q2_02.csv"
TEST_03_PATH = "surveillance_q2_03.csv"

def test_01_01():
    expected = [
        ["10.20.30.1/16", "20201019133324"]
    ]
    timeout_num = 1
    assert expected == get_failure_server_list(TEST_01_PATH, timeout_num)
    
def test_01_02():
    expected = [
    ]
    timeout_num = 2
    assert expected == get_failure_server_list(TEST_01_PATH, timeout_num)

def test_02_01():
    expected = [
        ["10.20.30.1/16", "20201019133124"],
        ["10.20.30.2/16", "20201019133125"]
    ]
    timeout_num = 1
    assert expected == get_failure_server_list(TEST_02_PATH, timeout_num)

def test_02_02():
    expected = [
        ["10.20.30.2/16", "20201019133225"],
    ]
    timeout_num = 2
    assert expected == get_failure_server_list(TEST_02_PATH, timeout_num)

def test_02_03():
    expected = [
    ]
    timeout_num = 3
    assert expected == get_failure_server_list(TEST_02_PATH, timeout_num)


def test_03_01():
    expected = [
    ]
    timeout_num = 1
    assert expected == get_failure_server_list(TEST_03_PATH, timeout_num)