from extraTools.vuldetect.deepwukong import *
from time import time




def test():
    start = time()
    fileName = "../testfiles/sard_test_cases/CWE_119_124_fscanf.c"
    file1: str = "../testfiles/sard_test_cases/io.c"
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

    systemDefinedFuncs: Set[str] = { "main", "memset", "memmove", "fscanf", "time", "printf", "wprintf", "puts"
                                     "sscanf", "isxdigit", "iswxdigit", "swscanf", "rand"}
    systemDefinedVars: Set[str] = { "argc", "argv", "stdin", "stdout", "cin", "cout" }

    calleeInfos = initialCalleeInfos(calleeInfs)
    converter: CFGToUDGConverter = CFGToUDGConverter()
    defUseConverter: CFGAndUDGToDefUseCFG = CFGAndUDGToDefUseCFG()
    ddgCreator: DDGCreator = DDGCreator()
    cpgs: List[CPG] = fileParse(fileName, calleeInfos, converter, defUseConverter, ddgCreator)
    for cpg in cpgs:
        cpg.file = fileName
    symbolizingTool: SymbolizingTool = SymbolizingTool(systemDefinedVars, systemDefinedFuncs)
    symbolizingTool.getVarFuncNamesInFile(cpgs)
    print(symbolizingTool.func2symbol)
    print(symbolizingTool.var2symbol)

    print("======================================")

    sensitive_apis: Set[str] = {"malloc", "memset"}
    sliceTool: XFGSliceTool = XFGSliceTool(cpgs, sensitive_apis, symbolizingTool)
    sliceTool.generateSliceForProgram()

    for slice in sliceTool.slices:
        for key, value in slice.toJson().items():
            print(key)
            print(value)
        print("======================")

    end = time()
    print(end - start)
    return



def testGenerateSlices():
    file1: str = "../testfiles/sard_test_cases/io.c"
    file2: str = "../testfiles/sard_test_cases/CWE_119_122_switch.c"

    testfiles: List[str] = ["../testfiles/sard_test_cases/CWE123_Write_What_Where_Condition__connect_socket_53a.c",
                            "../testfiles/sard_test_cases/CWE123_Write_What_Where_Condition__connect_socket_53b.c",
                            "../testfiles/sard_test_cases/CWE123_Write_What_Where_Condition__connect_socket_53c.c",
                            "../testfiles/sard_test_cases/CWE123_Write_What_Where_Condition__connect_socket_53d.c"]

    calleeInfs = {
        "ArgDef": {
            "memcpy": [0],
            "memmove": [0],
            "memset": [0],
            "fgets": [0],
            "recv": [1],
            "free": [0]
        },
        "ArgUse": {
            "memcpy": [1],
            "memmove": [1],
            "memset": [1],
            "connect": [1]
        },
        "ArgDefStartIds": {
            "scanf": 1,
            "fscanf": 2
        }
    }

    start = time()
    systemDefinedFuncs: Set[str] = {"main", "memset", "memmove", "fscanf", "time", "printf", "wprintf", "puts",
                                    "sscanf", "isxdigit", "iswxdigit", "swscanf", "rand", "exit",
                                    "malloc", "free", "srand", "WSAStartup", "socket", "connect",
                                    "inet_addr", "htons", "recv", "CLOSE_SOCKET", "WSACleanup"}
    systemDefinedVars: Set[str] = {"argc", "argv", "stdin", "stdout", "cin", "cout", "SOCKET_ERROR"}
    sensitive_apis: Set[str] = { "malloc", "memset" }

    calleeInfos = initialCalleeInfos(calleeInfs)
    converter: CFGToUDGConverter = CFGToUDGConverter()
    defUseConverter: CFGAndUDGToDefUseCFG = CFGAndUDGToDefUseCFG()
    ddgCreator: DDGCreator = DDGCreator()
    cpgsCommon: List[CPG] = fileParse(file1, calleeInfos, converter, defUseConverter, ddgCreator) # print et al
    for cpg in cpgsCommon:
        cpg.joinSlice = False
        cpg.file = file1

    # cpgsMain: List[CPG] = fileParse(file2, calleeInfos, converter, defUseConverter, ddgCreator) # print et al
    # for cpg in cpgsMain:
    #     cpg.file = file2
    cpgMainss: List[CPG] = list()
    for testfile in testfiles:
        cpgMains: List[CPG] = fileParse(testfile, calleeInfos, converter, defUseConverter, ddgCreator)
        for cpg in cpgMains:
            cpg.file = testfile
        cpgMainss.extend(cpgMains)

    cpgs = cpgsCommon + cpgMainss

    symbolizingTool: SymbolizingTool = SymbolizingTool(systemDefinedVars, systemDefinedFuncs)
    symbolizingTool.getVarFuncNamesInFile(cpgs)

    print(symbolizingTool.var2symbol)
    print(symbolizingTool.func2symbol)
    print("======================================")

    sliceTool: XFGSliceTool = XFGSliceTool(cpgs, sensitive_apis, symbolizingTool)
    sliceTool.generateSliceForProgram()

    for slice in sliceTool.slices:
        for key, value in slice.toJson().items():
            print(key)
            print(value)
        print("======================")

    end = time()
    print(end - start)
    return

if __name__ == '__main__':
    test()