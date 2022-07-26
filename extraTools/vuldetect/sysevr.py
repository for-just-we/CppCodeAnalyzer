from mainTool.ast.statements.jumps import ReturnStatement
from extraTools.vuldetect.utils.sinkPoint import SyVCPoint, CallExprTool
from extraTools.vuldetect.utils.symbolized import SymbolizingTool
from mainTool.CPG import *
from typing import List, Set
import json



class SySeSlice(object):
    def __init__(self, keyLine: List[int], keyContent: str):
        # slice覆盖到的行号以及每一行所在的文件
        self.lineNumbers: List[List[int]] = list()
        # slice中每个语句对应的token序列
        self.lineContents: List[str] = list()
        # key line 行号,文件Id
        self.keyLine: List[int] = keyLine
        # 内容
        self.keyLineContent: str = keyContent
        # 文件id对文件名
        self.id2file: Dict[int, str] = None

    def __hash__(self):
        return hash(json.dumps(self.lineContents))

    def toJson(self) -> Dict:
        return {
            "keyline": self.keyLine,
            "id2file": self.id2file,
            "line-Nos": self.lineNumbers,
            "line-contents": self.lineContents
        }


# 一个程序中所有function都由一个SliceTool对象处理
# cpgs is all cpgs from functions of a program (could be a file sometimes)
class SySeSliceTool(object):
    def __init__(self, cpgs: List[CPG], sensitive_apis: Set[str], symbolizingTool: SymbolizingTool):
        self.cpgs: List[CPG] = cpgs
        self.funcName2cpg: Dict[str, CPG] = {cpg.name: cpg for cpg in cpgs}
        self.sensitive_apis: Set[str] = sensitive_apis #
        self.symbolizingTool: SymbolizingTool = symbolizingTool

        self.slices: Set[SySeSlice] = set() # store all code gadgets of a program
        # backward information of control- data-deoendence for each statement
        self.funcName2backInfo: Dict[str, Dict[int, Set[int]]] = dict()
        # forward information of data-deoendence for each statement
        self.funcName2forwInfo: Dict[str, Dict[int, Set[int]]] = dict()
        # 将文件名映射
        self.files: List[str] = list()
        for cpg in self.cpgs:
            self.generateForAndBackInfos(cpg)
            if cpg.file not in self.files:
                self.files.append(cpg.file)

        self.file2Id: Dict[str, int] = { file: i for i, file in enumerate(self.files) }



    def generateForAndBackInfos(self, cpg: CPG):
        # backward
        backInfo: Dict[int, Set[int]] = dict()
        # forward
        forwInfo: Dict[int, Set[int]] = dict()

        # backward for control dependence
        for edge in cpg.CDGEdges:
            if edge.destination not in backInfo.keys():
                backInfo[edge.destination] = set()
            backInfo[edge.destination].add(edge.source)

        # forward and backward for data dependence
        for edge in cpg.DDGEdges:
            # backward
            if edge.destination not in backInfo.keys():
                backInfo[edge.destination] = set()
            backInfo[edge.destination].add(edge.source)
            # forward
            if edge.source not in forwInfo.keys():
                forwInfo[edge.source] = set()
            forwInfo[edge.source].add(edge.destination)

        self.funcName2backInfo[cpg.name] = backInfo
        self.funcName2forwInfo[cpg.name] = forwInfo


    def generateSliceForProgram(self):
        sinkTool: SyVCPoint = SyVCPoint(self.sensitive_apis)
        slicesCpg = list(filter(lambda cpg: cpg.joinSlice, self.cpgs))
        for cpg in slicesCpg:
            for i, stmt in enumerate(cpg.statements):
                # 是否算SySe
                if sinkTool.judgeSink(stmt):
                    coveredFileIds: Set[int] = set()
                    lineNumber: int = stmt.location.startLine
                    slice: SySeSlice = SySeSlice([lineNumber, self.file2Id[cpg.file]], stmt.getEscapedCodeStr())

                    backwardFunctionChain: List[str] = list() # store function call chain in backward slices
                    backwardLineContents: List[str] = list()
                    backwardLineInfo: List[List[int]] = list()
                    backwardIdxs: List[int] = [i]
                    self.generateSlice(cpg.name, backwardIdxs, backwardLineContents, backwardFunctionChain,
                                       backwardLineInfo, coveredFileIds, True)

                    forwardFunctionChain: List[str] = list()  # store function call chain in backward slices
                    forwardLineContents: List[str] = list()
                    forwardLineInfo: List[List[int]] = list()
                    forwardIdxs: List[int] = [i]
                    self.generateSlice(cpg.name, forwardIdxs, forwardLineContents, forwardFunctionChain,
                                       forwardLineInfo, coveredFileIds, False)

                    slice.lineNumbers.extend(backwardLineInfo)
                    slice.lineContents.extend(backwardLineContents)

                    idx = forwardLineContents.index(stmt)
                    forwardLineContents.pop(idx)
                    forwardLineInfo.pop(idx)
                    slice.lineNumbers.extend(forwardLineInfo)
                    slice.lineContents.extend(forwardLineContents)

                    slice.id2file = { fileId: self.files[fileId] for fileId in coveredFileIds }

                    self.slices.add(slice)


    def generateSlice(self, functionName: str, sliceIdxs: List[int], slices: List[str],
                              functionChain: List[str], sliceLines: List[List[int]],
                      coveredFileIds: Set[int], backward: bool=True ):
        if functionName in functionChain:
            return

        functionChain.append(functionName)
        # computes all nodes with program-dependence with startIdx in a single function first
        if backward:
            Info: Dict[int, Set[int]] = self.funcName2backInfo[functionName]
        else:
            Info: Dict[int, Set[int]] = self.funcName2forwInfo[functionName]
        workList: List[int] = sliceIdxs.copy()
        while len(workList) > 0:
            curIdx: int = workList.pop(0)
            for o in Info.get(curIdx, set()):
                if o not in sliceIdxs:
                    sliceIdxs.append(o)
                    workList.append(o)

        # sliceIdxs stores all indexes of nodes of slices
        cpg: CPG = self.funcName2cpg[functionName]
        coveredFileIds.add(self.file2Id[cpg.file])
        sliceIdxs.sort()
        for id in sliceIdxs:
            # 添加slice行代码
            slices.append(self.symbolizingTool.symbolize(cpg.statements[id].getEscapedCodeStr()))
            # 添加slice行行号和文件id
            sliceLines.append([cpg.statements[id].location.startLine, self.file2Id[cpg.file]])

            callTool = CallExprTool()
            callTool.judgeCall(cpg.statements[id])
            if callTool.functionName is not None and callTool.functionName in self.funcName2cpg.keys():
                otherCpg: CPG = self.funcName2cpg[callTool.functionName]
                # 以前面一行代码的return语句为起点反向遍历
                if backward:
                    assert isinstance(otherCpg.statements[-1], ReturnStatement)
                    newStartIdxs: List[int] = [len(otherCpg.statements)]
                else:
                    assert callTool.argNum> 0
                    newStartIdxs: List[int] = list(range(callTool.argNum))
                self.generateSlice(otherCpg.name, newStartIdxs, slices, functionChain, sliceLines,
                                           coveredFileIds, backward)