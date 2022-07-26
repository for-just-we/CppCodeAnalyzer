from antlr4 import ParserRuleContext
from typing import List

from mainTool.ast.ParsingUtils import childTokenString
from mainTool.ast.walking.visitor import ASTNodeVisitor


NOT_SET = -1

class CodeLocation(object):
    def __init__(self, context: ParserRuleContext = None):
        self.startLine: int = NOT_SET
        self.startPos: int = NOT_SET
        self.startIndex: int = NOT_SET
        self.stopIndex: int = NOT_SET

        if context is not None:
            self.initializeFromContext(context)

    def initializeFromContext(self, context: ParserRuleContext = None):
        self.startLine = context.start.line
        self.startPos = context.start.column
        self.startIndex = context.start.tokenIndex
        self.stopIndex = context.stop.tokenIndex

    def  __str__(self):
        return f"{self.startLine}:{self.startPos}:{self.startIndex}:{self.stopIndex}"

    def __cmp__(self, other):
        if self.startLine < other.startLine:
            return -1
        elif self.startLine > other.startLine:
            return 1

        if self.startPos < other.startPos:
            return -1
        else:
            return 1

    def __lt__(self, other):
        return self.startLine < other.startLine or (self.startLine == other.startLine and
                                                    self.startPos < other.startPos)

    def __gt__(self, other):
        return self.startLine > other.startLine or (self.startLine == other.startLine and
                                                    self.startPos > other.startPos)



class ASTNode(object):
    def __init__(self):
        self.codeStr: str = None # 该node对应的代码文本
        self.parseTreeNodeContext: ParserRuleContext = None
        self.location: CodeLocation = None
        self.isInCFG: bool = False # 属于CFG node还是纯粹是AST node

        self.children: List[ASTNode] = list()
        self.childNumber: int = NOT_SET

    def addChild(self, node):
        node.childNumber = len(self.children)
        self.children.append(node)

    def getChildCount(self) -> int:
        return len(self.children)

    def getChild(self, i: int):
        if i < 0 or i >= len(self.children):
            raise RuntimeError("index out of bound")
        return self.children[i]

    def initializeFromContext(self, ctx: ParserRuleContext):
        self.parseTreeNodeContext = ctx
        self.setLocation(ctx)

    def setLocation(self, ctx: ParserRuleContext):
        self.location = CodeLocation(ctx)

    def getEscapedCodeStr(self) -> str:
        if self.codeStr is not None:
            return self.codeStr
        self.codeStr = self.escapeCodeStr(childTokenString(self.parseTreeNodeContext))
        return self.codeStr

    def escapeCodeStr(self, codeStr) -> str:
        retval = codeStr
        retval = retval.replace("\n", "\\n")
        retval = retval.replace("\t", "\\t")
        return retval

    def getLocationString(self) -> str:
        # self.setLocation(self.parseTreeNodeContext)
        return str(self.location)

    def markAsCFGNode(self):
        self.isInCFG = True

    def isLeaf(self) -> bool:
        return len(self.children) == 0

    def getTypeAsString(self):
        return type(self).__name__

    def accept(self, visitor: ASTNodeVisitor):
        visitor.visit(self)

    def __str__(self):
        return self.getEscapedCodeStr()







if __name__ == '__main__':
    location1 = CodeLocation()
    location1.startLine = 1
    location1.startPos = 2

    location2 = CodeLocation()
    location2.startLine = 2
    location2.startPos = 3

    print(location1 < location2)