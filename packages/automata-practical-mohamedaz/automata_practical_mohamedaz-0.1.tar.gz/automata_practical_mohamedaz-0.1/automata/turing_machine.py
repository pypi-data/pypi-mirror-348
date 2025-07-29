

class TuringMachine:
    def __init__(self, input_string):
        self.tape = list(input_string)
        self.head = 0
        self.state = 'q0'
        self.accept_states = {'q0'}  

    def step(self):
        if self.head >= len(self.tape):
            return False  # نهاية الشريط

        symbol = self.tape[self.head]

        if symbol not in {'0', '1'}:
            raise ValueError(f"Invalid symbol on tape: {symbol}")

        if self.state == 'q0':
            if symbol == '0':
                self.state = 'q0'
            elif symbol == '1':
                self.state = 'q1'

        elif self.state == 'q1':
            if symbol == '0':
                self.state = 'q2'
            elif symbol == '1':
                self.state = 'q0'

        elif self.state == 'q2':
            if symbol == '0':
                self.state = 'q1'
            elif symbol == '1':
                self.state = 'q2'

        self.head += 1
        return True

    def run(self):
        while self.head < len(self.tape):
            self.step()
        return self.state in self.accept_states
