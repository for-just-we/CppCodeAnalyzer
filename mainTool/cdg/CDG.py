from mainTool.cdg.DominatorTree import *

# 控制依赖边，连接CFG结点
class CDGEdge(Edge[CFGNode]):
    def __init__(self, source: CFGNode, destination: CFGNode):
        super(CDGEdge, self).__init__(source, destination)

    def getProperties(self) -> Dict[str, object]:
        return None

    def __str__(self):
        return str(self.source) + " ==[]==> " + str(self.destination)


# 逆向控制流图
class ReverseCFG(AbstractTwoWayGraph[CFGNode]):
    def __init__(self):
        super(ReverseCFG, self).__init__()
        self.entry: CFGNode = None
        self.exit: CFGNode = None

    @staticmethod
    def newInstance(cfg: CFG):
        reverseCFG: ReverseCFG = ReverseCFG()
        for vertex in cfg.vertices:
            reverseCFG.addVertex(vertex)

        for edge in cfg.getEdges():
            reverseEdge: CFGEdge = CFGEdge(edge.destination, edge.source, edge.label)
            reverseCFG.addEdge(reverseEdge)
        reverseCFG.entry = cfg.exit
        reverseCFG.exit = cfg.entry

        augmentedEdge: CFGEdge = CFGEdge(reverseCFG.entry, reverseCFG.exit, CFGEdgeType.EMPTY_LABEL)
        reverseCFG.addEdge(augmentedEdge)
        return reverseCFG

# 控制依赖图定义
class CDG(AbstractGraph[CFGNode]):
    def __init__(self):
        super(CDG, self).__init__()
        self.dominatorTree: DominatorTree[CFGNode] = None

    # 根据支配树建立控制依赖图
    @staticmethod
    def newInstance(dominatorTree: DominatorTree[CFGNode]):
        cdg: CDG = CDG()
        cdg.dominatorTree = dominatorTree
        for vertex in dominatorTree.getVertices():
            frontier: Set[CFGNode] = dominatorTree.dominanceFrontier(vertex)
            if frontier is not None:
                cdg.addVertex(vertex)
                for f in frontier:
                    # 跳过entry和自我依赖的情况
                    if f == vertex or str(f) == "[ENTRY]":
                        continue
                    cdg.addVertex(f)
                    cdg.addEdge(CDGEdge(f, vertex))
        return cdg


def createCDG(cfg: CFG) -> CDG:
    # 建立逆向CFG
    reverseCFG: ReverseCFG = ReverseCFG.newInstance(cfg)
    # 根据逆向CFG构建支配树
    dominatorTreeCreator: DominatorTreeCreator[CFGNode] = DominatorTreeCreator[CFGNode](reverseCFG, reverseCFG.entry)
    dominatorTree: DominatorTree[CFGNode] = dominatorTreeCreator.create()
    # 基于支配树创建CDG
    return CDG.newInstance(dominatorTree)