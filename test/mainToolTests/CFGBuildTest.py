from mainTool.cfg.CCFG import *
from mainTool.antlr.CPP14Lexer import CPP14Lexer, InputStream, CommonTokenStream
from mainTool.ast.builders import *

from antlr4.tree.Tree import ParseTree, ParseTreeWalker

walker: ParseTreeWalker = ParseTreeWalker()

def getParser(code: str) -> CPP14Parser:
    inputStream = InputStream(code)
    cpp14Lexer = CPP14Lexer(inputStream)
    tokenStream = CommonTokenStream(cpp14Lexer)
    parser = CPP14Parser(tokenStream)
    return parser

def testCompoundStatement():
    stmt: str = "{ exit(-1); *p = a * b; int s = *p + d; }"
    parser: CPP14Parser = getParser(stmt)
    tree: ParseTree = parser.statement()
    builder: FunctionContentBuilder = FunctionContentBuilder()
    builder.stack.append(CompoundStatement())
    walker.walk(builder, tree)

    compoundStatement: CompoundStatement = builder.stack.pop()
    compCFG: CFG = CCFGFactory.newCompoundInstance(compoundStatement)
    return


def testSelectionStatement():
    ifstmt: str = "if (a == 1)\n" + \
        "    a = 1;\n" + \
        "else if (a == 2)\n" + \
        "    a = 2;\n" + \
        "else \n" + \
        "    a = 3;"

    ifCode1: str = "if (staticFalse){ exit(-1); goto loop; *p = a * b; return a + 1; }"

    switchCode: str = "switch (staticTrue){\n" + \
        "    case 1:\n" + \
        "        test::a = 1;\n" + \
        "        break;\n" + \
        "    case 2:\n" + \
        "        a = 2;\n" + \
        "        break;\n" + \
        "    default:\n" + \
        "        a = 3;\n" + \
        "}"

    parser: CPP14Parser = getParser(switchCode)
    tree: ParseTree = parser.selectionstatement()
    builder: FunctionContentBuilder = FunctionContentBuilder()
    builder.stack.append(Statement())
    walker.walk(builder, tree)

    # ifStatement: IfStatement = builder.stack.pop()
    switchStatement: SwitchStatement = builder.stack.pop()
    compCFG: CFG = CCFGFactory.newSwitchInstance(switchStatement)

    for node, edges in compCFG.outNeighborhood.items():
        print(node)
        for edge in edges:
            print(edge)
    return


def testIteration():
    whileStmt: str = "while(x <= 1){\n" + \
        "    (*x)++;\n" + \
        "    ++*x;\n" + \
        "    if (cond)\n" + \
        "        break;\n" + \
        "    func(a);\n" + \
        "}"

    doStmt: str = "do {\n" + \
        "    int a = sizeof(int);\n" + \
        "    b = sizeof(a);\n" + \
        "}while(a + b <= 4);"

    forStmt: str = "for(int i = 0; i < 10; ++i){ \n" + \
                "    int a = 1;\n" + \
                "    b = c + a;" + \
                "    if (a > 0)\n" + \
                "        break;\n" + \
                "    func(a);\n" + \
                "}"

    forRangeStmt: str = "for (unsigned int * p: vec){\n" + \
                "   unsigned int a = b + c, d{a}, e(8);\n" + \
                "   char source[100], *dst[100], p[50][40];\n" + \
                "   if (staticTrue)\n" + \
                "       break;\n" + \
                "   func(a);\n" + \
                "   }"

    parser: CPP14Parser = getParser(forRangeStmt)
    tree: ParseTree = parser.iterationstatement()
    builder: FunctionContentBuilder = FunctionContentBuilder()
    builder.stack.append(Statement())
    walker.walk(builder, tree)

    # whileStatement: WhileStatement = builder.stack.pop()
    # doStatement: DoStatement = builder.stack.pop()
    # forStatement: ForStatement = builder.stack.pop()
    forRangeStatement: ForRangeStatement = builder.stack.pop()

    # compCFG: CFG = CCFGFactory.newWhileInstance(whileStatement)
    # compCFG: CFG = CCFGFactory.newDoInstance(doStatement)
    # compCFG: CFG = CCFGFactory.newForInstance(forStatement)
    compCFG: CFG = CCFGFactory.newForRangeInstance(forRangeStatement)

    for node, edges in compCFG.outNeighborhood.items():
        print(node)
        for edge in edges:
            print(edge)
    return


def testTry():
    code: str = "try{\n" + \
        "        const int& a = 1;\n" + \
        "    }catch(const int& e){\n" + \
        "    }catch(...){\n" + \
        "    }"

    parser: CPP14Parser = getParser(code)
    tree: ParseTree = parser.tryblock()
    builder: FunctionContentBuilder = FunctionContentBuilder()
    builder.stack.append(Statement())
    walker.walk(builder, tree)

    tryStatement: TryStatement = builder.stack.pop()
    compCFG: CFG = CCFGFactory.newTryInstance(tryStatement)
    return


def testFunctionDef():
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

    parser: CPP14Parser = getParser(code)
    tree: ParseTree = parser.functiondefinition()
    builder: FunctionDefBuilder = FunctionDefBuilder()
    walker.walk(builder, tree)

    functionDef: FunctionDef = builder.functionDef
    compCFG: CFG = ASTToCFGConvert(functionDef)


    for i, (node, edges) in enumerate(compCFG.outNeighborhood.items()):
        print(f"{i} : {node}")
        for edge in edges:
            print(edge)

    return

if __name__ == '__main__':
    testIteration()