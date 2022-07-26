from mainTool.udg.astAnalyzers import ASTDefUseAnalyzer, CalleeInfos, CFGToUDGConverter
from mainTool.ddg.DDGCreator import *
from mainTool.cfg.CCFG import ASTToCFGConvert
from mainTool.CPG import CPG
from mainTool.cdg.CDG import *

from mainTool.antlr.CPP14Lexer import CPP14Lexer, InputStream, CommonTokenStream
from mainTool.ast.builders import *

import json
from time import time

from antlr4.tree.Tree import ParseTree, ParseTreeWalker

walker: ParseTreeWalker = ParseTreeWalker()


astAnalyzer: ASTDefUseAnalyzer = ASTDefUseAnalyzer()
calleeInfos: CalleeInfos = CalleeInfos()

calleeInfos.addArgDef("memcpy", 0)
calleeInfos.addArgUse("memcpy", 1)
calleeInfos.addArgDef("memmove", 0)
calleeInfos.addArgUse("memmove", 1)
calleeInfos.addArgDef("memset", 0)
calleeInfos.addArgDef("fgets", 0)
calleeInfos.addArgUse("atoi", 1)
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
           "        return 0;\n" + \
           "    }\n" + \
           "}"


def test():
    # AST
    start = time()
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

    # Control Dependence Graph
    cdg: CDG = createCDG(compCFG)

    # Code Property Graph
    cpg: CPG = CPG()
    cpg.initCFGEdges(compCFG)
    cpg.initCDGEdges(cdg)
    cpg.initDDGEdges(ddg)

    end = time()

    jsonCPG: dict = cpg.toJson()
    jsonSerCPG: dict = cpg.toSerializedJson()
    new_cpg: CPG = CPG.fromJson(jsonCPG)
    print(json.dumps(jsonSerCPG, indent=2))
    new_cpg1: CPG = CPG.fromSerJson(jsonSerCPG)
    print(end - start)
    return


if __name__ == '__main__':
    test()