from mainTool.ast.statements.statements import Statement
from mainTool.ast.declarations.simpleDecls import IdentifierDeclType, ForInit, ForRangeInit
from mainTool.ast.expressions.expressionHolders import Condition
from mainTool.ast.expressions.expression import Expression, Identifier
from mainTool.ast.walking.visitor import ASTNodeVisitor

from typing import List

class BlockStarter(Statement):
    def __init__(self):
        super(BlockStarter, self).__init__()
        self.statement: Statement = None
        self.condition: Condition = None

    def addChild(self, node):
        if isinstance(node, Condition):
            self.condition = node
        elif isinstance(node, Statement):
            self.statement = node
        super().addChild(node)

# else语句
class ElseStatement(BlockStarter):
    pass

# if语句
class IfStatement(BlockStarter):
    def __init__(self):
        super(IfStatement, self).__init__()
        self.elseNode: ElseStatement = None

    def getChildCount(self) -> int:
        childCount: int = super().getChildCount()
        if self.elseNode is not None:
            childCount += 1
        return childCount

    def getChild(self, i: int):
        if i == 0:
            return self.condition
        elif i == 1:
            return self.statement
        elif i == 2:
            return self.elseNode
        raise RuntimeError("Invalid IfItem")

    def accept(self, visitor: ASTNodeVisitor):
        visitor.visit(self)

# switch语句
class SwitchStatement(BlockStarter):
    def accept(self, visitor: ASTNodeVisitor):
        visitor.visit(self)

# while语句
class WhileStatement(BlockStarter):
    def accept(self, visitor: ASTNodeVisitor):
        visitor.visit(self)

# do-while
class DoStatement(BlockStarter):
    def accept(self, visitor: ASTNodeVisitor):
        visitor.visit(self)

# for语句
class ForStatement(BlockStarter):
    def __init__(self):
        super(ForStatement, self).__init__()
        self.forInitStatement: ForInit = None
        self.expression: Expression = None

    def addChild(self, node):
        if isinstance(node, ForInit):
            self.forInitStatement = node
        elif isinstance(node, Expression) and not isinstance(node, Condition):
            self.expression = node
        super().addChild(node)


class ForRangeStatement(BlockStarter):
    def __init__(self):
        super(ForRangeStatement, self).__init__()
        self.forRangeInit: ForRangeInit = None

    def addChild(self, node):
        if isinstance(node, ForRangeInit):
            self.forRangeInit = node
        super().addChild(node)


# Try-Catch
class CatchStatement(BlockStarter):
    def __init__(self):
        self.exceptionType: IdentifierDeclType = None
        self.exceptionIdentifier: Identifier = None
        super(CatchStatement, self).__init__()

    def setExceptionType(self, exceptionType: IdentifierDeclType):
        self.exceptionType = exceptionType
        super().addChild(exceptionType)

    def addChild(self, node):
        if isinstance(node, Identifier):
            self.exceptionIdentifier = node
        super().addChild(node)

# try下面包括一个tryBlock(CompoundStatement) 和 catchList
class TryStatement(BlockStarter):
    def __init__(self):
        super(TryStatement, self).__init__()
        self.catchList: List[CatchStatement] = list()

    def addCatchStatement(self, catchStatement: CatchStatement):
        self.catchList.append(catchStatement)

    def addChild(self, node):
        if isinstance(node, CatchStatement):
            self.addCatchStatement(node)
        else:
            super().addChild(node)