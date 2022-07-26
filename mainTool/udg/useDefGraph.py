from mainTool.ast.astNode import ASTNode
from mainTool.udg.astProvider import ASTProvider


from typing import List, Dict, Set

# 一个usedef记录，表示某个symbol在该AST中是定义还是使用
class UseOrDefRecord(object):
    def __init__(self, anASTNode: ASTNode, aIsDef: bool):
        self.isDef: bool = aIsDef
        self.astNode: ASTNode = anASTNode

class UseOrDef(object):
    def __init__(self):
        self.isDef: int = None
        self.symbol: str = None
        self.astProvider: ASTProvider = None

    def __eq__(self, other):
        if not isinstance(other, UseOrDef):
            return False
        return self.isDef == other.isDef and self.symbol == other.symbol \
               and self.astProvider == other.astProvider

    def __hash__(self):
        return hash(self.symbol)


class UseDefGraph(object):
    # A UseDefGraph is a table indexed by identifiers. Each table-entry is
    # a list of the UseOrDefRecords of the identifier.
    def __init__(self):
        # 主要成员变量，每个key(symbol)对应1个list [(stetement, def)]
        self.useOrDefRecordTable: Dict[str, List[UseOrDefRecord]] = dict()

    def getUsesAndDefsForSymbol(self, symbol: str) -> List[UseOrDefRecord]:
        return self.useOrDefRecordTable.get(symbol, [])

    def add(self, identifier: str, astNode: ASTNode, isDef: bool):
        record: UseOrDefRecord = UseOrDefRecord(astNode, isDef)
        if identifier in self.useOrDefRecordTable.keys():
            self.useOrDefRecordTable[identifier].append(record)
        else:
            self.useOrDefRecordTable[identifier] = [record]

    def addDefinition(self, identifier: str, astNode: ASTNode):
        self.add(identifier, astNode, True)

    def addUse(self, identifier: str, astNode: ASTNode):
        self.add(identifier, astNode, False)