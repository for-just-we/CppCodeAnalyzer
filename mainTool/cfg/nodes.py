from typing import Dict
from mainTool.ast.astNode import ASTNode

class CFGNode(object):
    def __str__(self) -> str:
        return self.__class__.__name__

    def getProperties(self) -> Dict[str, object]:
        return {
            "type": str(self),
            "code": self.__class__.__name__,
            "IS_CFG_NODE": True
        }

# 普通CFG结点
class ASTNodeContainer(CFGNode):
    def __init__(self, node: ASTNode):
        self.astNode: ASTNode = node
        self.astNode.markAsCFGNode()

    def getEscapedCodeStr(self):
        return self.astNode.getEscapedCodeStr()

    def __str__(self):
        return "[" + self.astNode.getEscapedCodeStr() + "]"

# 入口结点
class CFGEntryNode(CFGNode):
    def __str__(self):
        return "[ENTRY]"

    def getProperties(self) -> Dict[str, object]:
        return {
            "type": str(self),
            "code": "ENTRY",
            "IS_CFG_NODE": True
        }

# 退出结点
class CFGExitNode(CFGNode):
    def __str__(self):
        return "[EXIT]"

    def getProperties(self) -> Dict[str, object]:
        return {
            "type": str(self),
            "code": "EXIT",
            "IS_CFG_NODE": True
        }

# 错误结点
class CFGErrorNode(CFGNode):
    def __str__(self):
        return "[ERROR]"

    def getProperties(self) -> Dict[str, object]:
        return {
            "type": str(self),
            "code": "ERROR",
            "IS_CFG_NODE": True
        }

# for循环条件没写的话就是InfiniteForNode
class InfiniteForNode(CFGNode):
    def __str__(self):
        return "[INFINITE FOR]"

    def getProperties(self) -> Dict[str, object]:
        return {
            "type": str(self),
            "code": "true",
            "IS_CFG_NODE": True
        }