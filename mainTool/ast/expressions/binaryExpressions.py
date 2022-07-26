from mainTool.ast.expressions.expression import Expression
from mainTool.ast import astNode
from antlr4.ParserRuleContext import ParserRuleContext
from typing import List


#  二元运算表达式
class BinaryExpression(Expression):
    def __init__(self):
        super(Expression, self).__init__()
        self.flag: bool = True
        self.subExpressions: List[Expression] = [None, None]

    def getLeft(self) -> Expression:
        return self.subExpressions[0]

    def getRight(self) -> Expression:
        return self.subExpressions[1]

    def setLeft(self, left: Expression):
        self.subExpressions[0] = left

    def setRight(self, right: Expression):
        self.subExpressions[1] = right

    def addChild(self, item: astNode):
        if not isinstance(item, Expression):
            raise RuntimeError("Error: child of BinaryExpression should be Expression")
        if self.getLeft() is None:
            self.setLeft(item)
        elif self.getRight() is None:
            self.setRight(item)
        else:
            raise RuntimeError("Error: attempting to add third child to binary expression")
        super().addChild(item)

    def getChildCount(self) -> int:
        childCount: int = 0
        if self.getLeft() is not None:
            childCount += 1
        if self.getRight() is not None:
            childCount += 1
        return childCount

    def getChild(self, i: int):
        return self.subExpressions[i]

    def initializeFromContext(self, ctx: ParserRuleContext):
        super().initializeFromContext(ctx)
        if ctx.getChildCount() == 3 and self.flag:
            self.operator = ctx.getChild(1).getText()


# 加减运算，op 包括 +, -。2个AST子结点
class AdditiveExpression(BinaryExpression):
    pass

# 与运算，op 包括 &&
class AndExpression(BinaryExpression):
    pass

# 赋值运算，op 包括 =, *=, /=, %=, +=, -=, <<=, >>=, &=, ^=, |=
# c语言中规定 赋值运算符的左边必须变量，不能是常量。
class AssignmentExpr(BinaryExpression):
    pass

# 逻辑与运算，op 包括 &
class BitAndExpression(BinaryExpression):
    pass

# 等于判断，op 包括 ==, !=
class EqualityExpression(BinaryExpression):
    pass

# 逻辑异或运算，op 包括 ^
class ExclusiveOrExpression(BinaryExpression):
    pass

# 或运算，op 包括 ||
class InclusiveOrExpression(BinaryExpression):
    pass

# 乘除模运算，op 包括 *, /, %
class MultiplicativeExpression(BinaryExpression):
    pass

# 或运算，op 包括 ||
class OrExpression(BinaryExpression):
    pass

# 大于小于判断，op 包括 <, >, <=, >=
class RelationalExpression(BinaryExpression):
    pass

# 移位运算，op 包括 <<, >>
class ShiftExpression(BinaryExpression):
    pass