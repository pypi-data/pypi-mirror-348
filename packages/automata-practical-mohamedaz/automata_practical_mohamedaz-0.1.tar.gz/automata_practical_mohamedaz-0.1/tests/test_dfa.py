# test_dfa.py

from  automata.dfa import DFA 

def test_dfa_accepts_101():
    dfa = DFA()
    assert dfa.accepts("101") == True
    assert dfa.accepts("0101") == True
    assert dfa.accepts("111101") == True
    assert dfa.accepts("1010") == True
    assert dfa.accepts("000") == False
    assert dfa.accepts("110") == False
    assert dfa.accepts("111111") == False
    assert dfa.accepts("1") == False
    assert dfa.accepts("10") == False
