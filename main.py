import collections
import tkinter as tk
from tkinter import scrolledtext

# 定义文法
grammar = {
    'S': ['bASB', 'bA'],
    'A': ['dSa', 'e'],
    'B': ['cAa', 'c']
}

# 计算FIRST集合
def compute_first_sets(grammar):
    first = collections.defaultdict(set)

    def first_of(symbol):
        if symbol in first:
            return first[symbol]
        if not symbol.isupper():
            return {symbol}
        result = set()
        for production in grammar[symbol]:
            if production == 'e':
                result.add('e')
            else:
                for char in production:
                    char_first = first_of(char)
                    result |= (char_first - {'e'})
                    if 'e' not in char_first:
                        break
                else:
                    result.add('e')
        first[symbol] = result
        return result

    for non_terminal in grammar:
        first_of(non_terminal)

    return first

# 计算FOLLOW集合
def compute_follow_sets(grammar, first_sets):
    follow = collections.defaultdict(set)
    follow['S'].add('$')

    while True:
        updated = False
        for non_terminal in grammar:
            for production in grammar[non_terminal]:
                trailer = follow[non_terminal].copy()
                for symbol in reversed(production):
                    if symbol.isupper():
                        if follow[symbol] != follow[symbol] | trailer:
                            follow[symbol] |= trailer
                            updated = True
                        if 'e' in first_sets[symbol]:
                            trailer |= (first_sets[symbol] - {'e'})
                        else:
                            trailer = first_sets[symbol]
                    else:
                        trailer = first_sets[symbol]
        if not updated:
            break

    return follow

# 项目集规范族和DFA
def closure(items):
    closure_set = set(items)
    while True:
        new_items = closure_set.copy()
        for item in closure_set:
            if '.' not in item[1]:
                continue
            dot_index = item[1].index('.')
            if dot_index == len(item[1]) - 1:
                continue
            next_symbol = item[1][dot_index + 1]
            if next_symbol.isupper():
                for production in grammar[next_symbol]:
                    new_items.add((next_symbol, '.' + production))
        if new_items == closure_set:
            break
        closure_set = new_items
    return closure_set

def goto(items, symbol):
    goto_set = set()
    for item in items:
        if '.' in item[1]:
            dot_index = item[1].index('.')
            if dot_index < len(item[1]) - 1 and item[1][dot_index + 1] == symbol:
                goto_set.add((item[0], item[1][:dot_index] + symbol + '.' + item[1][dot_index + 2:]))
    return closure(goto_set)

def items(grammar):
    initial_item = ('S\'', '.' + 'S')
    states = [closure({initial_item})]
    dfa = {}
    while True:
        new_states = states.copy()
        for state in states:
            for symbol in set(''.join(''.join(production) for production in grammar.values())) | {'$'}:
                goto_state = goto(state, symbol)
                if goto_state and goto_state not in states:
                    new_states.append(goto_state)
                    dfa[(tuple(state), symbol)] = goto_state
        if new_states == states:
            break
        states = new_states
    return states, dfa

# 构建SLR(1)分析表
def build_slr1_parsing_table(grammar, first_sets, follow_sets):
    states, dfa = items(grammar)
    action = collections.defaultdict(dict)
    goto_table = collections.defaultdict(dict)
    for i, state in enumerate(states):
        for item in state:
            if '.' in item[1]:
                dot_index = item[1].index('.')
                if dot_index == len(item[1]) - 1:
                    if item[0] == 'S\'':
                        action[i]['$'] = 'accept'
                    else:
                        for terminal in follow_sets[item[0]]:
                            action[i][terminal] = ('reduce', item[0] + '->' + item[1][:-1])
                else:
                    symbol = item[1][dot_index + 1]
                    if not symbol.isupper():
                        goto_state = dfa.get((tuple(state), symbol))
                        if goto_state:
                            action[i][symbol] = ('shift', states.index(goto_state))
            else:
                for terminal in follow_sets[item[0]]:
                    action[i][terminal] = ('reduce', item[0] + '->' + item[1][:-1])
        for symbol in grammar.keys():
            goto_state = dfa.get((tuple(state), symbol))
            if goto_state:
                goto_table[i][symbol] = states.index(goto_state)
    return action, goto_table

# GUI显示
def display_gui(first_sets, follow_sets, action, goto_table):
    root = tk.Tk()
    root.title("SLR(1)分析器结果")

    text_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=100, height=40)
    text_area.pack(pady=10, padx=10)

    def display_sets(name, sets):
        text_area.insert(tk.END, f"{name}集合:\n")
        for non_terminal, set_ in sets.items():
            text_area.insert(tk.END, f"{name}({non_terminal}) = {set_}\n")
        text_area.insert(tk.END, "\n")

    display_sets("FIRST", first_sets)
    display_sets("FOLLOW", follow_sets)

    text_area.insert(tk.END, "SLR(1)分析表:\n")
    text_area.insert(tk.END, "Action表:\n")
    for state, actions in action.items():
        text_area.insert(tk.END, f"状态 {state}:\n")
        for symbol, action in actions.items():
            text_area.insert(tk.END, f"  {symbol}: {action}\n")
    text_area.insert(tk.END, "\n")

    text_area.insert(tk.END, "Goto表:\n")
    for state, gotos in goto_table.items():
        text_area.insert(tk.END, f"状态 {state}:\n")
        for symbol, state_ in gotos.items():
            text_area.insert(tk.END, f"  {symbol}: {state_}\n")

    root.mainloop()

# 主程序
if __name__ == "__main__":
    first_sets = compute_first_sets(grammar)
    follow_sets = compute_follow_sets(grammar, first_sets)
    
    action, goto_table = build_slr1_parsing_table(grammar, first_sets, follow_sets)

    display_gui(first_sets, follow_sets, action, goto_table)
