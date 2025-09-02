from tree_sitter import Language, Parser
import re
import time
from collections import Counter
import os

pattern = r"fn(.*?)[(<]"


Language.build_library(
    # Store the library in the `build` directory
    "build/my-languages.so",
    # Include one or more languages
    ["tree-sitter-rust"],
)

RUST_LANGUAGE = Language("build/my-languages.so", "rust")

parser = Parser()
parser.set_language(RUST_LANGUAGE)

function_query = """((function_item) @value)"""

CSRF = []
CSRL = []
path = "../result/"
# path = "/mnt/d/decompress/"
fail_compile = []
for dataset in os.listdir(path):
    print(dataset)
    # if dataset != "result_ramfs":
    #     continue
    dataset_path = path + dataset + "/compile_25/"
    topo = [one.replace(".txt", "") for one in os.listdir(dataset_path)]
    for filename in os.listdir(dataset_path):
        with open(dataset_path + filename, "r") as f:
            if f.read() != "":
                fail_compile.append(filename.replace(".txt", ""))

    matches = []
    result = []
    num1 = 0
    num2 = 0


    matches1 = []
    matches2 = []
    with open(path + dataset + "/main.rs") as f:
        code = f.read()
        tree = parser.parse(bytes(code, "utf8"))
        query = RUST_LANGUAGE.query(function_query)
        functions = query.captures(tree.root_node)
        functions = [one[0].text.decode() for one in functions]
        for function in functions:
            match = re.findall(pattern, function)
            for one in fail_compile:
                if match[0].strip().lower().replace("_", "") == one.strip().lower().replace("_", ""):
                    num1 += 1
                    matches1.append(function)
            for one in topo:
                if match[0].strip().lower().replace("_", "") == one.strip().lower().replace("_", ""):
                    num2 += 1
                    matches2.append(function)
    length1 = 0
    length2 = 0
    for one in matches2:
        length2 += one.count("\n") + 1
    for one in matches1:
        length1 += one.count("\n") + 1
    
    CSRF.append(1 - num1/num2)
    CSRL.append(1 - length1/length2)
    print(f"{dataset}组件编译通过率为{1 - length1/length2}")
print("------ 平均 ------")
print(f"CSRF: {sum(CSRF)/len(CSRF)}")
print(f"CSRL: {sum(CSRL)/len(CSRL)}")




