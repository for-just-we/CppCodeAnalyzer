from mainTool.ast.astNode import ASTNode
from mainTool.ast.expressions.postfixExpressions import CallExpression
from mainTool.ast.expressions.expressionHolders import Callee
from mainTool.ast.expressions.expression import ArrayIndexing, UnaryOp
from mainTool.ast.expressions.postfixExpressions import IncDecOp
from mainTool.ast.expressions.binaryExpressions import BinaryExpression, AssignmentExpr
from typing import Set

# judging whether a statement could be a sink point, following SySeVR
class SyVCPoint(object):
    def __init__(self, sensitive_apis: Set[str]):
        self.sensitive_apis: Set[str] = sensitive_apis

    def judgeSink(self, astNode: ASTNode):
        # Library/API Function Call
        if isinstance(astNode, Callee):
            if astNode.getEscapedCodeStr() in self.sensitive_apis:
                return True
        # Array Usage
        elif isinstance(astNode, ArrayIndexing):
            return True
        # Pointer Usage
        elif isinstance(astNode, UnaryOp):
            if astNode.operator == '*':
                return True
        # Arithmetic Expression
        elif isinstance(astNode, BinaryExpression):
            if astNode.operator in { '+', '-', '*', '/' }:
                return True

        flag = False
        for i in range(astNode.getChildCount()):
            flag = flag or self.judgeSink(astNode.getChild(i))
        return flag


class XFGPoint(SyVCPoint):
    def __init__(self, sensitive_apis: Set[str]):
        super(XFGPoint, self).__init__(sensitive_apis)

    def judgeSink(self, astNode: ASTNode):
        # Library/API Function Call
        if isinstance(astNode, Callee):
            if astNode.getEscapedCodeStr() in self.sensitive_apis:
                return True
        # Array Usage
        elif isinstance(astNode, ArrayIndexing):
            return True
        # Pointer Usage
        elif isinstance(astNode, UnaryOp):
            if astNode.operator == '*':
                return True
        # Arithmetic Expression
        elif isinstance(astNode, BinaryExpression):
            if astNode.operator in { '+', '-', '*', '/', '<<', '>>' }:
                return True
        # increament assignment
        elif isinstance(astNode, AssignmentExpr):
            if astNode.operator in { "+=", "-=", "*=", "/=", "%=", ">>=", "<<=" }:
                return True
        # # x++ / x-- / ++x / --x
        elif isinstance(astNode, IncDecOp):
            return True

        flag = False
        for i in range(astNode.getChildCount()):
            flag = flag or self.judgeSink(astNode.getChild(i))
        return flag



# judging whether a statement could be a function call, haven't consider nesting function call
class CallExprTool(object):
    def __init__(self):
        self.functionName: str = None
        self.argNum: int = -1

    def judgeCall(self, astNode: ASTNode):
        # Library/API Function Call
        if isinstance(astNode, CallExpression):
            self.functionName = astNode.getChild(0).getEscapedCodeStr()
            self.argNum = astNode.argumentList.getChildCount()
            return
        for i in range(astNode.getChildCount()):
            self.judgeCall(astNode.getChild(i))