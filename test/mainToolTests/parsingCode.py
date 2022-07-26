from mainTool.antlr.CPP14Lexer import CPP14Lexer, InputStream, CommonTokenStream
from mainTool.antlr.CPP14Parser import CPP14Parser

class A(object):
    pass

class B(A):
    pass

class C(B):
    pass

if __name__ == '__main__':
    code = "while(x <= 1){\n    x++;\n  ++x;\n}"
    inputStream = InputStream(code)
    cpp14Lexer = CPP14Lexer(inputStream)
    tokenStream = CommonTokenStream(cpp14Lexer)
    parser = CPP14Parser(tokenStream)
    tree = parser.iterationstatement()
    print("========")

    set1 = set([(1, 2), (1, 3), (1, 4)])
    set2 = set([(1, 2)])
    print(set2.difference(set1))

    print({"main", "memset", "memmove", "fscanf", "time", "printf", "wprintf", "puts",
                                    "sscanf", "isxdigit", "iswxdigit", "swscanf", "rand",
                                    "malloc", "free", "srand"})
