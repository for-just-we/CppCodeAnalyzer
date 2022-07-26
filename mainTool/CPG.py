# define code property graph
from mainTool.ast.builders import astNodeToJson, json2astNode, FileBuilder, astToSerializedJson, unserializeNode
from mainTool.cfg.CCFG import ASTToCFGConvert
from mainTool.cdg.CDG import *
from mainTool.udg.astAnalyzers import *
from mainTool.ddg.DDGCreator import *

from mainTool.utils.graphUtils import Edge

from mainTool.antlr.CPP14Lexer import CPP14Lexer, InputStream, CommonTokenStream
from mainTool.antlr.CPP14Parser import CPP14Parser
from antlr4.tree.Tree import ParseTree, ParseTreeWalker

import json

class CodeEdge(Edge[int]):
    def __init__(self, source: int, destination: int, property: str = None):
        super(CodeEdge, self).__init__(source, destination)
        self.property = property

    def __str__(self):
        if self.property is None:
            return f"{self.source} ---- {self.destination}"
        return f"{self.source} --[{self.property}]-- {self.destination}"

    def toJson(self):
        datas = [self.source, self.destination]
        if self.property is not None:
            datas.append(self.property)
        return datas

    @classmethod
    def fromJson(cls, datas: list):
        assert len(datas) in { 2, 3 }
        if len(datas) == 3:
            return CodeEdge(datas[0], datas[1], datas[2])
        else:
            return CodeEdge(datas[0], datas[1])

# code property graph for a function
class CPG(object):
    def __init__(self):
        self.statements: List[ASTNode] = list()
        self.statement2Idx: Dict[ASTNode, int] = None

        self.CFGEdges: List[CodeEdge] = list()
        self.CDGEdges: List[CodeEdge] = list()
        self.DDGEdges: List[CodeEdge] = list()

        self.name: str = None # 函数名
        self.file: str = None # function来源的文件名
        self.joinSlice: bool = True # slice的时候是否考虑
        # self.entry: CFGEntryNode = None

    def initCFGEdges(self, cfg: CFG):
        self.name = cfg.name
        nodes: List[ASTNodeContainer] = list(filter(lambda node: isinstance(node, ASTNodeContainer), cfg.vertices))
        nodes.sort(key=lambda node: node.astNode.location)

        self.statements.extend(list(map(lambda node: node.astNode, nodes)))
        self.statement2Idx = { n.astNode: i for i, n in enumerate(nodes)}

        edges: List[Edge[CFGNode]] = list(filter(lambda edge: not (isinstance(edge.source, CFGEntryNode)
                                    or isinstance(edge.destination, CFGExitNode)), cfg.getEdges()))
        self.CFGEdges.extend([CodeEdge(self.statement2Idx[edge.source.astNode], self.statement2Idx[edge.destination.astNode], edge.label)
                              for edge in edges])

        #self.entry: CFGEntryNode = cfg.entry



    def initCDGEdges(self, cdg: CDG):
        edges: List[Edge[CFGNode]] = cdg.getEdges()
        self.CDGEdges.extend(
            [CodeEdge(self.statement2Idx[edge.source.astNode], self.statement2Idx[edge.destination.astNode])
             for edge in edges])
        # self.CDGEdges.extend(
        #     [CodeEdge(-1, self.statement2Idx[edge.destination.astNode])
        #      for edge in edges if isinstance(edge.source, CFGEntryNode)])


    def initDDGEdges(self, ddg: DDG):
        self.DDGEdges.extend([CodeEdge(self.statement2Idx[edge.src], self.statement2Idx[edge.dst], edge.symbol)
                              for edge in ddg.defUseEdges])

    def toJson(self) -> Dict:
        jsonStatements: List[dict] = [astNodeToJson(statement) for statement in self.statements]
        cfgEdges: List[list] = [edge.toJson() for edge in self.CFGEdges]
        cdgEdges: List[list] = [edge.toJson() for edge in self.CDGEdges]
        ddgEdges: List[list] = [edge.toJson() for edge in self.DDGEdges]

        return {
            "fileName": self.file,
            "functionName": self.name,
            "nodes": jsonStatements,
            "cfgEdges": cfgEdges,
            "cdgEdges": cdgEdges,
            "ddgEdges": ddgEdges
        }

    def toSerializedJson(self) -> Dict:
        jsonStatements: List[dict] = [astToSerializedJson(statement) for statement in self.statements]
        serializedCfgEdges: List[str] = [json.dumps(edge.toJson()) for edge in self.CFGEdges]
        serializedCdgEdges: List[str] = [json.dumps(edge.toJson()) for edge in self.CDGEdges]
        serializedDdgEdges: List[str] = [json.dumps(edge.toJson()) for edge in self.DDGEdges]


        return {
            "fileName": self.file,
            "functionName": self.name,
            "nodes": jsonStatements,
            "cfgEdges": serializedCfgEdges,
            "cdgEdges": serializedCdgEdges,
            "ddgEdges": serializedDdgEdges
        }


    @staticmethod
    def fromJson(jsonData: Dict):
        cpg: CPG = CPG()
        cpg.name = jsonData["functionName"]
        cpg.file = jsonData["fileName"]
        cfgEdges: List[CodeEdge] = [CodeEdge.fromJson(edge) for edge in jsonData["cfgEdges"]]
        cdgEdges: List[CodeEdge] = [CodeEdge.fromJson(edge) for edge in jsonData["cdgEdges"]]
        ddgEdges: List[CodeEdge] = [CodeEdge.fromJson(edge) for edge in jsonData["ddgEdges"]]
        cpg.CFGEdges.extend(cfgEdges)
        cpg.CDGEdges.extend(cdgEdges)
        cpg.DDGEdges.extend(ddgEdges)

        stmts: List[ASTNode] = [json2astNode(jsonStmt) for jsonStmt in jsonData["nodes"]]
        cpg.statements.extend(stmts)

        return cpg

    @staticmethod
    def fromSerJson(serJsonData: Dict):
        cfgEdges: List[list] = [json.loads(serEdge) for serEdge in serJsonData["cfgEdges"]]
        cdgEdges: List[list] = [json.loads(serEdge) for serEdge in serJsonData["cdgEdges"]]
        ddgEdges: List[list] = [json.loads(serEdge) for serEdge in serJsonData["ddgEdges"]]
        jsonStatements: List[dict] = [unserializeNode(serStmt) for serStmt in serJsonData["nodes"]]

        json_data: Dict = {
            "fileName": serJsonData["fileName"],
            "functionName": serJsonData["functionName"],
            "nodes": jsonStatements,
            "cfgEdges": cfgEdges,
            "cdgEdges": cdgEdges,
            "ddgEdges": ddgEdges
        }

        return CPG.fromJson(json_data)


def convertASTtoCPG(functionDef: FunctionDef, udgConverter: CFGToUDGConverter, defUseConverter: CFGAndUDGToDefUseCFG,
                    ddgCreator: DDGCreator) -> CPG:
    cfg: CFG = ASTToCFGConvert(functionDef) # CFG
    udgConverter.astAnalyzer.reset()
    useDefGraph: UseDefGraph = udgConverter.convert(cfg) # UDG
    defUseCFG: DefUseCFG = defUseConverter.convert(cfg, useDefGraph) # DefUseCFG
    ddgCreator.clear()
    ddg: DDG = ddgCreator.createForDefUseCFG(defUseCFG) # Data Dependence Graph
    cdg: CDG = createCDG(cfg) # Control Dependence Graph

    # Code Property Graph
    cpg: CPG = CPG()
    cpg.initCFGEdges(cfg)
    cpg.initCDGEdges(cdg)
    cpg.initDDGEdges(ddg)
    cpg.name = cfg.name

    return cpg


def fileParse(fileName: str, udgConverter: CFGToUDGConverter,
              defUseConverter: CFGAndUDGToDefUseCFG, ddgCreator: DDGCreator) -> List[CPG]:
    code = open(fileName, 'r', encoding='utf-8').read()
    inputStream = InputStream(code)
    cpp14Lexer = CPP14Lexer(inputStream)
    tokenStream = CommonTokenStream(cpp14Lexer)
    parser = CPP14Parser(tokenStream)
    walker: ParseTreeWalker = ParseTreeWalker()
    tree: ParseTree = parser.translationunit()
    builder: FileBuilder = FileBuilder()
    walker.walk(builder, tree)

    functions: List[FunctionDef] = builder.functionDefs.copy()
    for classDecl in builder.classDefs:
        functions.extend(classDecl.functionDefs)

    # astAnalyzer: ASTDefUseAnalyzer = ASTDefUseAnalyzer()
    # astAnalyzer.calleeInfos = calleeInfos
    # udgConverter.astAnalyzer = astAnalyzer
    cpgs: List[CPG] = [convertASTtoCPG(functionDef, udgConverter, defUseConverter, ddgCreator)
                       for functionDef in functions]

    return cpgs



def initialCalleeInfos(calleeInfs: Dict) -> CalleeInfos:
    calleeInfos: CalleeInfos = CalleeInfos()

    defInfos = calleeInfs["ArgDef"]
    for funcName, argNs in defInfos.items():
        for argN in argNs:
            calleeInfos.addArgDef(funcName, argN)

    useInfos = calleeInfs["ArgUse"]
    for funcName, argNs in useInfos.items():
        for argN in argNs:
            calleeInfos.addArgUse(funcName, argN)

    startIdsInfos = calleeInfs["ArgDefStartIds"]
    for funcName, argN in startIdsInfos.items():
        calleeInfos.addArgDefStartIds(funcName, argN)

    return calleeInfos