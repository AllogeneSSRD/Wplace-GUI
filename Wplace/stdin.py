def my_print(head, head_type='info', content=None):
    """
    前景色（文本颜色）：
    30：黑色
    31：红色
    32：绿色
    33：黄色
    34：蓝色
    35：洋红色
    36：青色
    37：白色

    背景色：
    40：黑色
    41：红色
    42：绿色
    43：黄色
    44：蓝色
    45：洋红色
    46：青色
    47：白色
    """
    if content is None:
        content = ''
    if head_type == 'info':
        bg = 42 # 背景色：绿色
        word = 38
    elif head_type in ('warn', 'warning'):
        bg = 43 # 黄
        word = 31
    elif head_type in ('err', 'error'):
        bg = 41 # 红
        word = 38
    elif head_type == 'data':
        bg = 47 # 白
        word = 30
    else:
        bg = 44 # 蓝
        word = 38
    print(f"\033[{bg};{word}m {head} \033[0m {content}")

if __name__ == '__main__':
    my_print('Hello, world!', 'info', 'This is a test message.')
    # 测试 'info' 类型的头部
    my_print('Info Header', 'info', 'This is an info message.')

    # 测试 'warn' 类型的头部
    my_print('Warning Header', 'warn', 'This is a warning message.')

    # 测试 'err' 类型的头部
    my_print('Error Header', 'err', 'This is an error message.')

    # 测试 'data' 类型的头部
    my_print('Data Header', 'data', 'This is a data message.')

    # 测试未定义类型的头部
    my_print('Undefined Header', 'undefined', 'This is an undefined type message.')

    my_print(f"[warn] Channel mismatch: img.shape={123}, baseline.shape={456}")