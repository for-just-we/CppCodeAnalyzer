from mainTool.ast.expressions.expression import Expression
from mainTool.ast.walking.visitor import ASTNodeVisitor

# literals，常量部分
class PrimaryExpression(Expression):
    def accept(self, visitor: ASTNodeVisitor):
        visitor.visit(self)

# bool类型常量
class BoolExpression(PrimaryExpression):
    def accept(self, visitor: ASTNodeVisitor):
        visitor.visit(self)

# char类型常量
class CharExpression(PrimaryExpression):
    def accept(self, visitor: ASTNodeVisitor):
        visitor.visit(self)

# float, double类型常量
class DoubleExpression(PrimaryExpression):
    def accept(self, visitor: ASTNodeVisitor):
        visitor.visit(self)

# int, short, unsigned int, unsigned short, long, unsigned long类型常量
class IntegerExpression(PrimaryExpression):
    def accept(self, visitor: ASTNodeVisitor):
        visitor.visit(self)

# 指针类型常量只有2种，NULL和nullptr
class PointerExpression(PrimaryExpression):
    def accept(self, visitor: ASTNodeVisitor):
        visitor.visit(self)

# 字符串类型常量
class StringExpression(PrimaryExpression):
    def accept(self, visitor: ASTNodeVisitor):
        visitor.visit(self)