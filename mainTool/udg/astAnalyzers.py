from mainTool.udg.environments import CallEnvironment, UseDefEnvironment, ArgumentEnvironment, AssignmentEnvironment
from mainTool.udg.environments import IncDecEnvironment, DeclEnvironment, PtrMemberAccessEnvironment, MemberAccessEnvironment
from mainTool.udg.environments import UseEnvironment, ArrayIndexingEnvironment, UnaryOpEnvironment, IdentifierEnvironment

from mainTool.udg.astProvider import ASTProvider, ASTNodeASTProvider
from mainTool.udg.useDefGraph import UseOrDef, UseDefGraph

from mainTool.ast.astNode import ASTNode
from mainTool.cfg.CFG import *

from typing import Set, Dict, List
import sys

# 这个类主要记录函数调用中参数为指针变量的信息，等同于Joern中的TaintSource，但是Joern考虑了指针def没考虑指针use的情况
class CalleeInfos(object):
    def __init__(self):
        # 假设key为memset，value为[0]，表示memset的第0个参数使用了指针变量，memset(a, xx,xx); 中use的symbol要包含 * a
        self.calleeToArgUseIds: Dict[str, List[int]] = dict()
        # 假设key为gets, value为[0]，表示gets函数重新定义了第0个指针参数，gets(buf) 重新定义了symbol * buf
        self.calleeToArgDefIds: Dict[str, List[int]] = dict()
        # 参数为可变参数的情况
        # 比如 scanf -> 1， 表示 scanf会重新定义第1个以后的所有参数, scanf("%d", &a) 会重新定义 a
        self.calleeToDefStartIds: Dict[str, int] = dict()

    # 判断是否使用指针
    def judgeUse(self, callEnv: CallEnvironment, childNumber: int) -> bool:
        callee: str = callEnv.astProvider.getChild(0).getEscapedCodeStr()
        return childNumber in self.calleeToArgUseIds.get(callee, [])

    # 判断是否定义指针
    def judgeDef(self, callEnv: CallEnvironment, childNumber: int) -> bool:
        callee: str = callEnv.astProvider.getChild(0).getEscapedCodeStr()
        if childNumber in self.calleeToArgDefIds.get(callee, []):
            return True
        return childNumber >= self.calleeToDefStartIds.get(callee, sys.maxsize)

    def addArgUse(self, callee: str, argN: int):
        if callee not in self.calleeToArgUseIds.keys():
            self.calleeToArgUseIds[callee] = []
        self.calleeToArgUseIds[callee].append(argN)

    def addArgDef(self, callee: str, argN: int):
        if callee not in self.calleeToArgDefIds.keys():
            self.calleeToArgDefIds[callee] = []
        self.calleeToArgDefIds[callee].append(argN)

    def addArgDefStartIds(self, callee: str, argN: int):
        self.calleeToDefStartIds[callee] = argN


class ASTDefUseAnalyzer(object):
    def __init__(self):
        self.environmentStack: List[UseDefEnvironment] = list()
        self.useDefsOfBlock: Set[UseOrDef] = set()
        self.calleeInfos: CalleeInfos = CalleeInfos()

    def reset(self):
        self.environmentStack.clear()
        self.useDefsOfBlock.clear()

    def emitUseOrDefs(self, toEmit: List[UseOrDef]):
        for useOrDef in toEmit:
            self.useDefsOfBlock.add(useOrDef)

    # Gets upstream symbols from environment and passes them to
    # parent-environment by calling addChildSymbols on the parent. Asks
    # parent-environment to generate useOrDefs and emit them.
    def reportUpstream(self, env: UseDefEnvironment):
        symbols: List[str] = env.upstreamSymbols()
        astProvider: ASTProvider = env.astProvider

        if len(self.environmentStack) > 0:
            parentEnv: UseDefEnvironment = self.environmentStack[-1]
            parentEnv.addChildSymbols(symbols, astProvider)

    def createArgumentEnvironment(self, astProvider: ASTProvider) -> ArgumentEnvironment:
        argEnv: ArgumentEnvironment = ArgumentEnvironment()
        # 中间还隔着个ArgumentList
        callEnv: CallEnvironment = self.environmentStack[-2]
        # 该参数是否使用指针
        if self.calleeInfos.judgeUse(callEnv, astProvider.getChildNumber()):
            argEnv.setIsUsePointer()
        # 是否定义指针
        if self.calleeInfos.judgeDef(callEnv, astProvider.getChildNumber()):
            argEnv.setIsDefPointer()
        return argEnv

    # Creates a UseDefEnvironment for a given AST node.
    def createUseDefEnvironment(self, astProvider: ASTProvider) -> UseDefEnvironment:
        nodeType: str = astProvider.getTypeAsString()

        if nodeType == "AssignmentExpr":
            return AssignmentEnvironment()
        elif nodeType == "IncDecOp":
            return IncDecEnvironment()
        elif nodeType == "IdentifierDecl" or nodeType == "Parameter":
            return DeclEnvironment()
        elif nodeType == "CallExpression":
            return CallEnvironment()
        elif nodeType == "Argument":
            return self.createArgumentEnvironment(astProvider)
        elif nodeType == "PtrMemberAccess":
            return PtrMemberAccessEnvironment()
        elif nodeType == "MemberAccess":
            return MemberAccessEnvironment()
        # condition和return中只有use没有def
        elif nodeType == "Condition" or nodeType == "ReturnStatement":
            return UseEnvironment()
        elif nodeType == "ArrayIndexing":
            return ArrayIndexingEnvironment()
        elif nodeType == "UnaryOp":
            return UnaryOpEnvironment()
        elif nodeType == "Identifier":
            return IdentifierEnvironment()
        else:
            return UseDefEnvironment()


    def traverseAST(self, astProvider: ASTProvider):
        env: UseDefEnvironment = self.createUseDefEnvironment(astProvider)
        env.astProvider = astProvider
        self.traverseASTChildren(astProvider, env)


    def traverseASTChildren(self, astProvider: ASTProvider, env: UseDefEnvironment):
        numChildren: int = astProvider.getChildCount()
        self.environmentStack.append(env)
        for i in range(numChildren):
            childProvider: ASTProvider = astProvider.getChild(i)
            self.traverseAST(childProvider)
            toEmit: List[UseOrDef] = env.useOrDefsFromSymbols(childProvider)
            self.emitUseOrDefs(toEmit)
        self.environmentStack.pop()
        self.reportUpstream(env)

    def analyzeAST(self, astProvider: ASTProvider) -> Set[UseOrDef]:
        self.reset()
        self.traverseAST(astProvider)
        return self.useDefsOfBlock


class CFGToUDGConverter(object):
    def __init__(self):
        self.astAnalyzer: ASTDefUseAnalyzer = ASTDefUseAnalyzer()

    # statementNode是CFGNode
    def addToUseDefGraph(self, useDefGraph: UseDefGraph, usesAndDefs: List[UseOrDef], statementNode: ASTNode):
        insertedForStatementDef: Set[str] = set()
        insertedForStatementUse: Set[str] = set()

        for useOrDef in usesAndDefs:
            astProvider: ASTNodeASTProvider = useOrDef.astProvider
            # CHECK?
            useOrDefNode: ASTNode = astProvider.node
            if useOrDef.isDef:
                if useOrDef.symbol not in insertedForStatementDef:
                    useDefGraph.addDefinition(useOrDef.symbol, statementNode)
                    insertedForStatementDef.add(useOrDef.symbol)
                # 给ASTNode添加
                if useOrDefNode is not None and useOrDefNode != statementNode:
                    useDefGraph.addDefinition(useOrDef.symbol, useOrDefNode)

            else:
                if useOrDef.symbol not in insertedForStatementUse:
                    useDefGraph.addUse(useOrDef.symbol, statementNode)
                    insertedForStatementUse.add(useOrDef.symbol)
                # Add use-links from AST nodes to symbols
                if useOrDef.astProvider is not None and useOrDefNode is not statementNode:
                    useDefGraph.addUse(useOrDef.symbol, useOrDefNode)

    # 将CFG转化为UDG
    def convert(self, cfg: CFG) -> UseDefGraph:
        # Incrementally create a UseDefGraph by generating
        # UseOrDefs for each statement separately and adding those
        # to the UseDefGraph
        useDefGraph: UseDefGraph = UseDefGraph()
        statements: List[CFGNode] = cfg.vertices

        # CFG中每个语句独立分析
        for cfgNode in statements:
            # skip empty blocks
            if not isinstance(cfgNode, ASTNodeContainer):
                continue
            statementNode: ASTNode = cfgNode.astNode
            provider: ASTNodeASTProvider = ASTNodeASTProvider()
            provider.node = statementNode
            usesAndDefs: List[UseOrDef] = self.astAnalyzer.analyzeAST(provider)
            self.addToUseDefGraph(useDefGraph, usesAndDefs, statementNode)

        return useDefGraph