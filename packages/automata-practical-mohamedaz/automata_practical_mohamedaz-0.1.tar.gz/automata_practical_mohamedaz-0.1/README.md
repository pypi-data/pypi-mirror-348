# Automata Practical Exam – Section 5

##  Student Info
- **Section Number:** 5  
- **Tasks Solved:**  
  1. DFA that accepts binary strings containing the substring `101`  
  2. Turing Machine that recognizes binary numbers divisible by 3  

---

## Project Structure

```text
automata_practical_exam_<4549>/
│
├── automata/                    #  Python package root
│   ├── __init__.py              # makes this a package
│   ├── dfa.py                   # DFA implementation
│   └── turing_machine.py        # Turing Machine implementation
│
├── tests/                       #  Unit tests
│   ├── test_dfa.py
│   └── test_turing_machine.py
│
├── README.md                    #  this file
└── setup.py                     #  package metadata


-------------------------------------------------
>>>Installation
# from project root
pip install -e .
Installs the package in “editable” mode so you can modify code and see changes immediately.

>>>Usage
1. Import and run the DFA
from automata.dfa import DFA

dfa = DFA()
print(dfa.accepts("010101"))   # True
print(dfa.accepts("0100"))     # False


------------------------------------------------

2. Import and run the Turing Machine
from automata.turing_machine import TuringMachine

tm = TuringMachine("110")      # binary 6
print(tm.run())                # True (6 divisible by 3)

tm2 = TuringMachine("101")     # binary 5
print(tm2.run())               # False (5 not divisible by 3)


------------------------------------------------
 >>>>>Running Tests
 pip install pytest
pytest tests/


Or run individual test files:
python -m pytest tests/test_dfa.py
python -m pytest tests/test_turing_machine.py
