def generate_positive_closure(language, max_length):
    """
    生成给定语言的正闭包中的所有可能字符串，限制最大长度。

    参数:
    language (set of str): 给定语言的字符串集合。
    max_length (int): 生成字符串的最大长度。

    返回:
    set of str: 正闭包中的字符串集合。
    """
    closure = set()
    
    # 初始化正闭包集合为空
    for length in range(1, max_length + 1):
        new_strings = {''.join(p) for p in product(language, repeat=length)}
        closure.update(new_strings)
    
    return closure

from itertools import product

# 示例语言
language = {"a", "b"}

# 生成语言的正闭包，限制最大长度为 3
closure = generate_positive_closure(language, 3)

# 打印结果
print("正闭包:")
for string in closure:
    print(string)
