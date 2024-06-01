def kleene_closure(language, max_length):
    # 初始化克林闭包集合，包含空串
    closure = {""}
    
    for _ in range(max_length):
        new_strings = set()
        for string in closure:
            for word in language:
                new_strings.add(string + word)
        closure.update(new_strings)
    
    return closure

# 示例语言
language = {"a", "b"}

# 生成语言的克林闭包，限制最大长度为 3
closure = kleene_closure(language, 3)

# 打印结果
print("克林闭包:")
for string in closure:
    print(string)
