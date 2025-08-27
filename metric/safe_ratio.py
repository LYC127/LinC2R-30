import re
import os


import os
import re

def stack(line, char):
    num = 0
    if char == '{':
        a = '{'
        b = '}'
    else:
        a = '('
        b = ')'
    for i in line:
        if i == a:
            num += 1
        if i == b:
            if num - 1 == 0:
                return 0
            num -= 1
    return num
            

def calculate_rust_safety(file_path):
    safe_percentages = []
    
    for dirname in os.listdir(file_path):
            print(dirname)
        
        # for i in range(10):
            with open(file_path + dirname + f"/{dirname}.rs", 'r') as file:
            # with open(file_path + dirname + "/" + str(i) + ".txt", 'r') as file:
                lines = file.readlines()

            total_lines = len(lines)
            unsafe_lines = 0
            inside_unsafe_block1 = 0
            inside_unsafe_block2 = 0
            inside_unsafe_block3 = 0

            for line in lines:
                stripped_line = line.strip()

                # 匹配 unsafe 函数声明 (包括 unsafe extern "C" fn ...)
                if 'unsafe' in stripped_line and '{' in stripped_line:
                    inside_unsafe_block1 += stack(stripped_line, '{')
                    unsafe_lines += 1  
                    # print(line)
                elif 'unsafe' in stripped_line and '(' in stripped_line and 'extern' in stripped_line:
                    inside_unsafe_block2 += stack(stripped_line, '(')
                    unsafe_lines += 1
                    # print(line)
                elif 'unsafe' in stripped_line and '(' not in stripped_line and '{' not in stripped_line:
                    inside_unsafe_block3 = -1
                    unsafe_lines += 1
                    # print(line)
                elif inside_unsafe_block1 > 0 or inside_unsafe_block2 > 0 or inside_unsafe_block2 != 0:
                    unsafe_lines += 1
                    if ('{' in stripped_line or '}' in stripped_line) and inside_unsafe_block1 > 0:
                        if stripped_line.find('}') < stripped_line.find('{') and ('{' in stripped_line and '}' in stripped_line):
                            if inside_unsafe_block1 - 1 == 0:
                                inside_unsafe_block1 = 0
                                continue
                        inside_unsafe_block1 += stripped_line.count('{') - stripped_line.count('}')
                    if ('(' in stripped_line or ')' in stripped_line) and inside_unsafe_block2 > 0:
                        if ')' in stripped_line and '{' in stripped_line:
                            inside_unsafe_block1 += stripped_line.count('{') - stripped_line.count('}')
                        elif stripped_line.find(')') < stripped_line.find('(') and ('(' in stripped_line and ')' in stripped_line):
                            if inside_unsafe_block2 - 1 == 0:
                                inside_unsafe_block2 = 0
                                continue
                        inside_unsafe_block2 += stripped_line.count('(') - stripped_line.count(')')
                    if ('{' in stripped_line or '}' in stripped_line) and inside_unsafe_block3 != 0:
                        if inside_unsafe_block3 < 0:
                            inside_unsafe_block3 = stripped_line.count('{') - stripped_line.count('}')
                        else:
                            inside_unsafe_block3 += stripped_line.count('{') - stripped_line.count('}')
                    # print(line)
                        

            if total_lines == 0:
                safe_percentage = 1  # 防止空文件除以零
            else:
                print(unsafe_lines)
                safe_percentage = ((total_lines - unsafe_lines) / total_lines) * 100
            safe_percentages.append(safe_percentage)
            

            # print(f"{filename}")
            # print(f"Safety ratio: {safe_percentage:.2f}%")
    
    # 输出文件平均安全比例
    # print(safe_percentages)
    print(safe_percentages)
    print(f"Average Safety ratio: {sum(safe_percentages) / len(safe_percentages):.2f}%")





# file_path = '../result_4o/'
file_path = "/mnt/c/Users/12737/Desktop/c2rust dataset modify/"
calculate_rust_safety(file_path)
