from abc import abstractmethod
from mainTool.ast.astNode import ASTNode
from mainTool.ast.expressions.expression import Expression

class ASTProvider(object):
    @abstractmethod
    def getTypeAsString(self) -> str:
        pass

    @abstractmethod
    def getChild(self, i: int):
        pass

    @abstractmethod
    def getEscapedCodeStr(self) -> str:
        pass

    @abstractmethod
    def getChildNumber(self) -> int:
        pass

    @abstractmethod
    def getChildCount(self) -> int:
        pass

    @abstractmethod
    def getOperatorCode(self) -> str:
        pass


class ASTNodeASTProvider(ASTProvider):
    def __init__(self):
        self.node: ASTNode = None

    def getTypeAsString(self) -> str:
        return self.node.getTypeAsString()

    def getChild(self, i: int) -> ASTProvider:
        childProvider: ASTNodeASTProvider = ASTNodeASTProvider()
        childProvider.node = self.node.getChild(i)
        return childProvider

    def getChildCount(self) -> int:
        return self.node.getChildCount()

    def getEscapedCodeStr(self) -> str:
        return self.node.getEscapedCodeStr()

    def getChildNumber(self) -> int:
        return self.node.childNumber

    def getOperatorCode(self) -> str:
        if isinstance(self.node, Expression):
            return self.node.operator
        return None

    def __eq__(self, other):
        if not isinstance(other, ASTNodeASTProvider):
            return False
        return self.node == other.node