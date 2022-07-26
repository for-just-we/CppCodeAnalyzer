from mainTool.udg.useDefGraph import UseOrDef
from mainTool.udg.astProvider import ASTProvider
from typing import List

class UseDefEnvironment(object):
    def __init__(self):
        self.astProvider: ASTProvider = None
        # 交由父节点处理的token
        self.symbols: List[str] = list()

    def isUse(self, child: ASTProvider) -> bool:
        return False

    def isDef(self, child: ASTProvider) -> bool:
        return False

    # Propagate all symbols to upstream
    # 交由父节点处理的symbol
    def upstreamSymbols(self) -> List[str]:
        return self.symbols

    # 处理子结点的symbol，默认全部交给父节点
    def addChildSymbols(self, childSymbols: List[str], child: ASTProvider):
        self.symbols.extend(childSymbols)

    #  默认不生成任何use或者def symbol
    def useOrDefsFromSymbols(self, child: ASTProvider) -> List[UseOrDef]:
        return []

    def createDefOrUseForSymbols(self, symbols: List[str], isDef: bool) -> List[UseOrDef]:
        retval: List[UseOrDef] = list()
        for s in symbols:
            useOrDef: UseOrDef = UseOrDef()
            useOrDef.isDef = isDef
            useOrDef.symbol = s
            useOrDef.astProvider = self.astProvider
            retval.append(useOrDef)
        return retval

    def createDefsForAllSymbols(self, symbols: List[str]) -> List[UseOrDef]:
        return self.createDefOrUseForSymbols(symbols, True)

    def createUsesForAllSymbols(self, symbols: List[str]) -> List[UseOrDef]:
        return self.createDefOrUseForSymbols(symbols, False)

# 只有使用symbol，没有定义symbol，Condition和ReturnStatement属于这一类
class UseEnvironment(UseDefEnvironment):
    # 只有use，没有def
    def isUse(self, child: ASTProvider) -> bool:
        return True

    # 该结点下所有的symbol记为使用
    def useOrDefsFromSymbols(self, child: ASTProvider) -> List[UseOrDef]:
        retval: List[UseOrDef] = self.createUsesForAllSymbols(self.symbols)
        return retval

class EmitUseEnvironment(UseDefEnvironment):
    def __init__(self):
        super().__init__()
        self.useSymbols: List[str] = list()

    def addChildSymbols(self, childSymbols: List[str], child: ASTProvider):
        self.useSymbols.extend(childSymbols)

    # 该结点下所有的useSymbols记为使用
    def useOrDefsFromSymbols(self, child: ASTProvider) -> List[UseOrDef]:
        retval: List[UseOrDef] = self.createUsesForAllSymbols(self.useSymbols)
        return retval


class EmitDefEnvironment(UseDefEnvironment):
    def __init__(self):
        super().__init__()
        self.defSymbols: List[str] = list()

    def addChildSymbols(self, childSymbols: List[str], child: ASTProvider):
        if self.isDef(child):
            self.defSymbols.extend(childSymbols)
        if self.isUse(child):
            self.symbols.extend(childSymbols)

    def useOrDefsFromSymbols(self, child: ASTProvider) -> List[UseOrDef]:
        retval: List[UseOrDef] = self.createDefsForAllSymbols(self.defSymbols) + \
                                 self.createUsesForAllSymbols(self.symbols)
        return retval


class EmitDefAndUseEnvironment(UseDefEnvironment):
    def __init__(self):
        super().__init__()
        self.useSymbols: List[str] = list()
        self.defSymbols: List[str] = list()

    def addChildSymbols(self, childSymbols: List[str], child: ASTProvider):
        if self.isDef(child):
            self.defSymbols.extend(childSymbols)
        if self.isUse(child):
            self.useSymbols.extend(childSymbols)

    def useOrDefsFromSymbols(self, child: ASTProvider) -> List[UseOrDef]:
        retval: List[UseOrDef] = list()
        if self.isDef(child):
            retval.extend(self.createDefsForAllSymbols(self.defSymbols))
        if self.isUse(child):
            retval.extend(self.createUsesForAllSymbols(self.useSymbols))
        return retval


class CallEnvironment(UseDefEnvironment):
    def addChildSymbols(self, childSymbols: List[str], child: ASTProvider):
        childNumber: int = child.getChildNumber()
        # 函数名不添加
        if childNumber != 0:
            self.symbols.extend(childSymbols)


class IdentifierEnvironment(UseDefEnvironment):
    # Identifier类型直接获取token作为symbol
    def upstreamSymbols(self) -> List[str]:
        code: str = self.astProvider.getEscapedCodeStr()
        retval: List[str] = [code]
        return retval

# 结构体成员访问
class MemberAccessEnvironment(UseDefEnvironment):
    def upstreamSymbols(self) -> List[str]:
        # emit all symbols
        retval: List[str] = self.symbols.copy()
        # emit entire code string
        retval.append(self.astProvider.getEscapedCodeStr())
        return retval

    def addChildSymbols(self, childSymbols: List[str], child: ASTProvider):
        # 结构体变量名添加到symbol中但是使用的成员变量名不添加
        childNum: int = child.getChildNumber()
        if childNum == 0:
            super().addChildSymbols(childSymbols, child)

    def useOrDefsFromSymbols(self, child: ASTProvider) -> List[UseOrDef]:
        return self.createUsesForAllSymbols(self.symbols)


class PtrMemberAccessEnvironment(UseDefEnvironment):
    def upstreamSymbols(self) -> List[str]:
        # emit all symbols as '* symbol'
        retval: List[str] = ['* ' + c for c in self.symbols]
        retval.append(self.astProvider.getEscapedCodeStr())
        return retval

    def addChildSymbols(self, childSymbols: List[str], child: ASTProvider):
        # 结构体变量名添加到symbol中但是使用的成员变量名不添加
        childNum: int = child.getChildNumber()
        if childNum == 0:
            super().addChildSymbols(childSymbols, child)

    def useOrDefsFromSymbols(self, child: ASTProvider) -> List[UseOrDef]:
        return self.createUsesForAllSymbols(self.symbols)


# EmitDefEnvironment
# 赋值语句
class AssignmentEnvironment(EmitDefEnvironment):
    def isUse(self, child: ASTProvider) -> bool:
        childNum: int = child.getChildNumber()
        # 如果是第一个symbol
        if childNum == 0:
            # 如果operator不为空 并且 operator不是 =，也就是 x = y没有使用x，而x += y即使用也重新定义
            operatorCode: str = self.astProvider.getOperatorCode()
            if operatorCode is not None and not operatorCode == "=":
                return True
            else:
                return False
        return True

    # Assignment Expr中第一个symbol为重新定义，后面的均不是
    def isDef(self, child: ASTProvider) -> bool:
        childNum: int = child.getChildNumber()
        if childNum == 0:
            return True
        return False

# 变量定义
class DeclEnvironment(EmitDefEnvironment):
    def isUse(self, child: ASTProvider) -> bool:
        return False

    def isDef(self, child: ASTProvider) -> bool:
        type: str = child.getTypeAsString()
        childNum: int = child.getChildNumber()
        # IdentifierDecl的子结点第0个是IdentifierDeclType，第1个是Identifier
        # Parameter的子结点中参数名可能是第0个参数
        return childNum == 1 and type == "Identifier"

# x++ / x-- / ++x / --x
class IncDecEnvironment(EmitDefEnvironment):
    def isUse(self, child: ASTProvider) -> bool:
        return True

    def isDef(self, child: ASTProvider) -> bool:
        return True


class UnaryOpEnvironment(EmitUseEnvironment):
    def addChildSymbols(self, childSymbols: List[str], child: ASTProvider):
        codeStr: str = self.astProvider.getEscapedCodeStr()
        if codeStr is not None and codeStr.startswith("&"):
            for symbol in childSymbols:
                self.symbols.append("& " + symbol)
            return
        # 不是*p
        if codeStr is None or not codeStr.startswith("*"):
            self.symbols.extend(childSymbols)
            return
        # emit all symbols as '* symbol'
        retval: List[str] = ["* " + c for c in childSymbols]
        # emit entire code string
        self.useSymbols.extend(childSymbols)
        self.symbols.extend(retval)


class ArrayIndexingEnvironment(EmitDefAndUseEnvironment):
    def isUse(self, child: ASTProvider) -> bool:
        return True

    def addChildSymbols(self, childSymbols: List[str], child: ASTProvider):
        childNum: int = child.getChildNumber()
        # 数组名
        if childNum == 0:
            derefedChildren: List[str] = ["* " + c for c in childSymbols]
            self.symbols.extend(derefedChildren)

        self.useSymbols.extend(childSymbols)


class ArgumentEnvironment(EmitDefAndUseEnvironment):
    def __init__(self):
        super().__init__()
        self.isUsePointer = False
        self.isDefPointer = False

    def isUse(self, child: ASTProvider) -> bool:
        return True

    def isDef(self, child: ASTProvider) -> bool:
        return self.isDefPointer

    def setIsUsePointer(self):
        self.isUsePointer = True

    def setIsDefPointer(self):
        self.isDefPointer = True

    def addChildSymbols(self, childSymbols: List[str], child: ASTProvider):
        # 函数调用默认不会改变参数，参数指针指向可能改变
        if self.isDefPointer:
            # For tainted arguments, add "* symbol" instead of symbol
            # to defined symbols. Make an exception if symbol starts with '& '
            derefChildSymbols: List[str] = list(map(lambda symbol: "* " + symbol if not symbol.startswith("&")
                else symbol.encode('utf-8')[2:].decode('utf-8'), childSymbols))
            self.defSymbols.extend(derefChildSymbols)

        if self.isUsePointer:
            # 使用了指针类型，那么 * + id 会被添加到使用到的symbol中
            derefChildSymbols: List[str] = list(map(lambda symbol: "* " + symbol if not symbol.startswith("&")
                else symbol.encode('utf-8')[2:].decode('utf-8'), childSymbols))
            self.useSymbols.extend(derefChildSymbols)
        # id 会被添加到使用到的symbol中
        self.useSymbols.extend(childSymbols)