from extraTools.vuldetect.ivdetect import *

from mainTool.ast.builders import *
from mainTool.cfg.CCFG import *
from mainTool.CPG import *

from antlr4.tree.Tree import ParseTree, ParseTreeWalker

walker: ParseTreeWalker = ParseTreeWalker()

def getParser(code: str) -> CPP14Parser:
    inputStream = InputStream(code)
    cpp14Lexer = CPP14Lexer(inputStream)
    tokenStream = CommonTokenStream(cpp14Lexer)
    parser = CPP14Parser(tokenStream)
    return parser

def varGeneratingTest():
    callStmt: str = 'memset(source, dst, 100);'
    declStmt: str = "unsigned int a = b + c, d{a}, e(8);"
    declStmt1: str = "char aa ='A', bb{'B'}, cc('C'), **dd(NULL);"
    declStmt2: str = "int aa = addr < TASK_SIZE_MAX ? 1 : a;"  # 三目表达式初始化赋值
    declStmt3: str = "unsigned int test::m_value1 = 0, ::a = stu->score, *bb(4);"

    parser: CPP14Parser = getParser(declStmt2)
    tree: ParseTree = parser.simpledeclaration()
    builder: FunctionContentBuilder = FunctionContentBuilder()
    builder.stack.append(CompoundStatement())
    walker.walk(builder, tree)

    astNode: ASTNode = builder.stack.pop()
    astVarAnalyzer: ASTVarAnalyzer = ASTVarAnalyzer()
    provider: ASTNodeASTProvider = ASTNodeASTProvider()
    provider.node = astNode
    astVarAnalyzer.analyzeAST(provider)

    return


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


def feature3_4_5_Test():
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

    code1 = "static inline void init_copy_chunk_defaults(struct cifs_tcon *tcon){\n" \
            "    tcon->max_chunks = 256;\n" \
            "    tcon->max_bytes_chunk = 1048576;\n" \
            "    tcon->max_bytes_copy = 16777216;\n" \
            "}"

    code2 = "int is_valid_bugaddr(unsigned long addr){\n" \
            "    unsigned short ud;\n" \
            "    if (addr < TASK_SIZE_MAX)\n" \
            "        return 0;\n" \
            "    if (probe_kernel_address((unsigned short *)addr, ud))\n" \
            "        return 0;\n" \
            "    return ud == INSN_UD0 || ud == INSN_UD2;\n}"


    parser: CPP14Parser = getParser(code)
    tree: ParseTree = parser.functiondefinition()
    builder: FunctionDefBuilder = FunctionDefBuilder()
    walker.walk(builder, tree)

    functionDef: FunctionDef = builder.functionDef
    cfg: CFG = ASTToCFGConvert(functionDef)
    cdg: CDG = createCDG(cfg)
    # UDG
    converter: CFGToUDGConverter = CFGToUDGConverter()
    converter.astAnalyzer = astAnalyzer
    useDefGraph: UseDefGraph = converter.convert(cfg)

    # DefUseCFG
    defUseConverter: CFGAndUDGToDefUseCFG = CFGAndUDGToDefUseCFG()
    defUseCFG: DefUseCFG = defUseConverter.convert(cfg, useDefGraph)

    # Data Dependence Graph
    ddgCreator: DDGCreator = DDGCreator()
    ddg: DDG = ddgCreator.createForDefUseCFG(defUseCFG)

    cpg: CPG = CPG()
    cpg.initCFGEdges(cfg)
    cpg.initCDGEdges(cdg)
    cpg.initDDGEdges(ddg)

    varLists = generate_feature3(cpg.statements)
    for varList in varLists:
        print(varList)

    feature4s: List[List[List[str]]] = generate_feature4(cpg)
    feature5s: List[List[List[str]]] = generate_feature5(cpg)
    return


if __name__ == '__main__':
    feature3_4_5_Test()