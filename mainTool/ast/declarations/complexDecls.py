from mainTool.ast.statements.statements import Statement, CompoundStatement
from mainTool.ast.expressions.primaryExpressions import PrimaryExpression
from mainTool.ast.expressions.expression import Identifier
from mainTool.ast.astNode import ASTNode
from mainTool.ast.walking.visitor import ASTNodeVisitor

from typing import List
from mainTool.utils.types import ClassType

# 包括函数和类的定义

# 函数参数类型
class ParameterType(ASTNode):
    def __init__(self):
        super(ParameterType, self).__init__()
        self.baseType: str = None
        self.completeType: str = None

    def getEscapedCodeStr(self) -> str:
        if self.codeStr is not None:
            return self.codeStr
        return self.completeType

# 函数返回类型
class ReturnType(ASTNode):
    def __init__(self):
        super(ReturnType, self).__init__()
        self.baseType: str = None
        self.completeType: str = None

    def getEscapedCodeStr(self) -> str:
        return self.completeType

# 函数定义形参
class Parameter(ASTNode):
    def __init__(self):
        super(Parameter, self).__init__()
        self.type: ParameterType = None
        self.name: Identifier = None
        self.defaultValue: PrimaryExpression = None

    def setName(self, name: Identifier):
        self.name = name
        super().addChild(name)

    def setType(self, type: ParameterType):
        self.type = type
        super().addChild(type)

    def setDefaultValue(self, value: PrimaryExpression):
        self.defaultValue = value
        super().addChild(value)

    def addChild(self, node):
        if isinstance(node, Identifier):
            self.setName(node)
        elif isinstance(node, ParameterType):
            self.setType(node)
        elif isinstance(node, PrimaryExpression):
            self.setDefaultValue(node)
        else:
            super().addChild(node)

    def accept(self, visitor: ASTNodeVisitor):
        visitor.visit(self)


# 参数列表
class ParameterList(ASTNode):
    def __init__(self):
        super(ParameterList, self).__init__()
        self.parameters: List[Parameter] = list()

    def addParameter(self, param: Parameter):
        self.parameters.append(param)
        super().addChild(param)

    def addChild(self, node):
        if isinstance(node, Parameter):
            self.addParameter(node)

    # 将所有参数名加载到一个string里面
    def getEscapedCodeStr(self) -> str:
        if self.codeStr is not None:
            return self.codeStr

        if len(self.parameters) == 0:
            self.codeStr = ""
            return self.codeStr

        s = ""
        for param in self.parameters:
            s += param.getEscapedCodeStr() + " , "

        s = s.encode('utf-8')[:-3].decode('utf-8')
        self.codeStr = s
        return s

    def accept(self, visitor: ASTNodeVisitor):
        visitor.visit(self)


class FunctionDef(ASTNode):
    def __init__(self):
        super(FunctionDef, self).__init__()
        self.name: Identifier = None # 函数名
        self.parameterList: ParameterList = None # 形参列表
        self.returnType: ReturnType = None # 返回类型
        self.content: CompoundStatement = None # 函数body

    def replaceName(self, name: Identifier):
        i = self.children.index(self.name)
        self.children[i] = name
        self.name = name

    def setContent(self, functionContent: CompoundStatement):
        self.content = functionContent
        super().addChild(functionContent)

    def setParameterList(self, parameterList: ParameterList):
        self.parameterList = parameterList
        super().addChild(parameterList)

    def setName(self, name: Identifier):
        self.name = name
        super().addChild(name)

    def setReturnType(self, returnType: ReturnType):
        self.returnType = returnType
        super().addChild(returnType)

    def addChild(self, node):
        if isinstance(node, CompoundStatement):
            self.setContent(node)
        elif isinstance(node, ParameterList):
            self.setParameterList(node)
        elif isinstance(node, ReturnType):
            self.setReturnType(node)
        elif isinstance(node, Identifier):
            self.setName(node)
        else:
            super().addChild(node)

class ClassDefStatement(Statement):
    def __init__(self):
        super(ClassDefStatement, self).__init__()
        self.name: Identifier = None
        self.functionDefs: List[FunctionDef] = list()
        self.type: ClassType = None

    def addChild(self, node):
        if isinstance(node, Identifier):
            self.name = node
        super().addChild(node)