from mainTool.ast.statements.statements import Statement
from mainTool.ast.walking.visitor import ASTNodeVisitor


class JumpStatement(Statement):
    pass

# break;
class BreakStatement(JumpStatement):
    def accept(self, visitor: ASTNodeVisitor):
        visitor.visit(self)

# continue;
class ContinueStatement(JumpStatement):
    def accept(self, visitor: ASTNodeVisitor):
        visitor.visit(self)

# goto label;
class GotoStatement(JumpStatement):
    def getTarget(self) -> str:
        return self.getChild(0).getEscapedCodeStr()

    def getEscapedCodeStr(self) -> str:
        return "goto " + self.getTarget() + ";"

    def accept(self, visitor: ASTNodeVisitor):
        visitor.visit(self)

# return expr;
class ReturnStatement(JumpStatement):
    def accept(self, visitor: ASTNodeVisitor):
        visitor.visit(self)