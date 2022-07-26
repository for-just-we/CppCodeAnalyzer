from mainTool.ast.expressions.expression import Expression
from mainTool.ast.astNode import ASTNode
from mainTool.ast.walking.visitor import ASTNodeVisitor


class ExpressionHolder(Expression):
    def getEscapedCodeStr(self) -> str:
        if self.codeStr is not None:
            return self.codeStr

        expr: Expression = self.getExpression()
        if expr is None:
            return ""
        codeStr = expr.getEscapedCodeStr()
        return codeStr

    def getExpression(self):
        if self.getChildCount() > 0:
            return self.getChild(0)
        return None


# 函数调用参数，子类为Expression
# 如果在解析AST的时候精简掉Argument后面解析Use Def的时候不太好弄
class Argument(ExpressionHolder):
    pass

# ArgumentList可以接任意个（包括0个） Argument，没有参数的话就是一个没有child的 ArgumentList
class ArgumentList(ExpressionHolder):
    def accept(self, visitor: ASTNodeVisitor):
        visitor.visit(self)


# Callee 可能为 Identifier（直接使用函数名）或者MemberAccess、PtrMemberAccess（成员函数）
class Callee(ExpressionHolder):
    pass

# 条件判断
class Condition(ExpressionHolder):
    def accept(self, visitor: ASTNodeVisitor):
        visitor.visit(self)

# 对应数组赋值 a = { a1, a2, a3 } 中的 a1, a2, a3，可能有嵌套
class InitializerList(ExpressionHolder):
    pass

class ThrowExpression(ExpressionHolder):
    def __init__(self):
        super(ThrowExpression, self).__init__()
        self.throwExpression = None

    def getThrowExpression(self):
        return self.throwExpression

    def addChild(self, node: ASTNode):
        if isinstance(node, Expression):
            self.throwExpression = node
        super().addChild(node)


