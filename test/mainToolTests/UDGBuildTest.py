from mainTool.udg.useDefGraph import *
from mainTool.udg.astAnalyzers import ASTDefUseAnalyzer, CalleeInfos
from mainTool.udg.astProvider import ASTNodeASTProvider

from mainTool.antlr.CPP14Lexer import CPP14Lexer, InputStream, CommonTokenStream
from mainTool.ast.builders import *

from antlr4.tree.Tree import ParseTree, ParseTreeWalker

walker: ParseTreeWalker = ParseTreeWalker()


astAnalyzer: ASTDefUseAnalyzer = ASTDefUseAnalyzer()
calleeInfos: CalleeInfos = CalleeInfos()

def getParser(code: str) -> CPP14Parser:
    inputStream = InputStream(code)
    cpp14Lexer = CPP14Lexer(inputStream)
    tokenStream = CommonTokenStream(cpp14Lexer)
    parser = CPP14Parser(tokenStream)
    return parser

def testFuncCallStmt():
    calleeInfos.addArgDef("memcpy", 0)
    calleeInfos.addArgUse("memcpy", 1)
    calleeInfos.addArgDef("memmove", 0)
    calleeInfos.addArgUse("memmove", 1)
    calleeInfos.addArgDef("memset", 0)
    calleeInfos.addArgDef("fgets", 0)
    calleeInfos.addArgDef("recv", 1)

    calleeInfos.addArgDefStartIds("scanf", 1)
    calleeInfos.addArgDefStartIds("fscanf", 2)
    astAnalyzer.calleeInfos = calleeInfos

    # function call
    code = "memcpy(data, source, 100*sizeof(char));" # 定义了 *data，使用了 data, source, *source
    code1 = "memset(source, 'C' ,100- 1);" # 定义了 *source，使用了source
    code2 = "scanf(\"%d-%d\", &a, &b);"
    coden = "fscanf(stdin, \"%d\", &data);"
    code3 = "fgets(inputBuffer, CHAR_ARRAY_SIZE, stdin);"
    code4 = "fgets(data+dataLen, (int)(FILENAME_MAX - dataLen), stdin);"
    code5 = "recvResult = recv(connectSocket, (char*)(data+dataLen) , " + \
                    "sizeof(char)*(FILENAME_MAX-dataLen-1), 0);"
    code6 = "recv(connectSocket, (char*)(data+dataLen) , sizeof(char)*(FILENAME_MAX-dataLen-1), 0);"

    # ptr access
    ptrAccessCode = "*(p + 1 + i) = *(a + j);"
    # array access
    arrayAccessCode = "p[1 + i] = a[j][i];"
    arrayAccessCode1 = "a[i][j] = b[1 + i];"

    # struct access
    structAccCode = "foo.bar = 10;"
    structAccCode1 = "foo->bar = foo1.f1.f2;"
    structAccCode2 = "structCharVoid->charFirst[(sizeof(structCharVoid->charFirst) / sizeof(char))-1] = '\0';"
    structAccCode3 = "structCharVoid->voidSecond = (void*)SRC_STR;"
    structAccCode4 = "memmove(structCharVoid->charFirst, SRC_STR, sizeof(*structCharVoid));"

    # assign
    assignCode1 = "*p = a;"
    assignCode2 = "*p += a;"

    parser: CPP14Parser = getParser(coden)
    tree: ParseTree = parser.statement()
    builder: FunctionContentBuilder = FunctionContentBuilder()
    builder.stack.append(CompoundStatement())
    walker.walk(builder, tree)
    expressionStatement: ExpressionStatement = builder.stack[-1].getChild(0)

    provider: ASTNodeASTProvider = ASTNodeASTProvider()
    provider.node = expressionStatement
    usesAndDefs: Set[UseOrDef] = astAnalyzer.analyzeAST(provider)

    for useOrDef in usesAndDefs:
        print(f"{useOrDef.astProvider.getEscapedCodeStr()} --- {useOrDef.symbol} : {useOrDef.isDef}")
    return


def testIdentifierDecl():
    code = "char source[100] = '\0';"
    code1 = "char* dst = (char*)malloc(sizeof(char)*100);"
    code2 = "struct my_struct foo;"

    calleeInfos.addArgDef("recv", 1)
    astAnalyzer.calleeInfos = calleeInfos

    parser: CPP14Parser = getParser(code2)
    tree: ParseTree = parser.statement()
    builder: FunctionContentBuilder = FunctionContentBuilder()
    builder.stack.append(CompoundStatement())
    walker.walk(builder, tree)
    declStatement: IdentifierDeclStatement = builder.stack[-1].getChild(0)

    provider: ASTNodeASTProvider = ASTNodeASTProvider()
    provider.node = declStatement
    usesAndDefs: Set[UseOrDef] = astAnalyzer.analyzeAST(provider)

    for useOrDef in usesAndDefs:
        print(f"{useOrDef.astProvider.getEscapedCodeStr()} --- {useOrDef.symbol} : {useOrDef.isDef}")
    return


if __name__ == '__main__':
    testFuncCallStmt()