from q1 import get_failure_server_list

TEST_01_PATH = "surveillance_q1_01.csv"
TEST_02_PATH = "surveillance_q1_02.csv"
TEST_03_PATH = "surveillance_q1_03.csv"

def test_01():
    expected = [
        ["10.20.30.1/16", "20201019133324"]
                ]
    assert expected == get_failure_server_list(TEST_01_PATH)

def test_02():
    expected = [
        ["10.20.30.2/16", "20201019133125"],
        ["10.20.30.1/16", "20201019133324"]
    ]
    
    assert expected == get_failure_server_list(TEST_02_PATH)

def test_03():
    expected = [
    ]
    
    assert expected == get_failure_server_list(TEST_03_PATH)