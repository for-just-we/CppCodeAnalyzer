from abc import abstractmethod
from typing import List, TypeVar, Generic, Dict

T = TypeVar('T')

class Edge(Generic[T]):
    def __init__(self, source: T, destination: T):
        self.source: T = source
        self.destination: T = destination

    @abstractmethod
    def getProperties(self) -> Dict[str, object]:
        pass

    def __eq__(self, o: object) -> bool:
        if o is None:
            return False
        if id(self) == id(o):
            return True
        if not isinstance(o, Edge):
            return False
        return self.destination == o.destination and self.source == o.source

    def __hash__(self) -> int:
        prime: int = 31
        result: int = 1
        result = prime * result + hash(self.destination)
        result = prime * result + hash(self.source)
        return result


class AbstractGraph(Generic[T]):
    def __init__(self):
        self.vertices: List[T] = list()
        self.outNeighborhood: Dict[T, List[Edge[T]]] = dict()

    def __iter__(self):
        return iter(self.vertices)

    def getEdges(self) -> List[Edge[T]]:
        edges: List[Edge[T]] = list()
        for v, e in self.outNeighborhood.items():
            edges.extend(e)
        return edges

    def outDegree(self, vertex: T) -> int:
        return len(self.outNeighborhood.get(vertex, []))

    def addVertex(self, vertex: T) -> bool:
        if not self.vertices.__contains__(vertex):
            self.vertices.append(vertex)
            return True
        return False

    def addEdge(self, edge: Edge[T]):
        if edge.source in self.outNeighborhood.keys():
            self.outNeighborhood[edge.source].append(edge)
        else:
            self.outNeighborhood[edge.source] = [edge]

    def removeEdge(self, src: T, dst: T):
        edges: List[Edge[T]] = self.outNeighborhood[src]
        for edge in edges:
            if edge.destination == dst:
                edges.remove(edge)

    def removeEdgesFrom(self, source: T):
        self.outNeighborhood.pop(source)

    def removeEdgesTo(self, destination: T):
        for src, edges in self.outNeighborhood.items():
            for edge in edges:
                if edge.destination == destination:
                    edges.remove(edge)

    def totalEdgeNum(self) -> int:
        size: int = 0
        for src, edges in self.outNeighborhood.items():
            size += len(edges)
        return size

    def __str__(self) -> str:
        res: str = f"Graph with {len(self.vertices)} vertices and {self.totalEdgeNum()} edges:\n"
        for vertex in self.vertices:
            res += str(vertex) + '\n'
            for edge in self.outNeighborhood[vertex]:
                res += str(edge) + '\n'
        return res

class AbstractTwoWayGraph(AbstractGraph[T]):
    # 保存node -> ingoing edge
    def __init__(self):
        super(AbstractTwoWayGraph, self).__init__()
        self.inNeighborhood: Dict[T, List[Edge[T]]] = dict()

    def inDegree(self, vertex: T) -> int:
        return len(self.inNeighborhood.get(vertex, []))

    def addEdge(self, edge: Edge[T]):
        super().addEdge(edge)
        if edge.destination in self.inNeighborhood.keys():
            self.inNeighborhood[edge.destination].append(edge)
        else:
            self.inNeighborhood[edge.destination] = [edge]

    def removeEdgesFrom(self, source: T):
        for edge in self.outNeighborhood[source]:
            self.inNeighborhood[edge.destination].remove(edge)
        super().removeEdgesFrom(source)

    def removeEdgesTo(self, destination: T):
        for edge in self.inNeighborhood[destination]:
            self.outNeighborhood[edge.source].remove(edge)
        self.inNeighborhood.pop(destination)

    def removeEdge(self, src: T, dst: T):
        super().removeEdge(src, dst)
        edges: List[Edge[T]] = self.inNeighborhood[dst]
        for edge in edges:
            if edge.source == src:
                edges.remove(edge)

# 后序广度优先遍历逆向CFG
class PostorderIterator(Generic[T]):
    def __init__(self, graph: AbstractGraph[T], root: T):
        self.graph = graph
        self.remainingNodes: List[T] = [root]
        self.visitedNodes: List[T] = list()

    def __iter__(self):
        return self

    def hasNext(self) -> bool:
        return len(self.remainingNodes) > 0

    def __next__(self):
        while self.hasNext():
            root: T = self.remainingNodes[-1]
            # visit root
            if not root in self.visitedNodes:
                self.visitedNodes.append(root)
            # predecessors first if any
            if self.graph.outDegree(root) > 0:
                for edge in self.graph.outNeighborhood.get(root, []):
                    if not edge.destination in self.visitedNodes:
                        self.remainingNodes.append(edge.destination)
                        # 深度优先，1个就够了
                        break

            # 没有后续结点或者后续结点都已经被访问过了
            if self.remainingNodes[-1] == root:
                return self.remainingNodes.pop()
        raise StopIteration()