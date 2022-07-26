from mainTool.ast.expressions.expression import Expression, Identifier
from mainTool.ast.expressions.expressionHolders import ArgumentList
from mainTool.ast.walking.visitor import ASTNodeVisitor


class PostfixExpression(Expression):
    pass

# 对应 x++ 或者 x--， ++x, --x
class IncDecOp(PostfixExpression):
    def __init__(self):
        super(IncDecOp, self).__init__()
        # isPost为true表示 ++/-- 在变量后面, x++, x--，反之为 ++x, --x
        self.isPost = True

class CallExpressionBase(PostfixExpression):
    def __init__(self):
        self.targetFunc: Expression = None
        self.argumentList: ArgumentList = None
        super(CallExpressionBase, self).__init__()

    def setTargetFunc(self, targetFunc: Expression):
        self.targetFunc = targetFunc
        super().addChild(targetFunc)

    def setArgumentList(self, argumentList: ArgumentList):
        self.argumentList = argumentList
        super().addChild(argumentList)

    def accept(self, visitor: ASTNodeVisitor):
        visitor.visit(self)

class CallExpression(CallExpressionBase):
    def addChild(self, node):
        if isinstance(node, Identifier):
            self.setTargetFunc(node)
        elif isinstance(node, ArgumentList):
            self.setArgumentList(node)
        else:
            super().addChild(node)

    def accept(self, visitor: ASTNodeVisitor):
        visitor.visit(self)


class DeleteExpression(CallExpressionBase):
    def __init__(self):
        # delete掉的变量名
        self.target: Expression = None
        super(DeleteExpression, self).__init__()

    def addChild(self, node):
        if isinstance(node, Expression) and self.target is None:
            self.target = node
        super().addChild(node)

    def accept(self, visitor: ASTNodeVisitor):
        visitor.visit(self)


class NewExpression(CallExpressionBase):
    def __init__(self):
        # targetClass
        self.targetClass: Identifier = None
        super(NewExpression, self).__init__()

    def setTargetClass(self, targetClass: Identifier):
        self.targetClass = targetClass
        self.targetClass.codeStr = self.targetClass.codeStr.strip()
        super().addChild(targetClass)

    def accept(self, visitor: ASTNodeVisitor):
        visitor.visit(self)

# 成员变量访问，对应 a.f1
class MemberAccess(PostfixExpression):
    def accept(self, visitor: ASTNodeVisitor):
        visitor.visit(self)

# 指针类型成员变量访问，a->f1
class PtrMemberAccess(PostfixExpression):
    def accept(self, visitor: ASTNodeVisitor):
        visitor.visit(self)