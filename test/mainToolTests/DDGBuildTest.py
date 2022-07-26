from mainTool.udg.useDefGraph import *
from mainTool.udg.astAnalyzers import ASTDefUseAnalyzer, CalleeInfos, CFGToUDGConverter
from mainTool.udg.astProvider import ASTNodeASTProvider
from mainTool.ddg.DefUseGraph import DefUseCFG
from mainTool.ddg.DDGCreator import *
from mainTool.cfg.CCFG import ASTToCFGConvert

from mainTool.antlr.CPP14Lexer import CPP14Lexer, InputStream, CommonTokenStream
from mainTool.ast.builders import *

from antlr4.tree.Tree import ParseTree, ParseTreeWalker
from time import time
walker: ParseTreeWalker = ParseTreeWalker()


astAnalyzer: ASTDefUseAnalyzer = ASTDefUseAnalyzer()
calleeInfos: CalleeInfos = CalleeInfos()

calleeInfos.addArgDef("memcpy", 0)
calleeInfos.addArgUse("memcpy", 1)
calleeInfos.addArgDef("memmove", 0)
calleeInfos.addArgUse("memmove", 1)
calleeInfos.addArgDef("memset", 0)
calleeInfos.addArgDef("fgets", 0)
calleeInfos.addArgDef("recv", 1)
calleeInfos.addArgDefStartIds("scanf", 1)
astAnalyzer.calleeInfos = calleeInfos


def getParser(code: str) -> CPP14Parser:
    inputStream = InputStream(code)
    cpp14Lexer = CPP14Lexer(inputStream)
    tokenStream = CommonTokenStream(cpp14Lexer)
    parser = CPP14Parser(tokenStream)
    return parser


code = "static void goodG2B2(int a)\n" + \
           "{\n" + \
           "    char * data;\n" + \
           "    data = NULL;\n" + \
           "    switch(6)\n" + \
           "    {\n" + \
           "    case 6:\n" + \
           "        /* FIX: Allocate and point data to a large buffer that is at least as large as the large buffer used in the sink */\n" + \
           "        data = (char *)malloc(100*sizeof(char));\n" + \
           "        if (data == NULL) {exit(-1);}\n" + \
           "        data[0] = '\\0'; /* null terminate */\n" + \
           "        break;\n" + \
           "    default:\n" + \
           "        /* INCIDENTAL: CWE 561 Dead Code, the code below will never run */\n" + \
           "        printLine(\"Benign, fixed string\");\n" + \
           "        break;\n" + \
           "    }\n" + \
           "    {\n" + \
           "        size_t i;\n" + \
           "        char source[100];\n" + \
           "        memset(source, 'C', 100-1); /* fill with 'C's */\n" + \
           "        source[100-1] = '\\0'; /* null terminate */\n" + \
           "        /* POTENTIAL FLAW: Possible buffer overflow if source is larger than data */\n" + \
           "        for (i = 0; i < 100; i++)\n" + \
           "        {\n" + \
           "            data[i] = source[i];\n" + \
           "        }\n" + \
           "        data[100-1] = '\\0'; /* Ensure the destination buffer is null terminated */\n" + \
           "        printLine(data);\n" + \
           "        free(data);\n" + \
           "    }\n" + \
           "}"


code1 = "void CWE124_Buffer_Underwrite__char_alloca_memmove_82_bad::action(char * data = NULL){\n" + \
        "    char source[100];\n" + \
        "    memset(source, 'C', 100-1);\n" + \
        "    source[100-1] = '\0';\n" + \
        "    memmove(data, source, 100*sizeof(char));\n" + \
        "    data[100-1] = '\0';\n" + \
        "    printLine(data);\n" + \
        "}"

code2 = "void CWE122_Heap_Based_Buffer_Overflow__c_CWE805_char_memmove_04_bad(){\n" + \
        "    char * data;\n" + \
        "    data = NULL;\n" + \
        "    data = (char *)malloc(50*sizeof(char));\n" + \
        "    if (data == NULL) {exit(-1);}\n" + \
        "    data[0] = '\0';\n" + \
        "    char source[100];\n" + \
        "    memset(source, 'C', 100-1);\n" + \
        "    source[100-1] = '\0';\n" + \
        "    memmove(data, source, 100*sizeof(char));\n" + \
        "    printLine(data);\n" + \
        "    free(data);\n" + \
        "}"


def test():
    startTime = time()
    # AST
    parser: CPP14Parser = getParser(code)
    tree: ParseTree = parser.functiondefinition()
    builder: FunctionDefBuilder = FunctionDefBuilder()
    walker.walk(builder, tree)

    # CFG
    functionDef: FunctionDef = builder.functionDef
    compCFG: CFG = ASTToCFGConvert(functionDef)

    # UDG
    converter: CFGToUDGConverter = CFGToUDGConverter()
    converter.astAnalyzer = astAnalyzer
    useDefGraph: UseDefGraph = converter.convert(compCFG)

    # DefUseCFG
    defUseConverter: CFGAndUDGToDefUseCFG = CFGAndUDGToDefUseCFG()
    defUseCFG: DefUseCFG = defUseConverter.convert(compCFG, useDefGraph)

    # Data Dependence Graph
    ddgCreator: DDGCreator = DDGCreator()
    ddg: DDG = ddgCreator.createForDefUseCFG(defUseCFG)

    endTime = time()

    print(endTime - startTime)
    for edge in ddg.defUseEdges:
        print(f"{str(edge.src)} ----[{edge.symbol}] ----- {str(edge.dst)}")
    return

if __name__ == '__main__':
    test()