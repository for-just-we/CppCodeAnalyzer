from mainTool.cdg.CDG import *
from mainTool.antlr.CPP14Lexer import CPP14Lexer, InputStream, CommonTokenStream
from antlr4.tree.Tree import ParseTree
from mainTool.ast.builders import *

from mainTool.cfg.CCFG import *

walker: ParseTreeWalker = ParseTreeWalker()

code: str = "static void goodG2B2()\n" + \
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

code1: str = "void CWE124_Buffer_Underwrite__CWE839_fscanf_17_bad()\n" + \
            "{\n" + \
            "    int i,j;\n" + \
            "    int data;\n" + \
            "    /* Initialize data */\n" + \
            "    data = -1;\n" + \
            "    for(i = 0; i < 1; i++)\n" + \
            "    {\n" + \
            "        /* POTENTIAL FLAW: Read data from the console using fscanf() */\n" + \
            "        fscanf(stdin, \"%d\", &data);\n" + \
            "    }\n" + \
            "    for(j = 0; j < 1; j++)\n" + \
            "    {\n" + \
            "        {\n" + \
            "            int i;\n" + \
            "            int buffer[10] = { 0 };\n" + \
            "            /* POTENTIAL FLAW: Attempt to access a negative index of the array\n" + \
            "            * This code does not check to see if the array index is negative */\n" + \
            "            if (data < 10)\n" + \
            "            {\n" + \
            "                buffer[data] = 1;\n" + \
            "                /* Print the array values */\n" + \
            "                for(i = 0; i < 10; i++)\n" + \
            "                {\n" + \
            "                    printIntLine(buffer[i]);\n" + \
            "                }\n" + \
            "            }\n" + \
            "            else\n" + \
            "            {\n" + \
            "                printLine(\"ERROR: Array index is negative.\");\n" + \
            "            }\n" + \
            "        }\n" + \
            "    }\n" + \
            "}\n"


code2: str = "void CWE121_Stack_Based_Buffer_Overflow__CWE129_fgets_01_bad()\n" + \
            "{\n" + \
            "    int data;\n" + \
            "    /* Initialize data */\n" + \
            "    data = -1;\n" + \
            "    {\n" + \
            "        char inputBuffer[CHAR_ARRAY_SIZE] = \"\";\n" + \
            "        /* POTENTIAL FLAW: Read data from the console using fgets() */\n" + \
            "        if (fgets(inputBuffer, CHAR_ARRAY_SIZE, stdin) != NULL)\n" + \
            "        {\n" + \
            "            /* Convert to int */\n" + \
            "            data = atoi(inputBuffer);\n" + \
            "        }\n" + \
            "        else\n" + \
            "        {\n" + \
            "            printLine(\"fgets() failed.\");\n" + \
            "        }\n" + \
            "    }\n" + \
            "    {\n" + \
            "        int i;\n" + \
            "        int buffer[10] = { 0 };\n" + \
            "        /* POTENTIAL FLAW: Attempt to write to an index of the array that is above the upper bound\n" + \
            "        * This code does check to see if the array index is negative */\n" + \
            "        if (data >= 0)\n" + \
            "        {\n" + \
            "            buffer[data] = 1;\n" + \
            "            /* Print the array values */\n" + \
            "            for(i = 0; i < 10; i++)\n" + \
            "            {\n" + \
            "                printIntLine(buffer[i]);\n" + \
            "            }\n" + \
            "        }\n" + \
            "        else\n" + \
            "        {\n" + \
            "            printLine(\"ERROR: Array index is negative.\");\n" + \
            "        }\n" + \
            "    }\n" + \
            "}"


def getParser(code: str) -> CPP14Parser:
    inputStream = InputStream(code)
    cpp14Lexer = CPP14Lexer(inputStream)
    tokenStream = CommonTokenStream(cpp14Lexer)
    parser = CPP14Parser(tokenStream)
    return parser

def testFunctionDef():
    parser: CPP14Parser = getParser(code2)
    tree: ParseTree = parser.functiondefinition()
    builder: FunctionDefBuilder = FunctionDefBuilder()
    walker.walk(builder, tree)

    functionDef: FunctionDef = builder.functionDef
    compCFG: CFG = ASTToCFGConvert(functionDef)

    for i, (node, edges) in enumerate(compCFG.outNeighborhood.items()):
        print(f"{i} : {node}")
        for edge in edges:
            print(edge)

    print("=========================================")

    cdg: CDG = createCDG(compCFG)
    for edge in cdg.getEdges():
        print(edge)
    return

if __name__ == '__main__':
    testFunctionDef()