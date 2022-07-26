from mainTool.CPG import *
from time import time


def test():
    start = time()
    fileName = "../testfiles/sard_test_cases/CWE121_new_goto.c"

    calleeInfs = {
        "ArgDef": {
            "memcpy": [0],
            "memmove": [0],
            "memset": [0],
            "fgets": [0],
            "recv": [1],
        },
        "ArgUse": {
            "memcpy": [1],
            "memmove": [1],
            "memset": [1]
        },
        "ArgDefStartIds": {
            "scanf": 1,
            "fscanf": 2
        }
    }
    calleeInfos = initialCalleeInfos(calleeInfs)
    converter: CFGToUDGConverter = CFGToUDGConverter()
    astAnalyzer: ASTDefUseAnalyzer = ASTDefUseAnalyzer()
    astAnalyzer.calleeInfos = calleeInfos
    converter.astAnalyzer = astAnalyzer
    defUseConverter: CFGAndUDGToDefUseCFG = CFGAndUDGToDefUseCFG()
    ddgCreator: DDGCreator = DDGCreator()
    cpgs: List[CPG] = fileParse(fileName, converter, defUseConverter, ddgCreator)
    end = time()
    print(end - start)
    return


if __name__ == '__main__':
    test()