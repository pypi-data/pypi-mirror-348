def color_sample():

    print("\033[30mThis is black text.\033[0m")    # 黑色文本  
    print("\033[31mThis is red text.\033[0m")       # 红色文本  
    print("\033[32mThis is green text.\033[0m")     # 绿色文本  
    print("\033[33mThis is yellow text.\033[0m")    # 黄色文本  
    print("\033[34mThis is blue text.\033[0m")      # 蓝色文本  
    print("\033[35mThis is magenta text.\033[0m")   # 洋红色文本  
    print("\033[36mThis is cyan text.\033[0m")      # 青色文本  
    print("\033[37mThis is white text.\033[0m")     # 白色文本

    print("\033[40mThis text has a black background.\033[0m")    # 黑色背景  
    print("\033[41mThis text has a red background.\033[0m")       # 红色背景  
    print("\033[42mThis text has a green background.\033[0m")     # 绿色背景  
    print("\033[43mThis text has a yellow background.\033[0m")     # 黄色文本  
    print("\033[44mThis text has a blue background.\033[0m")     # 蓝色文本  
    print("\033[45mThis text has a magenta background.\033[0m")     # 洋红色文本  
    print("\033[46mThis text has a cyan background.\033[0m")     # 青色文本  
    print("\033[47mThis text has a white background.\033[0m")     # 白色背景

    print("\033[1mThis is bold text.\033[0m")        # 加粗文本  
    print("\033[4mThis is underlined text.\033[0m")   # 下划线文本  

    print("\033[31;47mRed text on white background.\033[0m")


    print("遍历测试：")
    for i in range(100):
        print(f"\033[{i}m测试{i}\033[0m")