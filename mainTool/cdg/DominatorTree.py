from mainTool.cfg.CFG import *
from typing import Set

# 支配树
class DominatorTree(Generic[T]):
    def __init__(self):
        self.dominators: Dict[T, T] = dict() # key -> value 表示 value 支配 key
        self.dominanceFrontiers: Dict[T, Set[T]] = dict() # 前向支配
        self.postorderEnumeration: Dict[T, int] = dict() # 结点访问顺序

    def getVertices(self) -> List[T]:
        return list(self.dominators.keys())

    def getDominator(self, vertex: T) -> T:
        return self.dominators.get(vertex)

    def dominanceFrontier(self, vertex: T) -> Set[T]:
        return self.dominanceFrontiers.get(vertex, None)

    def hasDominator(self, vertex: T) -> bool:
        return self.dominators.get(vertex, None) is not None

    def contains(self, vertex: T) -> bool:
        return vertex in self.dominators.keys()

    # 往支配树中添加结点
    def addVertex(self, vertex: T):
        if not self.contains(vertex):
            self.dominators[vertex] = None
            return True
        return False

    def setDominator(self, vertex: T, dominator: T) -> bool:
        changed: bool = False
        if self.contains(vertex):
            currentDominator: T = self.dominators.get(vertex)
            if currentDominator is None and dominator is not None:
                self.dominators[vertex] = dominator
                changed = True
            elif not currentDominator == dominator:
                self.dominators[vertex] = dominator
                changed = True
            else:
                changed = False
        return changed

    def commonDominator(self, vertex1: T, vertex2: T) -> T:
        finger1: T = vertex1
        finger2: T = vertex2
        while not finger1 == finger2:
            while self.postorderEnumeration.get(finger1) < self.postorderEnumeration.get(finger2):
                finger1 = self.getDominator(finger1)
            while self.postorderEnumeration.get(finger2) < self.postorderEnumeration.get(finger1):
                finger2 = self.getDominator(finger2)

        return finger1

    def commonDominatorList(self, vertices: List[T]) -> T:
        stack: List[T] = list()
        for vertex in vertices:
            if self.hasDominator(vertex):
                stack.append(vertex)

        if len(stack) == 0:
            return None
        while len(stack) > 1:
            stack.append(self.commonDominator(stack.pop(), stack.pop()))
        return stack.pop()


class DominatorTreeCreator(Generic[T]):
    def __init__(self, graph: AbstractTwoWayGraph[T], startNode: T):
        self.graph: AbstractTwoWayGraph[T] = graph # 逆向CFG
        self.startNode: T = startNode # 一般是逆向CFG EntryNode
        self.dominatorTree: DominatorTree[T] = DominatorTree[T]()
        self.orderedVertices: List[T] = list() # 存储逆向CFG结点访问顺序

    # 获取逆向CFG结点访问顺序
    def enumerateVertices(self):
        counter: int = 0
        iterator: PostorderIterator[T] = PostorderIterator[T](self.graph, self.startNode)

        while iterator.hasNext():
            vertex: T = iterator.__next__()
            self.orderedVertices.append(vertex)
            self.dominatorTree.postorderEnumeration[vertex] = counter
            counter += 1

        if len(self.orderedVertices) < len(self.graph.vertices):
            print("warning: incomplete control flow graph")

    # 初始化支配树
    def initializeDominatorTree(self):
        self.dominatorTree.addVertex(self.startNode)
        self.dominatorTree.setDominator(self.startNode, self.startNode)

    def buildDominatorTree(self):
        changed: bool = True
        while changed:
            changed = False
            # orderedVertices存储结点访问顺序
            reverseVertexIterator = list(reversed(self.orderedVertices))
            cur = 1
            while cur < len(reverseVertexIterator):
                currentNode: T = reverseVertexIterator[cur]
                cur += 1
                lis: List[T] = list()
                for edge in self.graph.inNeighborhood.get(currentNode, []):
                    lis.append(edge.source)
                newIdom: T = self.dominatorTree.commonDominatorList(lis)
                self.dominatorTree.addVertex(currentNode)
                if self.dominatorTree.setDominator(currentNode, newIdom):
                    changed = True


    def determineDominanceFrontiers(self):
        for currentNode in self.orderedVertices: # 后序遍历逆向CFG
            if self.graph.inDegree(currentNode) > 1:
                for edge in self.graph.inNeighborhood.get(currentNode, []):
                    predecessor: T = edge.source
                    if not predecessor in self.orderedVertices:
                        continue
                    # runnner序号大于currentNode
                    runner = predecessor
                    while not runner == self.dominatorTree.getDominator(currentNode): # value支配于key
                        if runner not in self.dominatorTree.dominanceFrontiers.keys():
                            self.dominatorTree.dominanceFrontiers[runner] = set()
                        self.dominatorTree.dominanceFrontiers[runner].add(currentNode)
                        runner = self.dominatorTree.getDominator(runner)

    def create(self):
        # 获取逆向CFG结点访问顺序
        self.enumerateVertices()
        # 初始化
        self.initializeDominatorTree()
        # 构建支配树
        self.buildDominatorTree()
        # 控制依赖边计算
        self.determineDominanceFrontiers()
        return self.dominatorTree