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

def testFunctionCall():
    code: str = 'func(a, b + c);'
    code1: str = "func();"
    parser: CPP14Parser = getParser(code1)
    tree: ParseTree = parser.statement()
    builder: FunctionContentBuilder = FunctionContentBuilder()
    builder.stack.append(CompoundStatement())
    walker.walk(builder, tree)
    return

def testSizeofExpr():
    code: str = 'sizeof a'
    parser: CPP14Parser = getParser(code)
    tree: ParseTree = parser.sizeofExpression()
    builder: FunctionContentBuilder = FunctionContentBuilder()
    builder.stack.append(AssignmentExpr())
    walker.walk(builder, tree)
    return

def testSimpleCast():
    code: str = "char(a + b * c)"
    parser: CPP14Parser = getParser(code)
    tree: ParseTree = parser.postfixexpression()
    builder: FunctionContentBuilder = FunctionContentBuilder()
    builder.stack.append(AssignmentExpr())
    walker.walk(builder, tree)
    return

def testCast():
    code: str = "(struct TestClass)a"
    parser: CPP14Parser = getParser(code)
    tree: ParseTree = parser.castexpression()
    builder: FunctionContentBuilder = FunctionContentBuilder()
    builder.stack.append(AssignmentExpr())
    walker.walk(builder, tree)
    return

def testCppCast():
    code: str = "static_cast<unsigned int>(7.987)"
    parser: CPP14Parser = getParser(code)
    tree: ParseTree = parser.postfixexpression()
    builder: FunctionContentBuilder = FunctionContentBuilder()
    builder.stack.append(AssignmentExpr())
    walker.walk(builder, tree)
    return


def testIdentifierDeclSimple():
    code: str = "unsigned int a, *p, **pp;"
    parser: CPP14Parser = getParser(code)
    tree: ParseTree = parser.simpledeclaration()
    builder: FunctionContentBuilder = FunctionContentBuilder()
    builder.stack.append(CompoundStatement())
    walker.walk(builder, tree)
    return


def testIdentifierDeclWithAssign():
    # typedef
    codeType: str = "typedef long long LL;"

    # C语言初始化
    code: str = "unsigned int a = b + c, d{a}, e(8);"
    code1: str = "char aa ='A', bb{'B'}, cc('C'), **dd(NULL);"
    code2: str = "char source[100], *dst[100], p[50][40];" # 数组定义
    code3: str = "char source[100] = L'A';" # 数组初始化
    code4: str = "int data[100] = {1, 2, 3, 4};"
    code5: str = "struct ST s = {1, 'a'};" # 结构体初始化
    code6: str = "struct ST s(1, 'a');" # 构造函数初始化
    code7: str = "int aa = b > 1 ? 1 : a;" # 三目表达式初始化赋值

    # C++初始化
    cppCpde: str = "vector<int> v4{10,1};"

    # const int
    Ccode: str = "const int a = char(1);"
    autoCode: str = "auto a = &i;"
    # static variable
    staticCode: str = "unsigned int test::m_value1 = 0, ::a = 1, *bb(4);"
    staticCode1: str = "singleton *singleton::m_instance= NULL;"

    parser: CPP14Parser = getParser(staticCode1)
    tree: ParseTree = parser.simpledeclaration()
    builder: FunctionContentBuilder = FunctionContentBuilder()
    builder.stack.append(CompoundStatement())
    walker.walk(builder, tree)
    return


def testNewExpression():
    code: str = "unsigned int **p = new unsigned int* [10];"
    code1: str = "int *a = new(buf) int[a+b];"
    code2: str = "Fun* ptr1 = new Fun;"

    parser: CPP14Parser = getParser(code2)
    tree: ParseTree = parser.simpledeclaration()
    builder: FunctionContentBuilder = FunctionContentBuilder()
    builder.stack.append(CompoundStatement())
    walker.walk(builder, tree)
    return


def testDeleteExpression():
    baseDelete: str = "delete [] p;"
    arrayDelete: str = "delete [] p[i][j];"
    ptrDelete: str = "delete [] *(p+1);"

    parser: CPP14Parser = getParser(ptrDelete)
    tree: ParseTree = parser.deleteexpression()
    builder: FunctionContentBuilder = FunctionContentBuilder()
    builder.stack.append(CompoundStatement())
    walker.walk(builder, tree)
    return


def testThrowExpression():
    throwExpr: str = "throw -1;"
    throwExpr2: str = "throw \"error msg\";"

    parser: CPP14Parser = getParser(throwExpr)
    tree: ParseTree = parser.expressionstatement()
    builder: FunctionContentBuilder = FunctionContentBuilder()
    builder.stack.append(CompoundStatement())
    walker.walk(builder, tree)
    return

def testStd():
    code: str = "std::cout << \"yes\" << a << endl;"
    code1: str = "recvResult = recv(connectSocket, (char*)(data+dataLen) , sizeof(char)*(FILENAME_MAX-dataLen-1), 0);"

    parser: CPP14Parser = getParser(code1)
    tree: ParseTree = parser.expressionstatement()
    builder: FunctionContentBuilder = FunctionContentBuilder()
    builder.stack.append(CompoundStatement())
    walker.walk(builder, tree)
    return


def testSelectionStatement():
    ifElseCode: str = "if (a == 1)\n" + \
                "    a = 1;\n" + \
                "else if (a == 2)\n" + \
                "    a = 2;\n" + \
                "else \n" + \
                "    a = 3;"
    ifCode1: str = "if (staticFalse){ exit(-1); goto loop; *p = a * b; return a + 1; }"

    switchCode = "switch (staticTrue){\n" + \
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
    builder.stack.append(CompoundStatement())
    walker.walk(builder, tree)
    return

def testMemberAccess():
    memberaccessExpr: str = "a.x = 1;"
    memberCall: str = "a.f(x, y);"

    parser: CPP14Parser = getParser(memberCall)
    tree: ParseTree = parser.expressionstatement()
    builder: FunctionContentBuilder = FunctionContentBuilder()
    builder.stack.append(CompoundStatement())
    walker.walk(builder, tree)
    return

def testArrayAccess():
    stmt: str = "arr[i] = 1;"
    stmt1: str = "*(p + i) = 2;"
    stmt2: str = "f.ar[i] = 1;"

    parser: CPP14Parser = getParser(stmt1)
    tree: ParseTree = parser.expressionstatement()
    builder: FunctionContentBuilder = FunctionContentBuilder()
    builder.stack.append(CompoundStatement())
    walker.walk(builder, tree)
    return


def testTryCatch():
    code: str = "try{\n" + \
                "        const int& a = 1;\n" + \
                "    }catch(const int& e){\n" + \
                "    }catch(...){\n" + \
                "    }"

    parser: CPP14Parser = getParser(code)
    tree: ParseTree = parser.tryblock()
    builder: FunctionContentBuilder = FunctionContentBuilder()
    builder.stack.append(CompoundStatement())
    walker.walk(builder, tree)
    return


def testIteration():
    stmt: str =  "while(x <= 1){\n" + \
                "    x++;\n" + \
                "    ++x;\n" + \
                 "    x+=1;\n" + \
                 "}"

    stmt1: str = "do {\n" + \
    "    int a = sizeof(int);\n" + \
    "    b = sizeof(a);\n" + \
    "}while(a + b <= 4);"

    stmt2: str = "for(int i = 0; i < 10; ++i);"

    stmt3: str = "for (unsigned int * p: vec){\n" + \
    "   unsigned int a = b + c, d{a}, e(8);\n" + \
    "   char source[100], *dst[100], p[50][40];\n" + \
    "   }"

    parser: CPP14Parser = getParser(stmt)
    tree: ParseTree = parser.iterationstatement()
    builder: FunctionContentBuilder = FunctionContentBuilder()
    builder.stack.append(Statement())
    walker.walk(builder, tree)
    return



def FunctionDefBuilderTest():
    code: str = "struct ST* c1::func(unsigned int *a = NULL, struct ST s){\n" + \
        "    int a = 1;\n" + \
        "}"

    code1: str = "char* func1(unsigned int a[], int aa = 1){\n" + \
        "    int c = a[0] + aa;\n" + \
        "}"

    code2: str = "#ifdef INCLUDEMAIN\n" + \
                "\n" + \
                "int main(int argc, char * argv[])\n" + \
                "{\n" + \
                "    /* seed randomness */\n" + \
                "    srand( (unsigned int)time(NULL) );\n" + \
                "#ifndef OMITGOOD\n" + \
                "    printLine(\"Calling good()...\");\n" + \
                "    CWE127_Buffer_Underread__wchar_t_declare_memmove_68_good();\n" + \
                "    printLine(\"Finished good()\");\n" + \
                "#endif /* OMITGOOD */\n" + \
                "#ifndef OMITBAD\n" + \
                "    printLine(\"Calling bad()...\");\n" + \
                "    CWE127_Buffer_Underread__wchar_t_declare_memmove_68_bad();\n" + \
                "    printLine(\"Finished bad()\");\n" + \
                "#endif /* OMITBAD */\n" + \
                "    return 0;\n" + \
                "}\n" + \
                "\n" + \
                "#endif"

    parser: CPP14Parser = getParser(code2)
    tree: ParseTree = parser.functiondefinition()
    builder: FunctionDefBuilder = FunctionDefBuilder()
    # builder.stack.append(Statement())
    walker.walk(builder, tree)
    return


def ClassDefBuilderTest():
    code: str = "class c1{\n" + \
        "    private:\n" + \
        "    unsigned int* cccc(int a[], char **p){\n" + \
        "    int aa = char(c);\n" + \
        "    }\n" + \
        "};"

    parser: CPP14Parser = getParser(code)
    tree: ParseTree = parser.translationunit()
    builder: ClassDefBuilder = ClassDefBuilder()
    walker.walk(builder, tree)
    return


def FileBuilderTest():
    fileName: str = "testfiles/sard_test_cases/CWE_119_124_class_method_decl.c"
    fileName1: str = "testfiles/ComplexStruct.c"

    code = open(fileName, 'r', encoding='utf-8').read()
    # inputStream: InputStream = FileStream(fileName1)
    parser = getParser(code)
    # cpp14Lexer = CPP14Lexer(inputStream)
    # tokenStream = CommonTokenStream(cpp14Lexer)
    # parser = CPP14Parser(tokenStream)
    tree: ParseTree = parser.translationunit()
    builder: FileBuilder = FileBuilder()
    walker.walk(builder, tree)
    return


if __name__ == '__main__':
    testIteration()