from mainTool.cfg.nodes import *
from mainTool.utils.types import CFGEdgeType
from mainTool.ast.declarations.complexDecls import FunctionDef

from mainTool.utils.graphUtils import *

class CFGEdge(Edge[CFGNode]):
    # CFG Edge的label对应 true, false, 空
    def __init__(self, source: CFGNode, destination: CFGNode, label: str = None):
        super(CFGEdge, self).__init__(source, destination)
        if label is None:
            self.label = CFGEdgeType.EMPTY_LABEL
        else:
            self.label = label

    def getProperties(self) -> Dict[str, object]:
        return {
            "flowLabel": self.label
        }

    def __hash__(self) -> int:
        prime = 31
        result = super().__hash__()
        result = prime * result + hash(self.label)
        return result

    def __str__(self):
        return str(self.source) + " ==[" + self.label + "]==> " + str(self.destination)

    def __eq__(self, o: object) -> bool:
        if id(self) == id(o):
            return True
        if not super().__eq__(o):
            return False
        if not isinstance(o, CFGEdge):
            return False
        return self.label == o.label

# 针对一个function的CFG
class CFG(AbstractTwoWayGraph[CFGNode]):
    def __init__(self):
        super(CFG, self).__init__()
        self.entry: CFGEntryNode = CFGEntryNode()
        self.exit: CFGExitNode = CFGExitNode()
        self.addVertex(self.entry)
        self.addVertex(self.exit)
        self.parameters: List[CFGNode] = list()
        self.errorNode: CFGErrorNode = None
        self.name: str = None # 函数名

    def getErrorNode(self):
        if self.errorNode is None:
            self.errorNode = CFGErrorNode()
        return self.errorNode

    def isEmpty(self) -> bool:
        return len(self.vertices) == 2

    # addCFG只是将otherCFG和当前CFG的所有结点和边放到当前CFG中，otherCFG中的结点还没有和当前CFG连通
    def addCFG(self, otherCFG):
        self.addVertices(otherCFG)
        self.addEdges(otherCFG)

    # 合并CFG
    def appendCFG(self, otherCFG):
        self.addCFG(otherCFG)
        if not otherCFG.isEmpty():
            # edge1为当前CFG的ExitNode的入边
            for edge1 in self.inNeighborhood.get(self.exit, []):
                # edge2为otherCFG的EntryNode的出边
                for edge2 in otherCFG.outNeighborhood.get(otherCFG.entry, []):
                    self.addCFGEdge(edge1.source, edge2.destination, edge1.label)
            # 删除当前的Exit结点
            self.removeEdgesTo(self.exit)
            for edge in otherCFG.inNeighborhood.get(otherCFG.exit):
                self.addCFGEdge(edge.source, self.exit, edge.label)

    # 处理if-else，while等情况
    def mountCFG(self, branchNode: CFGNode, mergeNode: CFGNode, cfg, label: str):
        # 在if-else中，cfg为elseBlock对应的CFG，branchNode为condition对应的CFGNode，mergeNode为该Block对应的ExitNode
        # 在while语句中，cfg为whileBody对应的CFG，branchNode和mergeNode为Condition对应的CFGNode
        # 在for语句中,cfg为forBody，branchNode为forCondition，mergeNode为forExpression或者forCondition
        if not cfg.isEmpty():
            self.addCFG(cfg)
            for edge in cfg.outNeighborhood.get(cfg.entry, []):
                self.addCFGEdge(branchNode, edge.destination, label)
            for edge in cfg.inNeighborhood.get(cfg.exit, []):
                self.addCFGEdge(edge.source, mergeNode, edge.label)
        else:
            self.addCFGEdge(branchNode, mergeNode, label)


    def addVertices(self, cfg):
        # 将cfg所有的非Entry和Exit的结点添加到当前CFG
        for vertex in cfg.vertices:
            if not (vertex == cfg.entry or vertex == cfg.exit):
                self.addVertex(vertex)

    def addEdges(self, cfg):
        # 将cfg所有非Entry和Exit的边添加到当前CFG
        for vertex in cfg.vertices:
            for edge in cfg.outNeighborhood.get(vertex, []):
                if not (edge.source == cfg.entry or edge.destination == cfg.exit):
                    self.addEdge(edge)

    def addCFGEdge(self, srcBlock: CFGNode, dstBlock: CFGNode, label: str = None):
        edge: CFGEdge = CFGEdge(srcBlock, dstBlock, label)
        self.addEdge(edge)


class CFGFactory(object):
    # Implement this method for each language
    @staticmethod
    def newInstance(functionDefinition: FunctionDef) -> CFG:
        pass