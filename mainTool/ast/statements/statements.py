from mainTool.ast.astNode import ASTNode
from mainTool.ast.expressions.expression import Expression
from mainTool.ast.walking.visitor import ASTNodeVisitor
from mainTool.utils.types import LabelType

from antlr4 import ParserRuleContext

class Statement(ASTNode):
    pass

# CompoundStatement = { + blockStatements + }
class CompoundStatement(Statement):
    def __init__(self):
        super(CompoundStatement, self).__init__()

    def getStatements(self) -> list:
        return self.children

    def addStatement(self, stmt: ASTNode):
        super().addChild(stmt)

    def getEscapedCodeStr(self) -> str:
        return ""

    def accept(self, visitor: ASTNodeVisitor):
        visitor.visit(self)

class ExpressionHolderStatement(Statement):
    def getEscapedCodeStr(self) -> str:
        expr: Expression = self.getExpression()
        if expr is None:
            return ""
        return expr.getEscapedCodeStr()

    def getExpression(self):
        if self.getChildCount() == 0:
            return None
        return self.getChild(0)

# 表达式语句, expr + ;
class ExpressionStatement(ExpressionHolderStatement):
    def getEscapedCodeStr(self) -> str:
        expr: Expression = self.getExpression()
        if expr is None:
            self.codeStr = ";"
        else:
            self.codeStr = expr.getEscapedCodeStr() + " ;"
        return self.codeStr

# 变量定义语句，每个child对应1个IdentifierDecl
class IdentifierDeclStatement(Statement):
    def __init__(self):
        super(IdentifierDeclStatement, self).__init__()
        self.typeNameContext: ParserRuleContext = None

    def accept(self, visitor: ASTNodeVisitor):
        visitor.visit(self)

class Label(Statement):
    # goto语句一般为NormalLabel， Case语句为Case，Default为default
    def __init__(self):
        super(Label, self).__init__()
        self.type: LabelType = None
        self.cond: Expression = None

    def addChild(self, node):
        if isinstance(node, Expression):
            self.cond = node
            super().addChild(node)

