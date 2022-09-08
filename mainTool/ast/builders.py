from antlr4 import TerminalNode, ParseTreeWalker
from antlr4.tree.Tree import TerminalNodeImpl

from mainTool.antlr.CPP14Listener import CPP14Listener
from mainTool.antlr.CPP14Parser import CPP14Parser

from mainTool.ast.astNode import CodeLocation
from mainTool.ast.declarations.complexDecls import *

from mainTool.ast.statements.blockStarters import *
from mainTool.ast.statements.jumps import *
from mainTool.ast.statements.statements import *

from mainTool.ast.declarations.simpleDecls import IdentifierDecl

from mainTool.ast.expressions.expression import *
from mainTool.ast.expressions.primaryExpressions import *
from mainTool.ast.expressions.expressionHolders import *
from mainTool.ast.expressions.postfixExpressions import *
from mainTool.ast.expressions.binaryExpressions import *

from typing import Dict
import json
# 将AntlrAST解析为自定义AST


varDecl = "VarDecl"
declarator = "Declarator"

class NestingReconstructor(object):
    def __init__(self, stack: List[ASTNode]):
        self.stack: List[ASTNode] = stack

    def addItemToParent(self, expression: ASTNode):
        topOfStack: ASTNode = self.stack[-1]
        topOfStack.addChild(expression)

    def pullUpOnlyChild(self, expression: Expression) -> Expression:
        if expression.getChildCount() == 1:
            expression = expression.getChild(0)
        return expression

    # 合并子表达式
    def consolidateSubExpression(self, ctx: ParserRuleContext):
        expression: Expression = self.stack.pop()
        expression.initializeFromContext(ctx)

        if not isinstance(expression, ExpressionHolder):
            expression = self.pullUpOnlyChild(expression)

        self.addItemToParent(expression)

class FunctionContentBuilder(CPP14Listener):
    def __init__(self):
        super(FunctionContentBuilder, self).__init__()
        self.stack: List[ASTNode] = list()
        self.idType: List[str] = list()

        self.curType: str = None
        self.curCompleteType: str = None
        self.curVarNameId: Identifier = None # 标识当前变量名，处理IdentifierDeclType时用

        self.countArrayDecl: int = 0
        self.arrayIdentifierCount: int = 0

        self.pastTheTypeId: bool = False # 用来解析cast type时用，为true表示现在正在解析castTarget
        self.nesting: NestingReconstructor = NestingReconstructor(self.stack)

    def enterStatement(self, ctx: CPP14Parser.StatementContext):
        # 跳过labelstatement
        if ctx.labeledstatement() is not None:
            return
        statementItem: Statement = Statement()
        statementItem.initializeFromContext(ctx)
        self.stack.append(statementItem)

    def exitStatement(self, ctx: CPP14Parser.StatementContext):
        # 跳过labelstatement
        if ctx.labeledstatement() is not None:
            return
        if len(self.stack) == 0:
            raise RuntimeError("statement parsing error")
        curNode: ASTNode = self.stack.pop()
        parent: ASTNode = self.stack[-1]
        curNode.initializeFromContext(ctx)

        # 当前statement的父节点是If-Else
        if isinstance(parent, IfStatement):
            # ctx.parent就是SelectionstatementContext类型
            # 如果当前statement的父节点是If
            if ctx == ctx.parentCtx.getChild(4):
                parent.addChild(curNode)
            # 当前statement的父节点是Else
            else:
                elseStatement: ElseStatement = ElseStatement()
                parent.elseNode = elseStatement
                elseStatement.addChild(curNode)
            return

        if isinstance(curNode, IdentifierDeclStatement):
            self.curType = None
        parent.addChild(curNode)

    # 块语句
    def enterCompoundstatement(self, ctx: CPP14Parser.CompoundstatementContext):
        if isinstance(self.stack[-1], TryStatement) or isinstance(self.stack[-1], CatchStatement):
            self.stack.append(CompoundStatement())
        else:
            self.stack[-1] = CompoundStatement()

    def exitCompoundstatement(self, ctx: CPP14Parser.CompoundstatementContext):
        # 非try-catch语句统统在exitStatement时处理
        comp: ASTNode = self.stack.pop()
        if len(self.stack) > 0 and (isinstance(self.stack[-1], TryStatement) or
                                    isinstance(self.stack[-1], CatchStatement)):
            comp.initializeFromContext(ctx)
            self.stack[-1].addChild(comp)
        else:
            self.stack.append(comp)

    # 表达式语句
    def enterExpressionstatement(self, ctx: CPP14Parser.ExpressionstatementContext):
        # expressionstatement上面可能是普通statement，也可能是forinit, 对于forinit，我们保留
        if isinstance(self.stack[-1], ForInit):
            return
        self.stack[-1] = ExpressionStatement() # replaceTopOfStack

    # label
    def enterLabel(self, ctx: CPP14Parser.LabelContext):
        label: Label = Label()
        if ctx.Case() is not None:
            label.type = LabelType.Case
        elif ctx.Default() is not None:
            label.type = LabelType.Default
        else:
            label.type = LabelType.Normal
        self.stack.append(label)

    def exitLabel(self, ctx: CPP14Parser.LabelContext):
        label: Label = self.stack.pop()
        label.initializeFromContext(ctx)
        self.stack[-1].addChild(label)

    # if-else语句
    def enterIfStatement(self, ctx: CPP14Parser.IfStatementContext):
        self.stack[-1] = IfStatement()  # replaceTopOfStack

    # switch
    def enterSwitchStatement(self, ctx: CPP14Parser.SwitchStatementContext):
        self.stack[-1] = SwitchStatement()  # replaceTopOfStack

    # while
    def enterWhileStatement(self, ctx: CPP14Parser.WhileStatementContext):
        self.stack[-1] = WhileStatement()  # replaceTopOfStack

    # For
    def enterForStatement(self, ctx: CPP14Parser.ForStatementContext):
        self.stack[-1] = ForStatement()  # replaceTopOfStack

    # for init语句
    def enterForinitstatement(self, ctx: CPP14Parser.ForinitstatementContext):
        forinit: ForInit = ForInit()
        self.stack.append(forinit)

    def exitForinitstatement(self, ctx: CPP14Parser.ForinitstatementContext):
        forinit: ASTNode = self.stack.pop()
        forinit.initializeFromContext(ctx)
        forStatement: ForStatement = self.stack[-1]
        forStatement.addChild(forinit)

    # DoWhile
    def enterDoStatement(self, ctx: CPP14Parser.DoStatementContext):
        self.stack[-1] = DoStatement()  # replaceTopOfStack

    # ForRange
    def enterForRangeStatement(self, ctx: CPP14Parser.ForRangeStatementContext):
        self.stack[-1] = ForRangeStatement()  # replaceTopOfStack

    # ForRange decl
    def enterForrangedeclaration(self, ctx: CPP14Parser.ForrangedeclarationContext):
        forRangeInit: ForRangeInit = ForRangeInit()
        self.stack.append(forRangeInit)
        self.curType = ""

    def exitForrangeinitializer(self, ctx:CPP14Parser.ForrangeinitializerContext):
        forRangeInit: ASTNode = self.stack.pop()
        forRangeInit.initializeFromContext(ctx)
        self.stack[-1].addChild(forRangeInit)
        self.curType = None
        self.curCompleteType = None

    # try catch异常处理
    # try语句
    def enterTryblock(self, ctx: CPP14Parser.TryblockContext):
        self.stack[-1] = TryStatement() # replaceTopOfStack

    # catch语句
    def enterHandler(self, ctx: CPP14Parser.HandlerContext):
        catchStatement: CatchStatement = CatchStatement()
        self.stack.append(catchStatement)

    def exitHandler(self, ctx:CPP14Parser.HandlerContext):
        catchStatement: CatchStatement = self.stack.pop()
        catchStatement.initializeFromContext(ctx)

        if not isinstance(self.stack[-1], TryStatement):
            raise RuntimeError("error when parsing try-catch block")

        tryStatement: TryStatement = self.stack[-1]
        tryStatement.addCatchStatement(catchStatement)

    def enterExceptiondeclaration(self, ctx: CPP14Parser.ExceptiondeclarationContext):
        self.curType = ""

    def exitExceptiondeclaration(self, ctx:CPP14Parser.ExceptiondeclarationContext):
        self.curType = None

    # 跳转语句
    def enterJumpstatement(self, ctx: CPP14Parser.JumpstatementContext):
        # break语句
        if ctx.Break() is not None:
            self.stack[-1] = BreakStatement()
        # continue语句
        elif ctx.Continue() is not None:
            self.stack[-1] = ContinueStatement()
        # goto语句
        elif ctx.Goto() is not None:
            self.stack[-1] = GotoStatement()
        # return语句
        elif ctx.Return() is not None:
            self.stack[-1] = ReturnStatement()

    # 变量定义IdentifierDeclStatement
    def enterSimpledeclaration(self, ctx: CPP14Parser.SimpledeclarationContext):
        self.curType = ""
        if isinstance(self.stack[-1], ForInit):
            return
        idDeclStmt: IdentifierDeclStatement = IdentifierDeclStatement()
        idDeclStmt.initializeFromContext(ctx)
        self.stack[-1] = idDeclStmt

    # 处理变量定义类型curType
    def exitDeclspecifierseq(self, ctx: CPP14Parser.DeclspecifierseqContext):
        if ctx.getChildCount() == 1:
            self.curType = self.curType.strip()

    def enterOtherDecl(self, ctx: CPP14Parser.OtherDeclContext):
        self.idType.append(varDecl)

    def exitOtherDecl(self, ctx: CPP14Parser.OtherDeclContext):
        self.idType.pop()

    # 一个initdeclarator标识着1个变量
    def enterInitdeclarator(self, ctx: CPP14Parser.InitdeclaratorContext):
        self.curCompleteType = self.curType.strip()
        identifierDecl: IdentifierDecl = IdentifierDecl()
        self.stack.append(identifierDecl)
        declType: IdentifierDeclType = IdentifierDeclType()
        # 先设置基础类型，完整类型可能是指针类型
        declType.baseType = self.curType.strip()
        identifierDecl.setType(declType)

    # 一个initdeclarator标识着1个变量
    def exitInitdeclarator(self, ctx: CPP14Parser.InitdeclaratorContext):
        self.curCompleteType = None
        self.curVarNameId = None
        identifierDecl: ASTNode = self.stack.pop()
        identifierDecl.initializeFromContext(ctx)
        identifierDeclStatement: ASTNode = self.stack[-1]
        identifierDeclStatement.addChild(identifierDecl)

    # 处理变量名和完整类型
    def enterDeclarator(self, ctx: CPP14Parser.DeclaratorContext):
        # 标识进入变量定义
        # ForRangeInit和catch要特殊处理
        if isinstance(self.stack[-1], ForRangeInit) or isinstance(self.stack[-1], CatchStatement):
            self.curType = self.curType.strip()
            self.curCompleteType = self.curType
        self.idType.append(declarator)

    def exitDeclarator(self, ctx: CPP14Parser.DeclaratorContext):
        self.idType.pop()
        # For Range Init
        if isinstance(self.stack[-1], ForRangeInit):
            init: ForRangeInit = self.stack[-1]
            initType: IdentifierDeclType = IdentifierDeclType()
            initType.baseType = self.curType
            initType.completeType = self.curCompleteType
            init.setType(initType)
            return
        elif isinstance(self.stack[-1], CatchStatement):
            catchStatement: CatchStatement = self.stack[-1]
            identifierDeclType: IdentifierDeclType = IdentifierDeclType()
            identifierDeclType.baseType = self.curType
            identifierDeclType.completeType = self.curCompleteType
            catchStatement.setExceptionType(identifierDeclType)
            return
        # 处理当前变量的完整类型
        curDecl: IdentifierDecl = self.stack[-1]
        curVarType: IdentifierDeclType = curDecl.type
        curVarType.completeType = self.curCompleteType

    # 处理指针定义类型, char *p;
    def enterPtrDecl(self, ctx: CPP14Parser.PtrDeclContext):
        if ctx.ptroperator().Star() is not None:
            self.curCompleteType += " *"

    # 处理数组定义类型，char source[100];，对于这种变量其类型为 char *
    def enterArrayDecl(self, ctx: CPP14Parser.ArrayDeclContext):
        self.curCompleteType += " *"
        self.countArrayDecl += 1

    def exitArrayDecl(self, ctx:CPP14Parser.ArrayDeclContext):
        self.countArrayDecl -= 1
        if self.countArrayDecl == 0:
            self.arrayIdentifierCount = 0

    # 变量定义语句可能伴随着赋值，包括 int a = 10, b{10}, c(100);
    # 对应 int a = 10;
    def enterInitDeclWithAssign(self, ctx: CPP14Parser.InitDeclWithAssignContext):
        assignmentExpr: AssignmentExpr = AssignmentExpr()
        assignmentExpr.operator = "="
        assignmentExpr.flag = False # 不再自动设置operator
        assignmentExpr.addChild(self.curVarNameId.copy())
        self.stack.append(assignmentExpr)

    def exitInitDeclWithAssign(self, ctx: CPP14Parser.InitDeclWithAssignContext):
        self.nesting.consolidateSubExpression(ctx)

    # 列表初始化对应int a{10};
    def enterInitDeclWithList(self, ctx: CPP14Parser.InitDeclWithListContext):
        assignmentExpr: AssignmentExpr = AssignmentExpr()
        assignmentExpr.operator = "="
        assignmentExpr.flag = False  # 不再自动设置operator
        assignmentExpr.addChild(self.curVarNameId.copy())

        initializerList: InitializerList = InitializerList()
        self.stack.append(assignmentExpr)
        self.stack.append(initializerList)

    def exitInitDeclWithList(self, ctx: CPP14Parser.InitDeclWithListContext):
        self.nesting.consolidateSubExpression(ctx)
        self.nesting.consolidateSubExpression(ctx)

    # 构造函数初始化，对应int a(10);
    def enterInitDeclWithCall(self, ctx: CPP14Parser.InitDeclWithCallContext):
        expr: CallExpression = CallExpression()
        self.stack.append(expr)

    def exitInitDeclWithCall(self, ctx: CPP14Parser.InitDeclWithCallContext):
        self.nesting.consolidateSubExpression(ctx)

    # 类静态变量 className::varName
    def enterClassIdentifier(self, ctx: CPP14Parser.ClassIdentifierContext):
        staticVariable: ClassStaticIdentifier = ClassStaticIdentifier()
        self.stack.append(staticVariable)

    def exitQualifiedid(self, ctx: CPP14Parser.QualifiedidContext):
        if isinstance(self.stack[-1], ClassStaticIdentifier):
            staticVariable: ClassStaticIdentifier = self.stack.pop()
            staticVariable.initializeFromContext(ctx)
            self.stack[-1].addChild(staticVariable)
            if len(self.idType) > 0 and self.idType[-1] == declarator:
                self.curVarNameId = staticVariable

    # 条件判断Condition
    def enterCondition(self, ctx: CPP14Parser.ConditionContext):
        condition: Condition = Condition()
        self.stack.append(condition)

    def exitCondition(self, ctx: CPP14Parser.ConditionContext):
        condition: Condition = self.stack.pop()
        parentNode: ASTNode = self.stack[-1]
        parentNode.addChild(condition)
        condition.initializeFromContext(ctx)

    # 三目表达式
    def enterRealConditionalExpression(self, ctx: CPP14Parser.RealConditionalExpressionContext):
        expr: ConditionalExpression = ConditionalExpression()
        self.stack.append(expr)

    def exitRealConditionalExpression(self, ctx: CPP14Parser.RealConditionalExpressionContext):
        expr: ConditionalExpression = self.stack[-1]
        child: ASTNode = expr.getChild(0)
        if child is None:
            return
        cnd: Condition = Condition()
        cnd.addChild(child)
        cnd.initializeFromContext(child.parseTreeNodeContext)
        expr.children[0] = cnd
        self.nesting.consolidateSubExpression(ctx)

    # BinaryExpression
    def enterAssignmentexpression(self, ctx: CPP14Parser.AssignmentexpressionContext):
        expr: AssignmentExpr = AssignmentExpr()
        self.stack.append(expr)

    def exitAssignmentexpression(self, ctx: CPP14Parser.AssignmentexpressionContext):
        self.nesting.consolidateSubExpression(ctx)

    # 逻辑或运算：expr1 || expr2
    def enterLogicalorexpression(self, ctx: CPP14Parser.LogicalorexpressionContext):
        expr: OrExpression = OrExpression()
        self.stack.append(expr)

    def exitLogicalorexpression(self, ctx: CPP14Parser.LogicalorexpressionContext):
        self.nesting.consolidateSubExpression(ctx)

    # 逻辑与运算，expr1 && expr2
    def enterLogicalandexpression(self, ctx: CPP14Parser.LogicalandexpressionContext):
        expr: AndExpression = AndExpression()
        self.stack.append(expr)

    def exitLogicalandexpression(self, ctx: CPP14Parser.LogicalandexpressionContext):
        self.nesting.consolidateSubExpression(ctx)

    # 与运算, expr1 | expr2
    def enterInclusiveorexpression(self, ctx: CPP14Parser.InclusiveorexpressionContext):
        expr: InclusiveOrExpression = InclusiveOrExpression()
        self.stack.append(expr)

    def exitInclusiveorexpression(self, ctx: CPP14Parser.InclusiveorexpressionContext):
        self.nesting.consolidateSubExpression(ctx)

    # 或运算, expr1 ^ expr2
    def enterExclusiveorexpression(self, ctx: CPP14Parser.ExclusiveorexpressionContext):
        expr: ExclusiveOrExpression = ExclusiveOrExpression()
        self.stack.append(expr)

    def exitExclusiveorexpression(self, ctx: CPP14Parser.ExclusiveorexpressionContext):
        self.nesting.consolidateSubExpression(ctx)

    # 与运算, expr1 & expr2
    def enterAndexpression(self, ctx: CPP14Parser.AndexpressionContext):
        expr: BitAndExpression = BitAndExpression()
        self.stack.append(expr)

    def exitAndexpression(self, ctx: CPP14Parser.AndexpressionContext):
        self.nesting.consolidateSubExpression(ctx)

    # 等于不等于判断，expr1 == expr2, expr1 != expr2
    def enterEqualityexpression(self, ctx: CPP14Parser.EqualityexpressionContext):
        expr: EqualityExpression = EqualityExpression()
        self.stack.append(expr)

    def exitEqualityexpression(self, ctx: CPP14Parser.EqualityexpressionContext):
        self.nesting.consolidateSubExpression(ctx)

    # 大于小于判断，expr1 >= / <= / < / > expr2
    def enterRelationalexpression(self, ctx: CPP14Parser.RelationalexpressionContext):
        expr: RelationalExpression = RelationalExpression()
        self.stack.append(expr)

    def exitRelationalexpression(self, ctx: CPP14Parser.RelationalexpressionContext):
        self.nesting.consolidateSubExpression(ctx)

    # 左移，右移运算 , expr1 << / >> expr2
    def enterShiftexpression(self, ctx: CPP14Parser.ShiftexpressionContext):
        expr: ShiftExpression = ShiftExpression()
        self.stack.append(expr)

    def exitShiftexpression(self, ctx: CPP14Parser.ShiftexpressionContext):
        self.nesting.consolidateSubExpression(ctx)

    # 加减法运算, expr1 + / - expr2
    def enterAdditiveexpression(self, ctx: CPP14Parser.AdditiveexpressionContext):
        expr: AdditiveExpression = AdditiveExpression()
        self.stack.append(expr)

    def exitAdditiveexpression(self, ctx: CPP14Parser.AdditiveexpressionContext):
        self.nesting.consolidateSubExpression(ctx)

    # 乘除模运算, expr1 * / / / % expr2
    def enterMultiplicativeexpression(self, ctx: CPP14Parser.MultiplicativeexpressionContext):
        expr: MultiplicativeExpression = MultiplicativeExpression()
        self.stack.append(expr)

    def exitMultiplicativeexpression(self, ctx: CPP14Parser.MultiplicativeexpressionContext):
        self.nesting.consolidateSubExpression(ctx)

    # New操作
    def enterNewexpression(self, ctx: CPP14Parser.NewexpressionContext):
        newExpression: NewExpression = NewExpression()
        self.stack.append(newExpression)

    def exitNewexpression(self, ctx: CPP14Parser.NewexpressionContext):
        newExpression: NewExpression = self.stack.pop()
        newExpression.initializeFromContext(ctx)
        topOfStack: ASTNode = self.stack[-1]
        topOfStack.addChild(newExpression)

    # delete 操作
    def enterDeleteexpression(self, ctx: CPP14Parser.DeleteexpressionContext):
        deleteExpression: DeleteExpression = DeleteExpression()
        self.stack.append(deleteExpression)

    def exitDeleteexpression(self, ctx: CPP14Parser.DeleteexpressionContext):
        deleteExpression: DeleteExpression = self.stack.pop()
        deleteExpression.initializeFromContext(ctx)
        topOfStack: ASTNode = self.stack[-1]
        topOfStack.addChild(deleteExpression)

    def enterThrowexpression(self, ctx: CPP14Parser.ThrowexpressionContext):
        throwExpression: ThrowExpression = ThrowExpression()
        self.stack.append(throwExpression)

    def exitThrowexpression(self, ctx: CPP14Parser.ThrowexpressionContext):
        self.nesting.consolidateSubExpression(ctx)

    # new type
    def enterNewtypeid(self, ctx: CPP14Parser.NewtypeidContext):
        self.curType = ""

    def exitNewtypeid(self, ctx: CPP14Parser.NewtypeidContext):
        identifier: Identifier = Identifier()
        identifier.codeStr = self.curType
        newExpression: NewExpression = self.stack[-1]
        newExpression.setTargetClass(identifier)
        self.curType = None

    def enterPtrNewDeclarator(self, ctx: CPP14Parser.PtrNewDeclaratorContext):
        self.curType = self.curType.strip() + " *"

    def enterThetypeid(self, ctx: CPP14Parser.ThetypeidContext):
        # cast target
        if isinstance(self.stack[-1], CastExpression):
            self.pastTheTypeId = True
            expr: CastTarget = CastTarget()
            expr.codeStr = ""
            self.stack.append(expr)
        # sizeof class
        elif isinstance(self.stack[-1], SizeofExpr):
            expr: SizeofOperand = SizeofOperand()
            self.stack.append(expr)

    def exitThetypeid(self, ctx: CPP14Parser.ThetypeidContext):
        if isinstance(self.stack[-1], CastTarget):
            self.pastTheTypeId = False
            self.nesting.consolidateSubExpression(ctx)
        elif isinstance(self.stack[-1], SizeofOperand):
            self.nesting.consolidateSubExpression(ctx)

    # 函数调用语句
    def enterFunctionCall(self, ctx: CPP14Parser.FunctionCallContext):
        expr: CallExpression = CallExpression()
        self.stack.append(expr)

    def exitFunctionCall(self, ctx: CPP14Parser.FunctionCallContext):
        expr: CallExpression = self.stack[-1]
        child: ASTNode = expr.getChild(0)
        if child is None:
            return
        callee: Callee = Callee()
        callee.codeStr = child.getEscapedCodeStr()
        callee.addChild(child)
        callee.childNumber = 0
        expr.children[0] = callee
        # 如果没有调用参数，就创建一个空的参数列表
        if expr.argumentList is None:
            argumentList: ArgumentList = ArgumentList()
            argumentList.codeStr = ""
            expr.setArgumentList(argumentList)
        self.nesting.consolidateSubExpression(ctx)

    # CastExpression
    def enterCastexpression(self, ctx:CPP14Parser.CastexpressionContext):
        expr: CastExpression = CastExpression()
        self.stack.append(expr)

    def exitCastexpression(self, ctx:CPP14Parser.CastexpressionContext):
        self.nesting.consolidateSubExpression(ctx)

    def enterPostSimpleCastExpression(self, ctx:CPP14Parser.PostSimpleCastExpressionContext):
        expr: CastExpression = CastExpression()
        self.stack.append(expr)

    def exitPostSimpleCastExpression(self, ctx:CPP14Parser.PostSimpleCastExpressionContext):
        self.nesting.consolidateSubExpression(ctx)

    # cast target
    def enterSimpletypespecifier(self, ctx:CPP14Parser.SimpletypespecifierContext):
        # type(n) cast
        if not self.pastTheTypeId and isinstance(self.stack[-1], CastExpression):
            expr: CastTarget = CastTarget()
            self.stack.append(expr)

    def exitSimpletypespecifier(self, ctx:CPP14Parser.SimpletypespecifierContext):
        if not self.pastTheTypeId and isinstance(self.stack[-1], CastTarget):
            self.nesting.consolidateSubExpression(ctx)

    def enterCppCastExpression(self, ctx:CPP14Parser.CppCastExpressionContext):
        expr: CastExpression = CastExpression()
        self.stack.append(expr)

    def exitCppCastExpression(self, ctx:CPP14Parser.CppCastExpressionContext):
        self.nesting.consolidateSubExpression(ctx)

    # Sizeof
    def enterSizeofExpression(self, ctx:CPP14Parser.SizeofExpressionContext):
        expr: SizeofExpr = SizeofExpr()
        self.stack.append(expr)

    def exitSizeofExpression(self, ctx:CPP14Parser.SizeofExpressionContext):
        self.nesting.consolidateSubExpression(ctx)

    # expressionlist父节点可能为newExpression, meminitializer, initializer，postfix
    def enterExpressionlist(self, ctx:CPP14Parser.ExpressionlistContext):
        # 父节点是函数调用
        if isinstance(self.stack[-1], CallExpression):
            expr: ArgumentList = ArgumentList()
            self.stack.append(expr)

    def exitExpressionlist(self, ctx:CPP14Parser.ExpressionlistContext):
        # 当前结点是参数列表
        if isinstance(self.stack[-1], ArgumentList):
            self.nesting.consolidateSubExpression(ctx)

    # 普通赋值语句 var = literal;
    def enterNormalAssign(self, ctx:CPP14Parser.NormalAssignContext):
        # 父节点是函数调用参数列表
        if isinstance(self.stack[-1], ArgumentList):
            expr: Argument = Argument()
            self.stack.append(expr)

    def exitNormalAssign(self, ctx:CPP14Parser.NormalAssignContext):
        if isinstance(self.stack[-1], Argument):
            self.nesting.consolidateSubExpression(ctx)

    # 列表赋值语句 var = { literal1, literal2, ... }
    def enterArrayAssign(self, ctx:CPP14Parser.ArrayAssignContext):
        initializerList: InitializerList = InitializerList()
        self.stack.append(initializerList)

    def exitArrayAssign(self, ctx:CPP14Parser.ArrayAssignContext):
        self.nesting.consolidateSubExpression(ctx)

    # 后缀表达式，x++, x--
    def enterIncDecOp(self, ctx:CPP14Parser.IncDecOpContext):
        incDecOp: IncDecOp = IncDecOp()
        self.stack.append(incDecOp)

    def exitIncDecOp(self, ctx:CPP14Parser.IncDecOpContext):
        self.nesting.consolidateSubExpression(ctx)

    # 单目运算符, -1
    def enterUnaryexpression(self, ctx:CPP14Parser.UnaryexpressionContext):
        unaryOp: UnaryOp = UnaryOp()
        self.stack.append(unaryOp)

    def exitUnaryexpression(self, ctx:CPP14Parser.UnaryexpressionContext):
        self.nesting.consolidateSubExpression(ctx)

    # 结构体属性访问
    def enterMemberAccess(self, ctx:CPP14Parser.MemberAccessContext):
        expr: MemberAccess = MemberAccess()
        self.stack.append(expr)

    def exitMemberAccess(self, ctx:CPP14Parser.MemberAccessContext):
        self.nesting.consolidateSubExpression(ctx)

    def enterPtrMemberAccess(self, ctx:CPP14Parser.PtrMemberAccessContext):
        expr: PtrMemberAccess = PtrMemberAccess()
        self.stack.append(expr)

    def exitPtrMemberAccess(self, ctx:CPP14Parser.PtrMemberAccessContext):
        self.nesting.consolidateSubExpression(ctx)

    # 数组访问
    def enterArrayIndexing(self, ctx:CPP14Parser.ArrayIndexingContext):
        expr: ArrayIndexing = ArrayIndexing()
        self.stack.append(expr)

    def exitArrayIndexing(self, ctx:CPP14Parser.ArrayIndexingContext):
        self.nesting.consolidateSubExpression(ctx)

    def visitTerminal(self, node: TerminalNode):
        parent: ASTNode = self.stack[-1]
        node_impl: TerminalNodeImpl = node
        # 当前终端结点属于变量定义语句一部分并且不属于C++模板定义
        if not self.pastTheTypeId and len(self.idType) > 0 and self.idType[-1] == varDecl:
            # 普通的变量定义初始化
            if self.curType is None:
                return
            self.curType += node_impl.getText() + " "
            return
        if isinstance(parent, CastTarget):
            parent.codeStr = parent.getEscapedCodeStr().strip() + " " + node_impl.getText()
            return

        node_type: int = node_impl.getSymbol().type
        # sizeof运算符
        if node_type == CPP14Parser.Sizeof:
            op: Sizeof = Sizeof()
            op.codeStr = node_impl.getText()
            parent.addChild(op)
        # 标识符
        elif node_type == CPP14Parser.Identifier:
            expr: Identifier = Identifier()
            expr.codeStr = node_impl.getText()
            parent.addChild(expr)
            # 如果当前Identifier在变量定义语句中
            if self.countArrayDecl > 0:
                self.arrayIdentifierCount += 1

            if self.countArrayDecl > 0 and self.arrayIdentifierCount > 1:
                return
            if len(self.idType) > 0 and self.idType[-1] == declarator:
                self.curVarNameId = expr

        # 字面值
        elif node_type in { CPP14Parser.Integerliteral, CPP14Parser.Userdefinedintegerliteral }:
            integerExpression: IntegerExpression = IntegerExpression()
            integerExpression.codeStr = node_impl.getText()
            parent.addChild(integerExpression)

        elif node_type in { CPP14Parser.Characterliteral, CPP14Parser.Userdefinedcharacterliteral }:
            charExpression: CharExpression = CharExpression()
            charExpression.codeStr = node_impl.getText()
            parent.addChild(charExpression)

        elif node_type in { CPP14Parser.Floatingliteral, CPP14Parser.Userdefinedfloatingliteral }:
            doubleExpression: DoubleExpression = DoubleExpression()
            doubleExpression.codeStr = node_impl.getText()
            parent.addChild(doubleExpression)

        elif node_type in { CPP14Parser.Stringliteral, CPP14Parser.Userdefinedstringliteral }:
            stringExpression: StringExpression = StringExpression()
            stringExpression.codeStr = node_impl.getText()
            parent.addChild(stringExpression)

        elif node_type in { CPP14Parser.TrueToken, CPP14Parser.FalseToken }:
            boolExpression: BoolExpression = BoolExpression()
            boolExpression.codeStr = node_impl.getText()
            parent.addChild(boolExpression)

        elif node_type == CPP14Parser.Nullptr:
            pointerExpression: PointerExpression = PointerExpression()
            pointerExpression.codeStr = node_impl.getText()
            parent.addChild(pointerExpression)

        # 单目运算符 &, *, +, -, ~, !
        elif node_type in { CPP14Parser.Star, CPP14Parser.And, CPP14Parser.Plus,
                            CPP14Parser.Minus, CPP14Parser.Tilde, CPP14Parser.Not }:
            # 目前是单目运算
            if isinstance(parent, UnaryOp):
                unaryOperator: UnaryOperator = UnaryOperator()
                unaryOperator.operator = node_impl.getText()
                parent.operator = node_impl.getText()
                parent.addChild(unaryOperator)

        # ++x, --x, x++, x--
        elif node_type in { CPP14Parser.PlusPlus, CPP14Parser.MinusMinus }:
            incDec: IncDec = IncDec()
            incDec.operator = node_impl.getText()
            incDec.codeStr = node_impl.getText()
            # ++x / --x
            if isinstance(parent, UnaryOp):
                incDecOp: IncDecOp = IncDecOp()
                incDecOp.isPost = False
                incDecOp.operator = node_impl.getText()
                incDecOp.addChild(incDec)
                self.stack[-1] = incDecOp

            # x++ / x--
            elif isinstance(parent, IncDecOp):
                parent.operator = incDec.operator
                parent.addChild(incDec)

# 这个类用来解析函数返回基础类型
class FunctionTypeBuilder(CPP14Listener):
    def __init__(self):
        self.type: str = ""
        self.idType: List[str] = list()

    def enterOtherDecl(self, ctx:CPP14Parser.OtherDeclContext):
        self.idType.append(varDecl)

    def exitOtherDecl(self, ctx:CPP14Parser.OtherDeclContext):
        self.idType.pop()

    def visitTerminal(self, node:TerminalNode):
        if len(self.idType) > 0 and self.idType[-1] == varDecl:
            self.type += node.getText() + " "

# 解析函数名以及函数参数列表
class FunctionNameParamBuilder(CPP14Listener):
    def __init__(self):
        self.stack: List[ASTNode] = list()
        self.stack.append(ParameterList())
        self.idType: List[str] = list()

        self.completeType: str = None
        self.funcName: Identifier = None

        self.curParamType: str = None # 参数基础类型
        self.curParamCompleteType: str = None # 参数基础类型

    def enterPtrDecl(self, ctx:CPP14Parser.PtrDeclContext):
        # 当前属于函数返回类型
        if isinstance(self.stack[-1], ParameterList):
            self.completeType += " *"
        else:
            self.curParamCompleteType += " *"

    def enterArrayDecl(self, ctx:CPP14Parser.ArrayDeclContext):
        if isinstance(self.stack[-1], Parameter):
            self.curParamCompleteType += " *"


    # 参数列表
    def enterParametersandqualifiers(self, ctx:CPP14Parser.ParametersandqualifiersContext):
        if isinstance(self.stack[-1], ParameterList):
            self.stack[-1].initializeFromContext(ctx)

    # 参数定义
    def enterParameterdeclaration(self, ctx:CPP14Parser.ParameterdeclarationContext):
        self.curParamType = ""
        parameter: Parameter = Parameter()
        type: ParameterType = ParameterType()
        parameter.setType(type)
        parameter.initializeFromContext(ctx)
        self.stack.append(parameter)

    def exitParameterdeclaration(self, ctx:CPP14Parser.ParameterdeclarationContext):
        parameter: Parameter = self.stack.pop()
        type = parameter.type
        type.baseType = self.curParamType
        type.completeType = self.curParamCompleteType

        parameterList: ParameterList = self.stack[-1]
        parameterList.addParameter(parameter)
        self.curParamType = None
        self.curParamCompleteType = None

    def enterDeclarator(self, ctx:CPP14Parser.DeclaratorContext):
        if isinstance(self.stack[-1], Parameter):
            self.curParamType = self.curParamType.strip()
            self.curParamCompleteType = self.curParamType

    def enterOtherDecl(self, ctx:CPP14Parser.OtherDeclContext):
        self.idType.append(varDecl)

    def exitOtherDecl(self, ctx:CPP14Parser.OtherDeclContext):
        self.idType.pop()

    # 函数名
    # 类静态变量 className::varName
    def enterClassIdentifier(self, ctx:CPP14Parser.ClassIdentifierContext):
        staticVariable: ClassStaticIdentifier = ClassStaticIdentifier()
        self.stack.append(staticVariable)

    def exitQualifiedid(self, ctx:CPP14Parser.QualifiedidContext):
        if isinstance(self.stack[-1], ClassStaticIdentifier):
            staticVariable: ClassStaticIdentifier = self.stack.pop()
            staticVariable.initializeFromContext(ctx)

            # 变量名
            if isinstance(self.stack[-1], ParameterList):
                self.funcName = staticVariable


    def visitTerminal(self, node:TerminalNode):
        parent: ASTNode = self.stack[-1]
        node_impl: TerminalNodeImpl = node

        # 当前终端结点属于变量定义语句一部分并且不属于C++模板定义
        if len(self.idType) > 0 and self.idType[-1] == varDecl:
            # 普通的变量定义初始化
            self.curParamType += node_impl.getText() + " "
            return

        node_type: int = node_impl.getSymbol().type
        #  标识符
        if node_type == CPP14Parser.Identifier:
            expr: Identifier = Identifier()
            expr.codeStr = node_impl.getText()
            # 函数名
            if isinstance(self.stack[-1], ParameterList):
                self.funcName = expr
            else:
                parent.addChild(expr)

                # 字面值
        elif node_type in {CPP14Parser.Integerliteral, CPP14Parser.Userdefinedintegerliteral}:
            integerExpression: IntegerExpression = IntegerExpression()
            integerExpression.codeStr = node_impl.getText()
            parent.addChild(integerExpression)

        elif node_type in {CPP14Parser.Characterliteral, CPP14Parser.Userdefinedcharacterliteral}:
            charExpression: CharExpression = CharExpression()
            charExpression.codeStr = node_impl.getText()
            parent.addChild(charExpression)

        elif node_type in {CPP14Parser.Floatingliteral, CPP14Parser.Userdefinedfloatingliteral}:
            doubleExpression: DoubleExpression = DoubleExpression()
            doubleExpression.codeStr = node_impl.getText()
            parent.addChild(doubleExpression)

        elif node_type in {CPP14Parser.Stringliteral, CPP14Parser.Userdefinedstringliteral}:
            stringExpression: StringExpression = StringExpression()
            stringExpression.codeStr = node_impl.getText()
            parent.addChild(stringExpression)

        elif node_type in {CPP14Parser.TrueToken, CPP14Parser.FalseToken}:
            boolExpression: BoolExpression = BoolExpression()
            boolExpression.codeStr = node_impl.getText()
            parent.addChild(boolExpression)

        elif node_type == CPP14Parser.Nullptr:
            pointerExpression: PointerExpression = PointerExpression()
            pointerExpression.codeStr = node_impl.getText()
            parent.addChild(pointerExpression)


class FunctionDefBuilder(CPP14Listener):
    def __init__(self):
        self.functionDef: FunctionDef = None
        self.walker: ParseTreeWalker = ParseTreeWalker()

    def enterFunctiondefinition(self, ctx:CPP14Parser.FunctiondefinitionContext):
        self.functionDef = FunctionDef()

        # 解析返回值类型
        typeBuilder: FunctionTypeBuilder = FunctionTypeBuilder()
        self.walker.walk(typeBuilder, ctx.declspecifierseq())
        returnType: ReturnType = ReturnType()
        returnType.baseType = typeBuilder.type.strip()
        # 设定函数返回类型
        self.functionDef.setReturnType(returnType)

        # 解析函数名和变量列表
        nameParamBuilder: FunctionNameParamBuilder = FunctionNameParamBuilder()
        nameParamBuilder.completeType = typeBuilder.type.strip()
        self.walker.walk(nameParamBuilder, ctx.declarator())

        parameterType: ParameterType = ParameterType()
        parameterType.baseType = nameParamBuilder.curParamType
        parameterType.completeType = nameParamBuilder.curParamCompleteType

        # 函数名
        self.functionDef.setName(nameParamBuilder.funcName)
        # 参数列表
        self.functionDef.setParameterList(nameParamBuilder.stack[-1])
        # 设置完整返回类型
        self.functionDef.returnType.completeType = nameParamBuilder.completeType

        # 解析函数名
        contentBuilder: FunctionContentBuilder = FunctionContentBuilder()
        contentBuilder.stack.append(Statement())
        self.walker.walk(contentBuilder, ctx.functionbody())
        content: CompoundStatement = contentBuilder.stack[-1]
        content.initializeFromContext(ctx.functionbody())
        self.functionDef.setContent(content)


class ClassDefBuilder(CPP14Listener):
    def __init__(self):
        self.inClassDecl: bool = False # 是否进入类定义作用域
        self.isClassName: bool = False # 是否可能为类名
        self.curClassName: Identifier = None
        self.classDefStatement: ClassDefStatement = None
        self.walker: ParseTreeWalker = ParseTreeWalker()

    def enterClassDecl(self, ctx:CPP14Parser.ClassDeclContext):
        self.classDefStatement = ClassDefStatement()
        self.inClassDecl = True

    def exitClassDecl(self, ctx:CPP14Parser.ClassDeclContext):
        self.inClassDecl = False

    def enterClassname(self, ctx:CPP14Parser.ClassnameContext):
        if self.inClassDecl:
            self.isClassName = True

    def exitClassname(self, ctx:CPP14Parser.ClassnameContext):
        if self.inClassDecl:
            self.isClassName = False

    # 成员函数定义
    def enterMemberFuncDecl(self, ctx:CPP14Parser.MemberFuncDeclContext):
        defBuilder: FunctionDefBuilder = FunctionDefBuilder()
        tree: CPP14Parser.FunctiondefinitionContext = ctx.functiondefinition()
        self.walker.walk(defBuilder, tree)

        functionDef: FunctionDef = defBuilder.functionDef
        if isinstance(functionDef.name, ClassStaticIdentifier):
            raise RuntimeError("Inner method declaration should not contain class name")
        staticIdentifier: ClassStaticIdentifier = ClassStaticIdentifier()
        staticIdentifier.className = self.curClassName
        staticIdentifier.varName = functionDef.name
        functionDef.replaceName(staticIdentifier)
        self.classDefStatement.functionDefs.append(functionDef)

    def visitTerminal(self, node:TerminalNode):
        if node.getSymbol().type == CPP14Parser.Identifier and self.isClassName:
            identifier:Identifier = Identifier()
            identifier.codeStr = node.getText()
            self.curClassName = identifier
            self.classDefStatement.name = identifier


# 解析一个c文件中包含的所有类/结构体定义和函数定义
class FileBuilder(CPP14Listener):
    def __init__(self):
        self.classDefs: List[ClassDefStatement] = list()
        self.functionDefs: List[FunctionDef] = list()
        self.walker: ParseTreeWalker = ParseTreeWalker()

    def enterClassDecl(self, ctx:CPP14Parser.ClassDeclContext):
        defBuilder: ClassDefBuilder = ClassDefBuilder()
        self.walker.walk(defBuilder, ctx)
        self.classDefs.append(defBuilder.classDefStatement)

    def enterFunctiondefinition(self, ctx:CPP14Parser.FunctiondefinitionContext):
        if isinstance(ctx.parentCtx, CPP14Parser.MemberFuncDeclContext):
            return
        defBuilder: FunctionDefBuilder = FunctionDefBuilder()
        self.walker.walk(defBuilder, ctx)
        self.functionDefs.append(defBuilder.functionDef)


def astNodeToJson(astNode: ASTNode) -> Dict:
    contents: list = list()
    astEdges: list = list()
    #  这里只引用了顶层结点的行号，需要其它的可以自行添加
    line: int = astNode.location.startLine
    queue: List[tuple] = [(-1, astNode)]
    idx = 0

    while len(queue) > 0:
        parentIdx, node = queue.pop(0)
        childNumber: int = node.getChildCount()
        operator: str = node.operator if isinstance(node, Expression) else ""
        contents.append([node.getTypeAsString(), node.getEscapedCodeStr(), operator])
        if parentIdx != -1:
            astEdges.append([parentIdx, idx])
        for i in range(childNumber):
            childNode: ASTNode = node.getChild(i)
            queue.append((idx, childNode))
        idx += 1

    return {
        "contents": contents,
        "edges": astEdges,
        "line": line
    }



def astToSerializedJson(astNode: ASTNode) -> Dict:
    json_data: Dict = astNodeToJson(astNode)
    return {
        "contents": json.dumps(json_data["contents"]),
        "edges": json.dumps(json_data["edges"]),
        "line": json_data["line"]
    }

def unserializeNode(data: Dict) -> Dict:
    return {
        "contents": json.loads(data["contents"]),
        "edges": json.loads(data["edges"]),
        "line": data["line"]
    }


def json2astNode(data: dict) -> ASTNode:
    types = list(map(lambda content: content[0], data["contents"]))
    tokenSeqs = list(map(lambda content: content[1], data["contents"]))
    operators = list(map(lambda content: content[2], data["contents"]))
    nodes: List[ASTNode] = [getInstanceFromTypeName(type) for type in types]
    for edge in data["edges"]:
        nodes[edge[0]].addChild(nodes[edge[1]])

    for node, tokenSeq, operator in zip(nodes, tokenSeqs, operators):
        node.codeStr = tokenSeq
        if isinstance(node, Expression):
            node.operator = operator

    location: CodeLocation = CodeLocation()
    location.startLine = data["line"]
    nodes[0].location = location

    return nodes[0]

def getInstanceFromTypeName(astType: str) -> ASTNode:
    if astType == "ParameterType":
        return ParameterType()
    elif astType == "ReturnType":
        return ReturnType()
    elif astType == "Parameter":
        return Parameter()
    elif astType == "ParameterList":
        return ParameterList()
    elif astType == "FunctionDef":
        return FunctionDef()
    elif astType == "ClassDefStatement":
        return ClassDefStatement()

    elif astType == "IdentifierDeclType":
        return IdentifierDeclType()
    elif astType == "IdentifierDecl":
        return IdentifierDecl()
    elif astType == "ForInit":
        return ForInit()
    elif astType == "ForRangeInit":
        return ForRangeInit()

    elif astType == "BinaryExpression":
        return BinaryExpression()
    elif astType == "AdditiveExpression":
        return AdditiveExpression()
    elif astType == "AndExpression":
        return AndExpression()
    elif astType == "AssignmentExpr":
        return AssignmentExpr()
    elif astType == "BitAndExpression":
        return BitAndExpression()
    elif astType == "EqualityExpression":
        return EqualityExpression()
    elif astType == "ExclusiveOrExpression":
        return ExclusiveOrExpression()
    elif astType == "InclusiveOrExpression":
        return InclusiveOrExpression()
    elif astType == "MultiplicativeExpression":
        return MultiplicativeExpression()
    elif astType == "OrExpression":
        return OrExpression()
    elif astType == "RelationalExpression":
        return RelationalExpression()
    elif astType == "ShiftExpression":
        return ShiftExpression()

    elif astType == "Expression":
        return Expression()
    elif astType == "Identifier":
        return Identifier()
    elif astType == "ClassStaticIdentifier":
        return ClassStaticIdentifier()
    elif astType == "ArrayIndexing":
        return ArrayIndexing()
    elif astType == "CastTarget":
        return CastTarget()
    elif astType == "CastExpression":
        return CastExpression()
    elif astType == "ConditionalExpression":
        return ConditionalExpression()
    elif astType == "IncDec":
        return IncDec()
    elif astType == "SizeofExpr":
        return SizeofExpr()
    elif astType == "Sizeof":
        return Sizeof()
    elif astType == "SizeofOperand":
        return SizeofOperand()
    elif astType == "UnaryOp":
        return UnaryOp()
    elif astType == "UnaryOperator":
        return UnaryOperator()

    elif astType == "ExpressionHolder":
        return ExpressionHolder()
    elif astType == "Argument":
        return Argument()
    elif astType == "ArgumentList":
        return ArgumentList()
    elif astType == "Callee":
        return Callee()
    elif astType == "Condition":
        return Condition()
    elif astType == "InitializerList":
        return InitializerList()
    elif astType == "ThrowExpression":
        return ThrowExpression()

    elif astType == "UnaryOp":
        return UnaryOp()
    elif astType == "UnaryOperator":
        return UnaryOperator()
    elif astType == "PostfixExpression":
        return PostfixExpression()
    elif astType == "IncDecOp":
        return IncDecOp()
    elif astType == "CallExpressionBase":
        return CallExpressionBase()
    elif astType == "CallExpression":
        return CallExpression()
    elif astType == "NewExpression":
        return NewExpression()
    elif astType == "DeleteExpression":
        return DeleteExpression()
    elif astType == "MemberAccess":
        return MemberAccess()
    elif astType == "PtrMemberAccess":
        return PtrMemberAccess()

    elif astType == "PrimaryExpression":
        return PrimaryExpression()
    elif astType == "BoolExpression":
        return BoolExpression()
    elif astType == "CharExpression":
        return CharExpression()
    elif astType == "DoubleExpression":
        return DoubleExpression()
    elif astType == "IntegerExpression":
        return IntegerExpression()
    elif astType == "PointerExpression":
        return PointerExpression()
    elif astType == "StringExpression":
        return StringExpression()

    elif astType == "JumpStatement":
        return JumpStatement()
    elif astType == "BreakStatement":
        return BreakStatement()
    elif astType == "ContinueStatement":
        return ContinueStatement()
    elif astType == "GotoStatement":
        return GotoStatement()
    elif astType == "ReturnStatement":
        return ReturnStatement()

    elif astType == "Statement":
        return Statement()
    elif astType == "ExpressionHolderStatement":
        return ExpressionHolderStatement()
    elif astType == "IdentifierDeclStatement":
        return IdentifierDeclStatement()
    elif astType == "Label":
        return Label()
    elif astType == "ExpressionStatement":
        return ExpressionStatement()

    else:
        return ASTNode()
