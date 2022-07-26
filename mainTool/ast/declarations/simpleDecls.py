from mainTool.ast.expressions.expression import Expression, Identifier
from mainTool.ast.astNode import ASTNode

class IdentifierDeclType(ASTNode):
    def __init__(self):
        super(IdentifierDeclType, self).__init__()
        self.baseType: str = None
        self.completeType: str = None

    def getEscapedCodeStr(self) -> str:
        if self.codeStr is not None:
            return self.codeStr
        return self.completeType


class IdentifierDecl(ASTNode):
    def __init__(self):
        super(IdentifierDecl, self).__init__()
        self.type: IdentifierDeclType = None
        self.name: Identifier = None

    def setName(self, name: Identifier):
        self.name = name
        super().addChild(name)

    def setType(self, type: IdentifierDeclType):
        self.type = type
        super().addChild(type)

    def addChild(self, node):
        if isinstance(node, Identifier):
            self.setName(node)
        elif isinstance(node, IdentifierDeclType):
            self.setType(node)
        else:
            super().addChild(node)

    def getEscapedCodeStr(self) -> str:
        if self.codeStr is not None:
            return self.codeStr
        self.codeStr = ' '.join( [self.getChild(i).getEscapedCodeStr() for i in range(self.getChildCount())])

    # def getChildCount(self) -> int:
    #     childCount: int = 0
    #     if self.type is not None:
    #         childCount += 1
    #     if self.name is not None:
    #         childCount += 1
    #     return childCount
    #
    # def getChild(self, i: int):
    #     if i == 0:
    #         return self.type
    #     elif i == 1:
    #         return self.name
    #     else:
    #         return self.children[i - 1]


# for init 表达式
class ForInit(Expression):
    pass

class ForRangeInit(IdentifierDecl):
    def __init__(self):
        super(ForRangeInit, self).__init__()
        # 要遍历的数组表达式
        self.arrayExpr: Expression = None

    def setArrayExpr(self, arrayExpr: Expression):
        self.arrayExpr = arrayExpr
        arrayExpr.childNumber = self.getChildCount()
        self.children.append(arrayExpr)

    def setType(self, type: IdentifierDeclType):
        super().setType(type)
        self.type.childNumber = 0
        self.name.childNumber = 1

    def addChild(self, node):
        # Type var1: var2
        if isinstance(node, Identifier):
            # var1
            if self.name is None:
                self.setName(node)
            # var2
            else:
                self.setArrayExpr(node)

        elif isinstance(node, Expression):
            self.setArrayExpr(node)

        elif isinstance(node, IdentifierDeclType):
            self.setType(node)

    def getEscapedCodeStr(self) -> str:
        return self.type.getEscapedCodeStr() + " " + self.name.getEscapedCodeStr() + " : " + self.arrayExpr.getEscapedCodeStr()

