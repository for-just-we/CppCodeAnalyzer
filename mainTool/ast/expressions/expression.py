from mainTool.ast.astNode import ASTNode
from mainTool.ast.walking.visitor import ASTNodeVisitor

class Expression(ASTNode):
    def __init__(self):
        super(Expression, self).__init__()
        self.operator: str = ""

    def replaceFirstChild(self, node: ASTNode):
        self.children[0] = node

#  定义的标识符，主要是变量名，类名，函数名等等
class Identifier(Expression):
    def accept(self, visitor: ASTNodeVisitor):
        visitor.visit(self)

    def copy(self):
        identifier: Identifier = Identifier()
        identifier.codeStr = self.codeStr
        identifier.location = self.location
        return identifier

# 类静态变量等等，比如int testClass::var = 1;
class ClassStaticIdentifier(Identifier):
    def __init__(self):
        super(ClassStaticIdentifier, self).__init__()
        self.className: Identifier = None
        self.varName: Identifier = None

    def addChild(self, node):
        if isinstance(node, Identifier):
            if self.className is None:
                self.className = node
            else:
                self.varName = node
        super().addChild(node)

    def copy(self):
        classIdentifier: ClassStaticIdentifier = ClassStaticIdentifier()
        className: Identifier = self.className.copy()
        varName: Identifier = self.varName.copy()
        classIdentifier.addChild(className)
        classIdentifier.addChild(varName)
        classIdentifier.location = self.location
        return classIdentifier

    def getEscapedCodeStr(self) -> str:
        return self.className.getEscapedCodeStr() + "::" + self.varName.getEscapedCodeStr()

# 数组访问, Expression [ Expression ]
class ArrayIndexing(Expression):
    def __init__(self):
        super(ArrayIndexing, self).__init__()
        self.array: Expression = None # 数组名，可以为变量名，或者函数调用等表达式
        self.index: Expression = None # 索引

    def setArrayExpression(self, array: Expression):
        self.array = array
        super().addChild(array)

    def setIndexExpression(self, index: Expression):
        self.index = index
        super().addChild(index)

    def addChild(self, node):
        if isinstance(node, Expression) and self.getChildCount() == 0:
            self.setArrayExpression(node)
        elif isinstance(node, Expression) and self.getChildCount() == 1:
            self.setIndexExpression(node)
        else:
            super().addChild(node)

    def accept(self, visitor: ASTNodeVisitor):
        visitor.visit(self)


# 转换类型
class CastTarget(Expression):
    pass

# 类型转换
class CastExpression(Expression):
    def __init__(self):
        super(CastExpression, self).__init__()
        self.castTarget: Expression = None
        self.castExpression: Expression = None

    def getChildCount(self) -> int:
        childCount: int = 0
        if self.castTarget is not None:
            childCount += 1
        if self.castExpression is not None:
            childCount += 1
        return childCount

    def getChild(self, i: int):
        if i == 0:
            return self.castTarget
        return self.castExpression

    def setCastTarget(self, castTarget: Expression):
        self.castTarget = castTarget
        super().addChild(castTarget)

    def setCastExpression(self, castExpression: Expression):
        self.castExpression = castExpression
        super().addChild(castExpression)

    def addChild(self, node):
        if self.castTarget is None:
            self.setCastTarget(node)
        else:
            self.setCastExpression(node)

    def accept(self, visitor: ASTNodeVisitor):
        visitor.visit(self)

# 三目表达式, cond ? expr1 : expr2
class ConditionalExpression(Expression):
    pass

# ++ 或 -- 运算符
class IncDec(Expression):
    pass

## sizeof表达式
class SizeofExpr(Expression):
    pass

# sizeof运算符
class Sizeof(Expression):
    pass

# sizeof运算数
class SizeofOperand(Expression):
    pass

# 单目表达式，运算符包括 &, *, +, -, ~, !， 这里 ++x, --x种,++,--也算单目运算，不过我把它算到IncDecOp中了
class UnaryOp(Expression):
    def accept(self, visitor: ASTNodeVisitor):
        visitor.visit(self)

# 单目运算符，包括 &, *, +, -, ~, !
class UnaryOperator(Expression):
    def accept(self, visitor: ASTNodeVisitor):
        visitor.visit(self)