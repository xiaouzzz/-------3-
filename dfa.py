class DFA:
    def __init__(self, states, alphabet, transition_function, start_state, accept_states):
        self.states = states
        self.alphabet = alphabet
        self.transition_function = transition_function
        self.start_state = start_state
        self.accept_states = accept_states
        self.current_state = start_state

    def reset(self):
        self.current_state = self.start_state

    def process_symbol(self, symbol):
        if symbol in self.alphabet:
            self.current_state = self.transition_function[self.current_state][symbol]
        else:
            raise ValueError(f"Symbol {symbol} not in alphabet")

    def process_string(self, input_string):
        self.reset()
        for symbol in input_string:
            self.process_symbol(symbol)
        return self.current_state in self.accept_states

# 定义 DFA
states = {'q0', 'q1'}
alphabet = {'a', 'b'}
transition_function = {
    'q0': {'a': 'q1', 'b': 'q0'},
    'q1': {'a': 'q1', 'b': 'q0'}
}
start_state = 'q0'
accept_states = {'q1'}

dfa = DFA(states, alphabet, transition_function, start_state, accept_states)

# 测试 DFA
input_string = "aba"
result = dfa.process_string(input_string)
print(f"Input string '{input_string}' is accepted by DFA: {result}")
