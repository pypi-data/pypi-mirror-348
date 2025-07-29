# test_tm_divisible_by_3.py

from automata.turing_machine import TuringMachine

def test_tm_divisibility():
    assert TuringMachine("0").run() == True
    assert TuringMachine("11").run() == True     # 3
    assert TuringMachine("110").run() == True    # 6
    assert TuringMachine("1001").run() == True   # 9
    assert TuringMachine("1010").run() == False  # 10
    assert TuringMachine("10").run() == False    # 2
    assert TuringMachine("111").run() == False   # 7
