def generate_strings(grammar, start_symbol, max_steps):
    """
    使用给定的文法生成字符串。

    参数:
    grammar (dict): 文法的产生式规则。
    start_symbol (str): 起始符。
    max_steps (int): 最大生成步骤数。

    返回:
    list of str: 生成的字符串列表。
    """
    current_strings = [start_symbol]
    for _ in range(max_steps):
        next_strings = []
        for string in current_strings:
            expanded = False
            for key, productions in grammar.items():
                if key in string:
                    for production in productions:
                        next_strings.append(string.replace(key, production, 1))
                    expanded = True
            if not expanded:
                next_strings.append(string)
        current_strings = next_strings
    return current_strings

# 定义文法
grammar = {
    'S': ['aSb','']
}

# 生成字符串
start_symbol = 'S'
max_steps = 2
generated_strings = generate_strings(grammar, start_symbol, max_steps)

# 打印结果
print("生成的字符串:")
for string in generated_strings:
    print(string)
