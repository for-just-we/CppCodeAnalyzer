from mainTool.ddg.DefUseGraph import *
from mainTool.udg.useDefGraph import *
from mainTool.cfg.CFG import *
from mainTool.ast.declarations.complexDecls import Parameter

class CFGAndUDGToDefUseCFG(object):

    def initializeStatements(self, cfg: CFG, defUseCFG: DefUseCFG):
        for statement in cfg.vertices:
            if isinstance(statement, ASTNodeContainer):
                statement = statement.astNode
            defUseCFG.addStatement(statement)


    def initializeParentsAndChildren(self, cfg: CFG, defUseCFG: DefUseCFG):
        for edge in cfg.getEdges():
            src = edge.source
            dst = edge.destination
            if isinstance(src, ASTNodeContainer):
                src = src.astNode
            if isinstance(dst, ASTNodeContainer):
                dst = dst.astNode
            defUseCFG.addChildBlock(src, dst)
            defUseCFG.addParentBlock(dst, src)


    def initializeDefUses(self, udg: UseDefGraph, defUseCFG: DefUseCFG):
        useDefDict: Dict[str, List[UseOrDefRecord]] = udg.useOrDefRecordTable
        for symbol, defUseRecords in useDefDict.items():
            for record in defUseRecords:
                if not record.astNode.isInCFG:
                    continue
                if record.isDef:
                    defUseCFG.addSymbolDefined(record.astNode, symbol)
                else:
                    defUseCFG.addSymbolUsed(record.astNode, symbol)


    def convert(self, cfg: CFG, udg: UseDefGraph) -> DefUseCFG:
        defUseCFG: DefUseCFG = DefUseCFG()
        self.initializeStatements(cfg, defUseCFG)
        self.initializeDefUses(udg, defUseCFG)

        parameters: List[str] = list()
        for parameterCFGNode in cfg.parameters:
            astNode: Parameter = parameterCFGNode.astNode
            # 参数名称
            symbol: str = astNode.name.getEscapedCodeStr()
            parameters.append(symbol)

        defUseCFG.exitNode = cfg.exit
        defUseCFG.parameters = parameters
        defUseCFG.addUsesForExitNode()
        self.initializeParentsAndChildren(cfg, defUseCFG)

        return defUseCFG


class Definition(object):
    def __init__(self, aStatement: object, aIdentifier: str):
        self.statement: object = aStatement
        self.identifier: str = aIdentifier


class DDGCreator(object):
    def __init__(self):
        self.cfg: DefUseCFG = None
        self.In: Dict[object, Set[object]] = dict() # in集合
        self.Out: Dict[object, Set[object]] = dict() # out集合
        self.Gen: Dict[object, Set[object]] = dict() # gen集合
        self.changedNodes: List[object] = list()

    def clear(self):
        self.cfg = None
        self.In.clear()
        self.Out.clear()
        self.Gen.clear()
        self.changedNodes.clear()

    def initOut(self):
        for statement in self.cfg.statements:
            # this has the nice side-effect that an empty hash is created for the statement.
            self.Out[statement] = set()
            symsDefined: List[str] = self.cfg.symbolsDefined.get(statement, [])
            for s in symsDefined:
                self.Out[statement].add(Definition(statement, s))

    def initGenFromOut(self):
        for statement in self.cfg.statements:
            for o in self.Out.get(statement, {}):
                if statement not in self.Gen.keys():
                    self.Gen[statement] = set()
                self.Gen[statement].add(o)

    #Reaching-Def info初始化
    def initReachingDefs(self):
        self.initOut()
        self.initGenFromOut()
        self.changedNodes.append(self.cfg.statements[0]) # entry
        for statement in self.cfg.statements[2:]:
            self.changedNodes.append(statement)
        self.changedNodes.append(self.cfg.statements[1])  # exit

    def updateIn(self, x: object):
        parents: List[object] = self.cfg.parentBlocks.get(x, None)
        if parents is None:
            return

        self.In[x] = set()
        # in(x) = union(out(p))_{p in parents(x)}
        for parent in parents:
            parentOut: Set[object] = self.Out.get(parent, {})
            self.In[x].update(parentOut)

    def updateOut(self, x: object) -> bool:
        listForKey: Set[object] = self.Out.get(x)
        oldOut: Set[object] = listForKey.copy()
        self.Out[x] = set()

        # out(x) = in(x)
        inForX: Set[object] = self.In.get(x, {})
        self.Out[x].update(inForX)

        # out(x) = out(x) - kill(x)
        killX: List[str] = self.cfg.symbolsDefined.get(x, None)
        if killX is not None:
            outItems: Set[object] = self.Out.get(x)
            deleteItems: Set[object] = set()
            for item in outItems:
                if item.identifier in killX:
                    deleteItems.add(item)

            outItems.difference_update(deleteItems)

        # gen(x) \cup  out(x)
        genX: Set[object] = self.Gen.get(x, {})
        self.Out[x].update(genX)

        difference = self.Out[x] == oldOut
        return not difference


    def popFromChangedNodes(self) -> object:
        x: object = next(iter(self.changedNodes))
        self.changedNodes.remove(x)
        return x

    # Reaching Def Analysis
    def calculateReachingDefs(self):
        self.initReachingDefs()

        while len(self.changedNodes) > 0:
            currentBlock: object = self.popFromChangedNodes()
            self.updateIn(currentBlock) # in(x) = out(p) + out(p1) .....
            changed: bool = self.updateOut(currentBlock) # out(x) = gen(x) + in(x) - kill(x)

            if not changed:
                continue
            # 更新的话添加后继结点
            children: List[object] = self.cfg.childBlocks.get(currentBlock, [])
            self.changedNodes.extend(children)


    def createDDGFromReachingDefs(self) -> DDG:
        ddg: DDG = DDG()
        for statement in self.cfg.statements:
            inForBlock: Set[object] = self.In.get(statement, None)
            if inForBlock is None:
                continue
            usedSymbols: List[str] = self.cfg.symbolsUsed.get(statement, None)
            if usedSymbols is None:
                continue

            for defi in inForBlock:
                if defi.statement == statement or isinstance(statement, CFGExitNode):
                    continue
                if defi.identifier in usedSymbols:
                    ddg.add(defi.statement, statement, defi.identifier)

        return ddg

    def createForDefUseCFG(self, aCfg: DefUseCFG) -> DDG:
        self.cfg = aCfg
        self.calculateReachingDefs()
        return self.createDDGFromReachingDefs()