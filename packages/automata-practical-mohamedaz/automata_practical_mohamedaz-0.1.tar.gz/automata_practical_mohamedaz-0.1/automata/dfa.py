# dfa.py

class DFA:
    def __init__(self):
        
        self.states = {"q0", "q1", "q2", "q3"}  
        self.start_state = "q0"
        self.accept_states = {"q3"}
        self.current_state = self.start_state

    def transition(self, state, symbol):
        
        if state == "q0":
            if symbol == "1":
                return "q1"
            elif symbol == "0":
                return "q0"

        elif state == "q1":
            if symbol == "0":
                return "q2"
            elif symbol == "1":
                return "q1"

        elif state == "q2":
            if symbol == "1":
                return "q3"
            elif symbol == "0":
                return "q0"

        elif state == "q3":
            
            return "q3"

        
        raise ValueError(f"Invalid state or symbol: {state}, {symbol}")

    def accepts(self, input_string):
        
        self.current_state = self.start_state

        for symbol in input_string:
            if symbol not in {"0", "1"}:
                raise ValueError(f"Invalid symbol: {symbol}")
            self.current_state = self.transition(self.current_state, symbol)

        return self.current_state in self.accept_states