from typing import List, Dict, Set

class DefUseRelation(object):
    def __init__(self, src: object, dst: object, symbol: str):
        self.src: object = src
        self.dst: object = dst
        self.symbol: str = symbol

    def __eq__(self, other):
        if not isinstance(other, DefUseRelation):
            return False
        return self.src == other.src and self.dst == other.dst and self.symbol == other.symbol

    def __hash__(self):
        return hash(self.symbol)

    def __str__(self):
        return f"{self.src} ----[{self.symbol}]-----{self.dst}"

# Data Dependence Graph
class DDG(object):
    def __init__(self):
        self.defUseEdges: Set[DefUseRelation] = set()

    def add(self, srcId: object, dstId: object, symbol: str):
        statementPair: DefUseRelation = DefUseRelation(srcId, dstId, symbol)
        self.defUseEdges.add(statementPair)

# A CFG decorated with USE and DEFs suitable to determine reaching definitions.
class DefUseCFG(object):
    def __init__(self):
        self.statements: List[object] = list()
        self.symbolsUsed: Dict[object, List[str]] = dict() # key是语句，value是语句中使用的symbol
        self.symbolsDefined: Dict[object, List[str]] = dict() # key是语句，value是语句中定义的symbol
        self.parentBlocks: Dict[object, List[str]] = dict() # key是value的CFG后继结点
        self.childBlocks: Dict[object, List[str]] = dict() # key是value的CFG前驱结点
        self.symbolIds: Dict[str, object] = dict()

        self.exitNode: object = None
        self.parameters: List[str] = list()

    def addStatement(self, statementId: object):
        self.statements.append(statementId)

    def addSymbolUsed(self, key: object, symbol: str):
        if key not in self.symbolsUsed.keys():
            self.symbolsUsed[key] = []
        self.symbolsUsed[key].append(symbol)

    def addSymbolDefined(self, key: object, symbol: str):
        if key not in self.symbolsDefined.keys():
            self.symbolsDefined[key] = []
        self.symbolsDefined[key].append(symbol)

    def addParentBlock(self, thisBlockId: object, parentId: object):
        if thisBlockId not in self.parentBlocks.keys():
            self.parentBlocks[thisBlockId] = []
        self.parentBlocks[thisBlockId].append(parentId)

    def addChildBlock(self, thisBlockId: object, childId: object):
        if thisBlockId not in self.childBlocks.keys():
            self.childBlocks[thisBlockId] = []
        self.childBlocks[thisBlockId].append(childId)

    def setSetSymbolId(self, symbolCode: str, symbolId: object):
        self.symbolIds[symbolCode] = symbolId

    def addUsesForExitNode(self):
        for symbol in self.parameters:
            self.addSymbolUsed(self.exitNode, "* " + symbol)