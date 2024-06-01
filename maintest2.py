import collections
import tkinter as tk
from tkinter import scrolledtext

# 解析用户输入的文法
def parse_grammar(input_text):
    grammar = collections.defaultdict(list)
    lines = input_text.strip().split('\n')
    for line in lines:
        if '->' in line:
            lhs, rhs = line.split('->')
            lhs = lhs.strip()
            productions = rhs.split('|')
            for production in productions:
                grammar[lhs].append(production.strip())
    return grammar

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
    follow[list(grammar.keys())[0]].add('$')  # 假定第一个非终结符是开始符号

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
def closure(items, grammar):
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

def goto(items, symbol, grammar):
    goto_set = set()
    for item in items:
        if '.' in item[1]:
            dot_index = item[1].index('.')
            if dot_index < len(item[1]) - 1 and item[1][dot_index + 1] == symbol:
                goto_set.add((item[0], item[1][:dot_index] + symbol + '.' + item[1][dot_index + 2:]))
    return closure(goto_set, grammar)

def items(grammar):
    initial_item = ('S\'', '.' + list(grammar.keys())[0])
    states = [closure({initial_item}, grammar)]
    dfa = {}
    while True:
        new_states = states.copy()
        for state in states:
            for symbol in set(''.join(''.join(production) for production in grammar.values())) | {'$'}:
                goto_state = goto(state, symbol, grammar)
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
def display_gui(grammar, first_sets, follow_sets, action, goto_table, states, dfa):
    root = tk.Tk()
    root.title("SLR(1)分析器结果")

    text_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=100, height=40)
    text_area.pack(pady=10, padx=10)

    # 识别活前缀的DFA
    text_area.insert(tk.END, "识别活前缀的DFA:\n")
    for (state, symbol), goto_state in dfa.items():
        state_index = states.index(state) if state in states else None
        goto_state_index = states.index(goto_state) if goto_state in states else None
        if state_index is not None and goto_state_index is not None:
            text_area.insert(tk.END, f"从状态 {state_index} 通过符号 {symbol} 到状态 {goto_state_index}\n")
        else:
            text_area.insert(tk.END, f"从状态 {state} 通过符号 {symbol} 到状态 {goto_state}\n")
    text_area.insert(tk.END, "\n")

    # LR(0)项目集规范族
    text_area.insert(tk.END, "LR(0)项目集规范族:\n")
    for i, state in enumerate(states):
        text_area.insert(tk.END, f"I{i}:\n")
        for item in state:
            text_area.insert(tk.END, f"  {item}\n")
        text_area.insert(tk.END, "\n")

    # FOLLOW集合
    text_area.insert(tk.END, "FOLLOW集合:\n")
    for non_terminal, set_ in follow_sets.items():
        text_area.insert(tk.END, f"FOLLOW({non_terminal}) = {set_}\n")
    text_area.insert(tk.END, "\n")

    # SLR(1)分析表
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

# 获取用户输入并计算结果
def get_input_and_compute():
    input_text = grammar_input.get("1.0", tk.END)
    grammar = parse_grammar(input_text)
    first_sets = compute_first_sets(grammar)
    follow_sets = compute_follow_sets(grammar, first_sets)
    states, dfa = items(grammar)
    action, goto_table = build_slr1_parsing_table(grammar, first_sets, follow_sets)
    display_gui(grammar, first_sets, follow_sets, action, goto_table, states, dfa)

# 创建GUI界面
root = tk.Tk()
root.title("SLR(1)分析器")

tk.Label(root, text="请输入文法，每行一个产生式，例如：\nS -> bASB | bA\nA -> dSa | e\nB -> cAa | c").pack(pady=10)
grammar_input = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=50, height=10)
grammar_input.pack(pady=10, padx=10)

compute_button = tk.Button(root, text="计算", command=get_input_and_compute)
compute_button.pack(pady=10)

root.mainloop()
