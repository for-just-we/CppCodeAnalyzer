from mainTool.ast.statements.jumps import ReturnStatement
from extraTools.vuldetect.utils.sinkPoint import CallExprTool, XFGPoint
from extraTools.vuldetect.utils.symbolized import SymbolizingTool
from mainTool.CPG import *
from typing import List, Set, Tuple
import json

# generating xfg defined in DeepWuKong
# following paper DeepWukong: Statically Detecting Software Vulnerabilities Using Deep Graph Neural Network

class XFG(object):
    def __init__(self, keyLine: List[int], keyContent: str):
        # control dependence edges
        self.cdes: List[CodeEdge] = list()
        # data dependence edges
        self.ddes: List[CodeEdge] = list()
        # key line 行号,文件Id
        self.keyLine: List[int] = keyLine
        # 内容
        # slice覆盖到的行号以及每一行所在的文件
        self.lineNumbers: List[List[int]] = list()
        self.keyLineContent: str = keyContent
        # 文件id对文件名
        self.id2file: Dict[int, str] = None
        # slice中每个语句对应的token序列
        self.lineContents: List[str] = list()

    def __hash__(self):
        return hash(json.dumps(self.lineContents))

    def toJson(self) -> Dict:
        return {
            "keyline": self.keyLine,
            "id2file": self.id2file,
            "line-Nos": self.lineNumbers,
            "line-contents": self.lineContents,
            "control-dependences": [edge.toJson() for edge in self.cdes],
            "data-dependences": [edge.toJson() for edge in self.ddes]
        }


# 一个程序中所有function都由一个SliceTool对象处理
# cpgs is all cpgs from functions of a program (could be a file sometimes)
class XFGSliceTool(object):
    def __init__(self, cpgs: List[CPG], sensitive_apis: Set[str], symbolizingTool: SymbolizingTool):
        self.cpgs: List[CPG] = cpgs
        self.funcName2cpg: Dict[str, CPG] = {cpg.name: cpg for cpg in cpgs}
        self.sensitive_apis: Set[str] = sensitive_apis #
        self.symbolizingTool: SymbolizingTool = symbolizingTool

        self.slices: Set[XFG] = set() # store all code gadgets of a program
        # backward information of data-deoendence for each statement
        self.funcName2backDataInfo: Dict[str, Dict[int, Set[int]]] = dict()
        # forward information of data-deoendence for each statement
        self.funcName2forwDataInfo: Dict[str, Dict[int, Set[int]]] = dict()
        # backward information of control-deoendence for each statement
        self.funcName2backControlInfo: Dict[str, Dict[int, Set[int]]] = dict()
        # forward information of control-deoendence for each statement
        self.funcName2forwControlInfo: Dict[str, Dict[int, Set[int]]] = dict()
        # 将文件名映射
        self.files: List[str] = list()
        for cpg in self.cpgs:
            self.generateForAndBackInfos(cpg)
            if cpg.file not in self.files:
                self.files.append(cpg.file)
        self.file2Id: Dict[str, int] = { file: i for i, file in enumerate(self.files) }



    def generateForAndBackInfos(self, cpg: CPG):
        # backward
        backDataInfo: Dict[int, Set[int]] = dict()
        # forward
        forwDataInfo: Dict[int, Set[int]] = dict()

        # forward and backward for data dependence
        for edge in cpg.DDGEdges:
            # backward
            if edge.destination not in backDataInfo.keys():
                backDataInfo[edge.destination] = set()
            backDataInfo[edge.destination].add(edge.source)
            # forward
            if edge.source not in forwDataInfo.keys():
                forwDataInfo[edge.source] = set()
            forwDataInfo[edge.source].add(edge.destination)

        self.funcName2backDataInfo[cpg.name] = backDataInfo
        self.funcName2forwDataInfo[cpg.name] = forwDataInfo

        # backward
        backControlInfo: Dict[int, Set[int]] = dict()
        # forward
        forwControlInfo: Dict[int, Set[int]] = dict()

        # forward and backward for control dependence
        for edge in cpg.CDGEdges:
            # backward
            if edge.destination not in backControlInfo.keys():
                backControlInfo[edge.destination] = set()
            backControlInfo[edge.destination].add(edge.source)
            # forward
            if edge.source not in forwControlInfo.keys():
                forwControlInfo[edge.source] = set()
            forwControlInfo[edge.source].add(edge.destination)

        self.funcName2backControlInfo[cpg.name] = backControlInfo
        self.funcName2forwControlInfo[cpg.name] = forwControlInfo


    def generateSliceForProgram(self):
        sinkTool: XFGPoint = XFGPoint(self.sensitive_apis)
        slicesCpg = list(filter(lambda cpg: cpg.joinSlice, self.cpgs))
        for cpg in slicesCpg:
            for i, stmt in enumerate(cpg.statements):
                # 是否算SySe
                if sinkTool.judgeSink(stmt):
                    coveredFileIds: Set[int] = set()
                    lineNumber: int = stmt.location.startLine
                    xfg: XFG = XFG([lineNumber, self.file2Id[cpg.file]], stmt.getEscapedCodeStr())

                    backwardFunctionChain: List[str] = list()  # store function call chain in backward slices
                    backwardCDEdges: List[Edge[ASTNode]] = list() # store control dependence edges
                    backwardDDEdges: List[Edge[ASTNode]] = list()  # store data dependence edges
                    backwardLineContents: List[ASTNode] = list()
                    backwardLineInfo: List[List[int]] = list()
                    backwardIdxs: List[int] = [i]
                    self.generateBackwardSlice(cpg.name, backwardIdxs, backwardLineContents, backwardFunctionChain,
                                       backwardLineInfo, backwardCDEdges, backwardDDEdges, coveredFileIds)

                    forwardFunctionChain: List[str] = list()  # store function call chain in backward slices
                    forwardCDEdges: List[Edge[ASTNode]] = list()  # store control dependence edges
                    forwardDDEdges: List[Edge[ASTNode]] = list()  # store data dependence edges
                    forwardLineContents: List[ASTNode] = list()
                    forwardLineInfo: List[List[int]] = list()
                    forwardIdxs: List[int] = [i]
                    self.generateForwardSlice(cpg.name, forwardIdxs, forwardLineContents, forwardFunctionChain,
                                       forwardLineInfo, forwardCDEdges, forwardDDEdges, coveredFileIds)

                    idx = forwardLineContents.index(stmt)
                    forwardLineContents.pop(idx)
                    forwardLineInfo.pop(idx)
                    lines = backwardLineInfo + forwardLineInfo
                    contents = backwardLineContents + forwardLineContents
                    lineInfos = list()

                    for lineCont in zip(lines, contents):
                        lineInfos.append((lineCont[0][1], lineCont[0][0], lineCont[1]))

                    # XFG中的内容，先按文件Id排序，再按行号排序
                    lineInfos.sort(key=lambda x: x[1])
                    lineInfos.sort(key=lambda x: x[0])

                    astNode2idx: Dict[ASTNode, int] = dict()

                    for i, lineInfo in enumerate(lineInfos):
                        xfg.lineNumbers.append([lineInfo[1], lineInfo[0]])
                        xfg.lineContents.append(self.symbolizingTool.symbolize(
                            lineInfo[2].getEscapedCodeStr()))
                        astNode2idx[lineInfo[2]] = i

                    cdEdgeSet: Set[Tuple[int, int]] = set()
                    cdEdges = backwardCDEdges + forwardCDEdges
                    for edge in cdEdges:
                        cdEdgeSet.add((astNode2idx[edge.source], astNode2idx[edge.destination]))
                    for edge in cdEdgeSet:
                        xfg.cdes.append(CodeEdge(edge[0], edge[1]))

                    xfg.cdes.sort(key=lambda edge: edge.destination)
                    xfg.cdes.sort(key=lambda edge: edge.source)

                    ddEdgeSet: Set[Tuple[int, int]] = set()
                    ddEdges = backwardDDEdges + forwardDDEdges
                    for edge in ddEdges:
                        ddEdgeSet.add((astNode2idx[edge.source], astNode2idx[edge.destination]))
                    for edge in ddEdgeSet:
                        xfg.ddes.append(CodeEdge(edge[0], edge[1]))

                    xfg.ddes.sort(key=lambda edge: edge.destination)
                    xfg.ddes.sort(key=lambda edge: edge.source)
                    xfg.id2file = {fileId: self.files[fileId] for fileId in coveredFileIds}
                    self.slices.add(xfg)




    def generateBackwardSlice(self, functionName: str, sliceIdxs: List[int], slices: List[ASTNode],
                      functionChain: List[str], sliceLines: List[List[int]], cdEdges: List[Edge[ASTNode]],
                      ddEdges: List[Edge[ASTNode]], coveredFileIds: Set[int]):
        if functionName in functionChain:
            return
        # sliceIdxs stores all indexes of nodes of slices
        cpg: CPG = self.funcName2cpg[functionName]
        functionChain.append(functionName)
        # computes all nodes with program-dependence with startIdx in a single function first
        dataInfo: Dict[int, Set[int]] = self.funcName2backDataInfo[functionName]
        controlInfo: Dict[int, Set[int]] = self.funcName2backControlInfo[functionName]

        workList: List[int] = sliceIdxs.copy()
        while len(workList) > 0:
            curIdx: int = workList.pop(0)
            # data dependence
            for o in dataInfo.get(curIdx, set()):
                edge = Edge(cpg.statements[o], cpg.statements[curIdx])
                if edge not in ddEdges:
                    ddEdges.append(edge)
                if o not in sliceIdxs:
                    sliceIdxs.append(o)
                    workList.append(o)
            # control dependence
            for o in controlInfo.get(curIdx, set()):
                edge = Edge(cpg.statements[o], cpg.statements[curIdx])
                if edge not in cdEdges:
                    cdEdges.append(edge)
                if o not in sliceIdxs:
                    sliceIdxs.append(o)
                    workList.append(o)

        coveredFileIds.add(self.file2Id[cpg.file])
        sliceIdxs.sort()
        for id in sliceIdxs:
            # 添加slice行代码
            slices.append(cpg.statements[id])
            # 添加slice行行号和文件id
            sliceLines.append([cpg.statements[id].location.startLine, self.file2Id[cpg.file]])
            callTool = CallExprTool()
            callTool.judgeCall(cpg.statements[id])
            if callTool.functionName is not None and callTool.functionName in self.funcName2cpg.keys():
                otherCpg: CPG = self.funcName2cpg[callTool.functionName]
                # 以前面一行代码的return语句为起点反向遍历
                assert isinstance(otherCpg.statements[-1], ReturnStatement)
                newStartIdxs: List[int] = [len(otherCpg.statements) - 1]
                self.generateBackwardSlice(otherCpg.name, newStartIdxs, slices, functionChain, sliceLines,
                                           cdEdges, ddEdges, coveredFileIds)


    def generateForwardSlice(self, functionName: str, sliceIdxs: List[int], slices: List[ASTNode],
                      functionChain: List[str], sliceLines: List[List[int]], cdEdges: List[Edge[ASTNode]],
                      ddEdges: List[Edge[ASTNode]], coveredFileIds: Set[int]):
        if functionName in functionChain:
            return
        # sliceIdxs stores all indexes of nodes of slices
        cpg: CPG = self.funcName2cpg[functionName]
        functionChain.append(functionName)
        # computes all nodes with program-dependence with startIdx in a single function first
        dataInfo: Dict[int, Set[int]] = self.funcName2forwDataInfo[functionName]
        controlInfo: Dict[int, Set[int]] = self.funcName2forwControlInfo[functionName]

        workList: List[int] = sliceIdxs.copy()
        while len(workList) > 0:
            curIdx: int = workList.pop(0)
            # data dependence
            for o in dataInfo.get(curIdx, set()):
                edge = Edge(cpg.statements[curIdx], cpg.statements[o])
                if edge not in ddEdges:
                    ddEdges.append(edge)
                if o not in sliceIdxs:
                    ddEdges.append(edge)
                    sliceIdxs.append(o)
                    workList.append(o)
            # control dependence
            for o in controlInfo.get(curIdx, set()):
                edge = Edge(cpg.statements[curIdx], cpg.statements[o])
                if edge not in cdEdges:
                    cdEdges.append(edge)
                if o not in sliceIdxs:
                    cdEdges.append(edge)
                    sliceIdxs.append(o)
                    workList.append(o)

        coveredFileIds.add(self.file2Id[cpg.file])
        sliceIdxs.sort()
        for id in sliceIdxs:
            # 添加slice行代码
            slices.append(cpg.statements[id])
            # 添加slice行行号和文件id
            sliceLines.append([cpg.statements[id].location.startLine, self.file2Id[cpg.file]])
            callTool = CallExprTool()
            callTool.judgeCall(cpg.statements[id])
            if callTool.functionName is not None and callTool.functionName in self.funcName2cpg.keys():
                otherCpg: CPG = self.funcName2cpg[callTool.functionName]
                # 以前面一行代码的parameter语句为起点反向遍历
                assert callTool.argNum > 0
                newStartIdxs: List[int] = list(range(callTool.argNum))
                self.generateForwardSlice(otherCpg.name, newStartIdxs, slices, functionChain, sliceLines,
                                           cdEdges, ddEdges, coveredFileIds)