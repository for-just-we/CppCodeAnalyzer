from mainTool.cfg.CFG import *
from mainTool.utils.types import *

from mainTool.ast.declarations.complexDecls import *
from mainTool.ast.statements.blockStarters import *
from mainTool.ast.statements.jumps import *
from mainTool.ast.statements.statements import *
from mainTool.ast.expressions.expressionHolders import *
from mainTool.ast.expressions.binaryExpressions import *


# CPP CFG

class CCFG(CFG):
    def __init__(self):
        super(CCFG, self).__init__()
        self.breakStatements: List[CFGNode] = list()
        self.continueStatements: List[CFGNode] = list()
        self.returnStatements: List[CFGNode] = list()
        self.gotoStatements: Dict[CFGNode, str] = dict()
        self.labels: Dict[str, CFGNode] = dict()

    # 记录label(goto用到)对应的CFG结点
    def getBlockByLabel(self, label: str) -> CFGNode:
        block: CFGNode = self.labels.get(label, None)
        if block is None:
            print(f"warning : can not find block for label {label}")
            return self.getErrorNode()
        return block

    def addCFG(self, otherCFG):
        super().addCFG(otherCFG)
        # 在之前的基础上合并jump语句。
        self.parameters.extend(otherCFG.parameters)
        self.breakStatements.extend(otherCFG.breakStatements)
        self.continueStatements.extend(otherCFG.continueStatements)
        self.returnStatements.extend(otherCFG.returnStatements)
        self.gotoStatements.update(otherCFG.gotoStatements)
        self.labels.update(otherCFG.labels)


class StructuredFlowVisitor(ASTNodeVisitor):
    def __init__(self):
        self.returnCFG = None

    def visit(self, item):
        if isinstance(item, ParameterList):
            self.returnCFG = CCFGFactory.newParamListInstance(item)
        elif isinstance(item, Parameter):
            self.returnCFG = CCFGFactory.newNodesInstance([item])
            for node in self.returnCFG.vertices:
                if not isinstance(node, ASTNodeContainer):
                    continue
                self.returnCFG.parameters.append(node)

        elif isinstance(item, CompoundStatement):
            self.returnCFG = CCFGFactory.newCompoundInstance(item)

        elif isinstance(item, ReturnStatement):
            self.returnCFG = CCFGFactory.newReturnInstance(item)
        elif isinstance(item, GotoStatement):
            self.returnCFG = CCFGFactory.newGotoInstance(item)
        elif isinstance(item, BreakStatement):
            self.returnCFG = CCFGFactory.newBreakInstance(item)
        elif isinstance(item, ContinueStatement):
            self.returnCFG = CCFGFactory.newContinueInstance(item)
        elif isinstance(item, Label):
            self.returnCFG = CCFGFactory.newLabelInstance(item)

        elif isinstance(item, IfStatement):
            self.returnCFG = CCFGFactory.newIfInstance(item)
        elif isinstance(item, SwitchStatement):
            self.returnCFG = CCFGFactory.newSwitchInstance(item)
        elif isinstance(item, WhileStatement):
            self.returnCFG = CCFGFactory.newWhileInstance(item)
        elif isinstance(item, DoStatement):
            self.returnCFG = CCFGFactory.newDoInstance(item)
        elif isinstance(item, ForStatement):
            self.returnCFG = CCFGFactory.newForInstance(item)
        elif isinstance(item, ForRangeStatement):
            self.returnCFG = CCFGFactory.newForRangeInstance(item)
        elif isinstance(item, TryStatement):
            self.returnCFG = CCFGFactory.newTryInstance(item)

        elif isinstance(item, ASTNode):
            self.returnCFG = CCFGFactory.newNodesInstance([item])



class CCFGFactory(CFGFactory):
    structuredFlowVisitior: StructuredFlowVisitor = StructuredFlowVisitor()
    # 递归遍历AST生成CFG
    @staticmethod
    def convert(node: ASTNode) -> CCFG:
        if node is not None:
            node.accept(CCFGFactory.structuredFlowVisitior)
            cfg: CCFG = CCFGFactory.structuredFlowVisitior.returnCFG
        else:
            cfg: CCFG = CCFGFactory.newNodesInstance([])
        return cfg

    @staticmethod
    def newInstance(functionDefinition: FunctionDef) -> CFG:
        function: CCFG = CCFGFactory.newNodesInstance([])
        function.name = functionDefinition.name.getEscapedCodeStr()
        # 求解parameterBlock对应的cfg
        parameterBlock: CCFG = CCFGFactory.convert(functionDefinition.parameterList)
        # 求解functionBody对应的cfg
        functionBody: CCFG = CCFGFactory.convert(functionDefinition.content)
        parameterBlock.appendCFG(functionBody)
        function.appendCFG(parameterBlock)

        # 语句中还存在goto和return语句
        CCFGFactory.fixGotoStatements(function)
        CCFGFactory.fixReturnStatements(function)

        if len(function.breakStatements) > 0:
            raise RuntimeError("error: unresolved break statement")

        if len(function.continueStatements) > 0:
            raise RuntimeError("error: unresolved continue statement")

        return function


    # 函数形参列表
    @staticmethod
    def newParamListInstance(paramList: ParameterList) -> CFG:
        parameterListBlock: CFG = CCFGFactory.newNodesInstance([])
        for parameter in paramList.parameters:
            parameterListBlock.appendCFG(CCFGFactory.convert(parameter))
        return parameterListBlock


    @staticmethod
    def newBreakInstance(breakStatement: BreakStatement) -> CFG:
        breakBlock: CCFG = CCFG()
        breakContainer: CFGNode = ASTNodeContainer(breakStatement)
        breakBlock.addVertex(breakContainer)
        breakBlock.addCFGEdge(breakBlock.entry, breakContainer)
        breakBlock.addCFGEdge(breakContainer, breakBlock.exit)
        breakBlock.breakStatements.append(breakContainer)
        return breakBlock

    @staticmethod
    def newContinueInstance(continueStatement: ContinueStatement) -> CFG:
        continueBlock: CCFG = CCFG()
        continueContainer: CFGNode = ASTNodeContainer(continueStatement)
        continueBlock.addVertex(continueContainer)
        continueBlock.addCFGEdge(continueBlock.entry, continueContainer)
        continueBlock.addCFGEdge(continueContainer, continueBlock.exit)
        continueBlock.continueStatements.append(continueContainer)
        return continueBlock


    @staticmethod
    def newReturnInstance(returnStatement: ReturnStatement) -> CFG:
        returnBlock: CCFG = CCFG()
        returnContainer: CFGNode = ASTNodeContainer(returnStatement)
        returnBlock.addVertex(returnContainer)
        returnBlock.addCFGEdge(returnBlock.entry, returnContainer)
        returnBlock.addCFGEdge(returnContainer, returnBlock.exit)
        returnBlock.returnStatements.append(returnContainer)
        return returnBlock


    @staticmethod
    def newGotoInstance(gotoStatement: GotoStatement) -> CFG:
        gotoBlock: CCFG = CCFG()
        gotoContainer: CFGNode = ASTNodeContainer(gotoStatement)
        gotoBlock.addVertex(gotoContainer)
        gotoBlock.addCFGEdge(gotoBlock.entry, gotoContainer)
        gotoBlock.addCFGEdge(gotoContainer, gotoBlock.exit)
        gotoBlock.gotoStatements[gotoContainer] = gotoStatement.getTarget()
        return gotoBlock


    @staticmethod
    def newLabelInstance(labelStatement: Label) -> CFG:
        continueBlock: CCFG = CCFG()
        labelContainer: CFGNode = ASTNodeContainer(labelStatement)
        continueBlock.addVertex(labelContainer)
        continueBlock.addCFGEdge(continueBlock.entry, labelContainer)
        continueBlock.addCFGEdge(labelContainer, continueBlock.exit)
        label = labelStatement.getEscapedCodeStr()
        label = label.encode('utf-8')[:-2].decode('utf-8')
        continueBlock.labels[label] = labelContainer
        return continueBlock


    # 空语句
    @staticmethod
    def newNodesInstance(nodes: List[ASTNode]) -> CFG:
        block: CCFG = CCFG()
        last: CFGNode = block.entry
        for node in nodes:
            container: CFGNode = ASTNodeContainer(node)
            block.addVertex(container)
            block.addCFGEdge(last, container)
            last = container
        block.addCFGEdge(last, block.exit)
        return block

    #  求解IfStatement对应的CFG
    @staticmethod
    def newIfInstance(ifStatement: IfStatement) -> CFG:
        block: CCFG = CCFG()
        # 先处理condition
        conditionContainer: CFGNode = ASTNodeContainer(ifStatement.condition)
        block.addVertex(conditionContainer)
        block.addCFGEdge(block.entry, conditionContainer)

        # 再处理block
        ifBlock: CFG = CCFGFactory.convert(ifStatement.statement)
        block.mountCFG(conditionContainer, block.exit, ifBlock, CFGEdgeType.TRUE_LABEL)

        # 如果还有else那就处理else
        if ifStatement.elseNode is not None:
            elseBlock: CFG = CCFGFactory.convert(ifStatement.elseNode.statement)
            block.mountCFG(conditionContainer, block.exit, elseBlock, CFGEdgeType.FALSE_LABEL)
        else:
            block.addCFGEdge(conditionContainer, block.exit, CFGEdgeType.FALSE_LABEL)

        return block

    # switch语句
    @staticmethod
    def newSwitchInstance(switchStatement: SwitchStatement) -> CFG:
        switchBlock: CCFG = CCFG()
        # 处理condition
        conditionContainer: CFGNode = ASTNodeContainer(switchStatement.condition)
        switchBlock.addVertex(conditionContainer)
        switchBlock.addCFGEdge(switchBlock.entry, conditionContainer)

        switchBody: CCFG = CCFGFactory.convert(switchStatement.statement)
        switchBlock.addCFG(switchBody)
        defaultLabel: bool = False

        # 获取每个case: xxx
        for key, value in switchBody.labels.items():
            # 如果内容是default
            if key == "default":
                defaultLabel = True
            switchBlock.addCFGEdge(conditionContainer, value, key)

        for edge in switchBody.inNeighborhood.get(switchBody.exit, []):
            switchBlock.addCFGEdge(edge.source, switchBlock.exit)
        # 不存在defalut标签的话，添加一条condition到switch结尾的CFG边
        if not defaultLabel:
            switchBlock.addCFGEdge(conditionContainer, switchBlock.exit)

        # switch中break直接与switch end相连
        CCFGFactory.fixBreakStatements(switchBlock, switchBlock.exit)
        return switchBlock


    # 处理while语句
    @staticmethod
    def newWhileInstance(whileStatement: WhileStatement) -> CFG:
        whileBlock: CCFG = CCFG()
        # 首先处理while condition
        conditionContainer: CFGNode = ASTNodeContainer(whileStatement.condition)
        whileBlock.addVertex(conditionContainer)
        whileBlock.addCFGEdge(whileBlock.entry, conditionContainer)
        # while对应的循环主体
        whileBody: CFG = CCFGFactory.convert(whileStatement.statement)
        whileBlock.mountCFG(conditionContainer, conditionContainer, whileBody, CFGEdgeType.TRUE_LABEL)
        whileBlock.addCFGEdge(conditionContainer, whileBlock.exit, CFGEdgeType.FALSE_LABEL)

        # 考虑break连接到exit
        CCFGFactory.fixBreakStatements(whileBlock, whileBlock.exit)
        # continue连接到condition
        CCFGFactory.fixContinueStatements(whileBlock, conditionContainer)
        return whileBlock

    @staticmethod
    def newDoInstance(doStatement: DoStatement) -> CFG:
        doBlock: CCFG = CCFG()
        # do-while condition
        conditionContainer: CFGNode = ASTNodeContainer(doStatement.condition)
        doBlock.addVertex(conditionContainer)
        doBlock.addCFGEdge(conditionContainer, doBlock.exit, CFGEdgeType.FALSE_LABEL)
        # do-while body
        doBody: CFG = CCFGFactory.convert(doStatement.statement)
        doBlock.mountCFG(doBlock.entry, conditionContainer, doBody, CFGEdgeType.EMPTY_LABEL)

        for edge in doBody.outNeighborhood.get(doBody.entry, []):
            doBlock.addCFGEdge(conditionContainer, edge.destination, CFGEdgeType.TRUE_LABEL)
        # 该层循环中的所有break直接连接到循环exit
        CCFGFactory.fixBreakStatements(doBlock, doBlock.exit)
        # continue直接连接到condition
        CCFGFactory.fixContinueStatements(doBlock, conditionContainer)
        return doBlock

    # 处理for循环，与while相比，for的CFG会先执行forInit，然后condition和（ForBody + expression）组成循环
    @staticmethod
    def newForInstance(forStatement: ForStatement) -> CFG:
        forBlock: CCFG = CCFG()
        # 处理forInit，forCondition和表达式
        initialization: ASTNode = forStatement.forInitStatement
        condition: ASTNode = forStatement.condition
        expression: ASTNode = forStatement.expression

        # forBody
        forBody: CFG = CCFGFactory.convert(forStatement.statement)
        if condition is not None:
            conditionContainer = ASTNodeContainer(condition)
        else: # 没条件的话该for循环不会终止
            conditionContainer = InfiniteForNode()

        forBlock.addVertex(conditionContainer)
        # condition连接到ExitNode的false边
        forBlock.addCFGEdge(conditionContainer, forBlock.exit, CFGEdgeType.FALSE_LABEL)

        if initialization is not None:
            # initialization不为null的话，将initializationContainer插入到Entry和condition之间
            initializationContainer: CFGNode = ASTNodeContainer(initialization)
            forBlock.addVertex(initializationContainer)
            forBlock.addCFGEdge(forBlock.entry, initializationContainer)
            forBlock.addCFGEdge(initializationContainer, conditionContainer)
        else:
            # 否则Entry直接连接到condition
            forBlock.addCFGEdge(forBlock.entry, conditionContainer)

        if expression is not None:
            # expression不为null的话
            expressionContainer: CFGNode = ASTNodeContainer(expression)
            forBlock.addVertex(expressionContainer)
            forBlock.addCFGEdge(expressionContainer, conditionContainer)
            forBlock.mountCFG(conditionContainer, expressionContainer, forBody, CFGEdgeType.TRUE_LABEL)
        else:
            forBlock.mountCFG(conditionContainer, conditionContainer, forBody, CFGEdgeType.TRUE_LABEL)

        # break直接连接到exit
        CCFGFactory.fixBreakStatements(forBlock, forBlock.exit)
        # continue连接到condition
        CCFGFactory.fixContinueStatements(forBlock, conditionContainer)
        return forBlock


    @staticmethod
    def newForRangeInstance(forRangeStatement: ForRangeStatement) -> CFG:
        forBlock: CCFG = CCFG()
        # 处理forRangeInit，forCondition和表达式
        forRangeInit: ASTNode = forRangeStatement.forRangeInit
        # forBody
        forBody: CFG = CCFGFactory.convert(forRangeStatement.statement)
        conditionContainer: CFGNode = InfiniteForNode()
        forBlock.addVertex(conditionContainer)

        # Entry到InfiniteFor
        forBlock.addCFGEdge(forBlock.entry, conditionContainer)
        # condition连接到ExitNode的false边
        forBlock.addCFGEdge(conditionContainer, forBlock.exit, CFGEdgeType.FALSE_LABEL)
        initializationContainer: CFGNode = ASTNodeContainer(forRangeInit)
        forBlock.addVertex(initializationContainer)

        # condition -> for range init
        forBlock.addCFGEdge(conditionContainer, initializationContainer, CFGEdgeType.TRUE_LABEL)
        # init -> forBody -> condition
        forBlock.mountCFG(initializationContainer, conditionContainer, forBody, CFGEdgeType.EMPTY_LABEL)
        # break直接连接到exit
        CCFGFactory.fixBreakStatements(forBlock, forBlock.exit)
        # continue连接到condition
        CCFGFactory.fixContinueStatements(forBlock, conditionContainer)
        return forBlock


    @staticmethod
    def newTryInstance(tryStatement: TryStatement):
        return CCFGFactory.newCompoundInstance(tryStatement.statement)

    @staticmethod
    def newCompoundInstance(content: CompoundStatement) -> CFG:
        compoundBlock: CFG = CCFGFactory.newNodesInstance([])
        for statement in content.getStatements():
            compoundBlock.appendCFG(CCFGFactory.convert(statement))
        return compoundBlock


    # jump类语句处理，添加CFG边
    @staticmethod
    def fixBreakStatements(thisCFG: CCFG, target: CFGNode):
        for breakStatement in thisCFG.breakStatements:
            # fix之前break语句与后面的CFG结点有CFG边相连，现在全部删除
            thisCFG.removeEdgesFrom(breakStatement)
            # break语句无条件跳转到target
            thisCFG.addCFGEdge(breakStatement, target)
        thisCFG.breakStatements.clear()

    @staticmethod
    def fixContinueStatements(thisCFG: CCFG, target: CFGNode):
        for continueStatement in thisCFG.continueStatements:
            # 删除与continue语句直接相连的边
            thisCFG.removeEdgesFrom(continueStatement)
            # target为continue跳转到的结点
            thisCFG.addCFGEdge(continueStatement, target)
        thisCFG.continueStatements.clear()

    @staticmethod
    def fixReturnStatements(thisCFG: CCFG):
        for returnStatement in thisCFG.returnStatements:
            # 删除return相连的边
            thisCFG.removeEdgesFrom(returnStatement)
            # return连接到exit
            thisCFG.addCFGEdge(returnStatement, thisCFG.exit)
        thisCFG.returnStatements.clear()

    @staticmethod
    def fixGotoStatements(thisCFG: CCFG):
        for gotoStatement, label in thisCFG.gotoStatements.items():
            # 删除与goto语句相连的CFG边
            thisCFG.removeEdgesFrom(gotoStatement)
            # 添加CFG边到block结点跳转的边
            thisCFG.addCFGEdge(gotoStatement, thisCFG.getBlockByLabel(label))
        thisCFG.gotoStatements.clear()


def ASTToCFGConvert(node: FunctionDef) -> CFG:
    return CCFGFactory.newInstance(node)