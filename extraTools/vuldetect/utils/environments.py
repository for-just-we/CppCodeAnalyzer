from mainTool.udg.astProvider import ASTProvider
from typing import Set, Dict


class VariableEnvironment(object):
    def __init__(self, astProvider: ASTProvider):
        self.astProvider: ASTProvider = astProvider
        # 交由父节点处理的token
        self.handledSymbols: Set[str] = set()
        # 交由父节点处理的token
        self.upStreamSymbols: Set[str] = set()
        self.var2type: Dict[str, str] = dict() # 变量名映射为类型名
        self.funcNames: Set[str] = set() # 使用过的函数名

    # 处理子结点的symbol，默认自己解决子结点中的symbol
    def addChildSymbols(self, childSymbols: Set[str], child: ASTProvider):
        self.handledSymbols.update(childSymbols)

    # 交由父节点处理的symbol
    def upstreamSymbols(self) -> Set[str]:
        return self.upStreamSymbols

    # 自己处理的symbol
    def selfHandledSymbols(self) -> Set[str]:
        return self.handledSymbols

# 函数调用环境
class CallVarEnvironment(VariableEnvironment):
    def addChildSymbols(self, childSymbols: Set[str], child: ASTProvider):
        childNumber: int = child.getChildNumber()
        # 函数名不添加
        if childNumber != 0:
            # 参数中的变量名全都处理了
            self.handledSymbols.update(childSymbols)

    # 交由父节点处理的symbol
    def upstreamSymbols(self) -> Set[str]:
        return set()

    # 自己处理的symbol
    def selfHandledSymbols(self) -> Set[str]:
        return set()

class CalleeEnvironment(VariableEnvironment):
    def addChildSymbols(self, childSymbols: Set[str], child: ASTProvider):
        self.funcNames.update(childSymbols)


class ClassStaticIdentifierVarEnvironment(VariableEnvironment):
    # Identifier类型直接获取token作为symbol，并返回给父节点处理
    def upstreamSymbols(self) -> Set[str]:
        code: str = self.astProvider.getChild(1).getEscapedCodeStr()
        retval: Set[str] = { code }
        return retval

    def selfHandledSymbols(self) -> Set[str]:
        return set()

class IdentifierVarEnvironment(VariableEnvironment):
    # Identifier类型直接获取token作为symbol，并返回给父节点处理
    def upstreamSymbols(self) -> Set[str]:
        code: str = self.astProvider.getEscapedCodeStr()
        retval: Set[str] = { code }
        return retval

    def selfHandledSymbols(self) -> Set[str]:
        return set()

# 结构体成员访问
# 这里需要注意的是会出现 struct1 -> inner1 这种，我会将struct1 和 struct1 -> inner1 添加到变量列表，但是inner1就不会了
class MemberAccessVarEnvironment(VariableEnvironment):
    def upstreamSymbols(self) -> Set[str]:
        retval: Set[str] = { self.astProvider.getEscapedCodeStr() }
        return retval

    def addChildSymbols(self, childSymbols: Set[str], child: ASTProvider):
        # 结构体变量名添加到symbol中但是使用的成员变量名不添加
        childNum: int = child.getChildNumber()
        if childNum == 0:
            self.handledSymbols.update(childSymbols)



# 变量定义
class VarDeclEnvironment(VariableEnvironment):
    def __init__(self, astProvider: ASTProvider):
        super().__init__(astProvider)
        self.type: str = self.astProvider.getChild(0).getEscapedCodeStr()

    def addChildSymbols(self, childSymbols: Set[str], child: ASTProvider):
        # 结构体变量名添加到symbol中但是使用的成员变量名不添加
        childNum: int = child.getChildNumber()
        # 变量名
        if childNum == 1:
            for symbol in childSymbols:
                self.var2type[symbol] = self.type
            self.handledSymbols.update(childSymbols)