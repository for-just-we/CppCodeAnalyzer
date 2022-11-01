from mainTool.CPG import *
import argparse
import sys
import os
import json


suffixs: Set[str] = {'c', 'cxx', 'c++', 'cpp', 'cc', 'cp', 'hxx', 'h', 'hpp'}

def show_files(base_path, all_files: List[str]):
    """
    遍历当前目录所有py文件及文件夹
    :param path:
    :param all_files:
    """
    file_list = os.listdir(base_path)
    # 准备循环判断每个元素是否是文件夹还是文件，是文件的话，把名称传入list，是文件夹的话，递归
    for file in file_list:
        # 利用os.path.join()方法取得路径全名，并存入cur_path变量，否则每次只能遍历一层目录
        cur_path = os.path.join(base_path, file)
        # 判断是否是文件夹
        if os.path.isdir(cur_path):
            show_files(cur_path, all_files)
        else:
            suffix = file.split('.')[-1]
            if suffix in suffixs:
                all_files.append(cur_path)

def _argparse():
    parser = argparse.ArgumentParser(description='user guide for CppCodeAnalyzer')
    parser.add_argument('-f', '--file', required=False, type=str,
                        help='specify c file to be parsed')
    parser.add_argument('-d', '--dir', required=False, type=str,
                        help='specify dir which contains source files to be parsed')
    parser.add_argument('-c', '--calleeInfos', required=False, type=str,
                        help='specify dir which contains source files to be parsed',
                        default="resources/calleeInfos.json")
    parser.add_argument('-o', '--output', required=False, type=str, help='specify dir which store parsing results')
    return parser.parse_args()

if __name__ == '__main__':
    parser = _argparse()  # main这里引入命令行参数函数

    # 参数解析过程
    if parser.file is None and parser.dir is None:
        sys.stderr.write("please specify file or dir to parse")
        exit(-1)
    elif parser.file is not None and parser.dir is not None:
        sys.stderr.write("please do not specify file and dir in the same time")
        exit(-1)

    potential_output_dir = "" # 默认解析结果存放的文件夹位置
    file2parse: List[str] = list()
    # 如果指定检测一个文件，那么默认解析结果存放在输入文件同一个文件夹下
    if parser.file is not None:
        parts: List[str] = parser.file.split(os.path.sep)
        potential_output_dir = os.path.sep.join(parts[:-1])
        file2parse.append(parser.file)
    # 指定检测文件夹，那么解析结果存放在该文件夹下
    elif parser.dir is not None:
        potential_output_dir = parser.dir
        show_files(potential_output_dir, file2parse)

    if len(file2parse) == 0:
        sys.stderr.write("the dir must at least contains one c file")
        exit(-1)

    output_dir = ""
    # 没有设定解析结果存放位置的话就用默认值
    if parser.output is not None:
        output_dir = parser.output
    else:
        output_dir = potential_output_dir

    # 加载callee信息
    calleeInfs: Dict[str, Dict] = json.load(open(parser.calleeInfos, 'r', encoding='utf-8'))
    calleeInfos: CalleeInfos = initialCalleeInfos(calleeInfs)

    converter: CFGToUDGConverter = CFGToUDGConverter()
    astAnalyzer: ASTDefUseAnalyzer = ASTDefUseAnalyzer()
    astAnalyzer.calleeInfos = calleeInfos
    converter.astAnalyzer = astAnalyzer
    defUseConverter: CFGAndUDGToDefUseCFG = CFGAndUDGToDefUseCFG()
    ddgCreator: DDGCreator = DDGCreator()

    #  start analysing
    result_cpgs: List[CPG] = list()
    successful_count = 0

    for i, file_name in enumerate(file2parse):
        print(f"{i} / {len(file2parse)} -- {file_name}")
        # ddgCreator.clear()
        try:
            cpgs: List[CPG] = fileParse(file_name, converter, defUseConverter, ddgCreator)
            result_cpgs.extend(cpgs)
            successful_count += 1
        except Exception as e:
            print(f"syntax error might appear in {file_name}")

    output_file = output_dir + "result.json"
    json_cpgs: List[Dict] = [cpg.toSerializedJson() for cpg in result_cpgs]
    json.dump(json_cpgs, open(output_file, 'w', encoding='utf-8'), indent=2)
