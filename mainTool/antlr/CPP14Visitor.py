# Generated from D:/projects/python/vul detect/tools/CppCodeAnalyzer/resources\CPP14.g4 by ANTLR 4.9.2
from antlr4 import *
from mainTool.antlr.CPP14Parser import CPP14Parser


# This class defines a complete generic visitor for a parse tree produced by CPP14Parser.

class CPP14Visitor(ParseTreeVisitor):

    # Visit a parse tree produced by CPP14Parser#translationunit.
    def visitTranslationunit(self, ctx:CPP14Parser.TranslationunitContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CPP14Parser#primaryexpression.
    def visitPrimaryexpression(self, ctx:CPP14Parser.PrimaryexpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CPP14Parser#idexpression.
    def visitIdexpression(self, ctx:CPP14Parser.IdexpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CPP14Parser#unqualifiedid.
    def visitUnqualifiedid(self, ctx:CPP14Parser.UnqualifiedidContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CPP14Parser#qualifiedid.
    def visitQualifiedid(self, ctx:CPP14Parser.QualifiedidContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CPP14Parser#normalGlobalIdentifier.
    def visitNormalGlobalIdentifier(self, ctx:CPP14Parser.NormalGlobalIdentifierContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CPP14Parser#classIdentifier.
    def visitClassIdentifier(self, ctx:CPP14Parser.ClassIdentifierContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CPP14Parser#nestedIdentifier.
    def visitNestedIdentifier(self, ctx:CPP14Parser.NestedIdentifierContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CPP14Parser#namespaceIdentifier.
    def visitNamespaceIdentifier(self, ctx:CPP14Parser.NamespaceIdentifierContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CPP14Parser#nestedTemplateIdentifier.
    def visitNestedTemplateIdentifier(self, ctx:CPP14Parser.NestedTemplateIdentifierContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CPP14Parser#decltypeIdentifier.
    def visitDecltypeIdentifier(self, ctx:CPP14Parser.DecltypeIdentifierContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CPP14Parser#lambdaexpression.
    def visitLambdaexpression(self, ctx:CPP14Parser.LambdaexpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CPP14Parser#lambdaintroducer.
    def visitLambdaintroducer(self, ctx:CPP14Parser.LambdaintroducerContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CPP14Parser#lambdacapture.
    def visitLambdacapture(self, ctx:CPP14Parser.LambdacaptureContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CPP14Parser#capturedefault.
    def visitCapturedefault(self, ctx:CPP14Parser.CapturedefaultContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CPP14Parser#capturelist.
    def visitCapturelist(self, ctx:CPP14Parser.CapturelistContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CPP14Parser#capture.
    def visitCapture(self, ctx:CPP14Parser.CaptureContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CPP14Parser#simplecapture.
    def visitSimplecapture(self, ctx:CPP14Parser.SimplecaptureContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CPP14Parser#initcapture.
    def visitInitcapture(self, ctx:CPP14Parser.InitcaptureContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CPP14Parser#lambdadeclarator.
    def visitLambdadeclarator(self, ctx:CPP14Parser.LambdadeclaratorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CPP14Parser#memberAccess.
    def visitMemberAccess(self, ctx:CPP14Parser.MemberAccessContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CPP14Parser#postTypeCastExpression.
    def visitPostTypeCastExpression(self, ctx:CPP14Parser.PostTypeCastExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CPP14Parser#incDecOp.
    def visitIncDecOp(self, ctx:CPP14Parser.IncDecOpContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CPP14Parser#TypeidExpression.
    def visitTypeidExpression(self, ctx:CPP14Parser.TypeidExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CPP14Parser#functionCall.
    def visitFunctionCall(self, ctx:CPP14Parser.FunctionCallContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CPP14Parser#postSimpleCastExpression.
    def visitPostSimpleCastExpression(self, ctx:CPP14Parser.PostSimpleCastExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CPP14Parser#CppCastExpression.
    def visitCppCastExpression(self, ctx:CPP14Parser.CppCastExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CPP14Parser#arrayIndexing.
    def visitArrayIndexing(self, ctx:CPP14Parser.ArrayIndexingContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CPP14Parser#ptrMemberAccess.
    def visitPtrMemberAccess(self, ctx:CPP14Parser.PtrMemberAccessContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CPP14Parser#postfixIgnore.
    def visitPostfixIgnore(self, ctx:CPP14Parser.PostfixIgnoreContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CPP14Parser#expressionlist.
    def visitExpressionlist(self, ctx:CPP14Parser.ExpressionlistContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CPP14Parser#pseudodestructorname.
    def visitPseudodestructorname(self, ctx:CPP14Parser.PseudodestructornameContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CPP14Parser#unaryexpression.
    def visitUnaryexpression(self, ctx:CPP14Parser.UnaryexpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CPP14Parser#sizeofExpression.
    def visitSizeofExpression(self, ctx:CPP14Parser.SizeofExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CPP14Parser#alignofExpression.
    def visitAlignofExpression(self, ctx:CPP14Parser.AlignofExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CPP14Parser#unaryoperator.
    def visitUnaryoperator(self, ctx:CPP14Parser.UnaryoperatorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CPP14Parser#newexpression.
    def visitNewexpression(self, ctx:CPP14Parser.NewexpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CPP14Parser#newplacement.
    def visitNewplacement(self, ctx:CPP14Parser.NewplacementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CPP14Parser#newtypeid.
    def visitNewtypeid(self, ctx:CPP14Parser.NewtypeidContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CPP14Parser#ptrNewDeclarator.
    def visitPtrNewDeclarator(self, ctx:CPP14Parser.PtrNewDeclaratorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CPP14Parser#nonPtrNewDeclarator.
    def visitNonPtrNewDeclarator(self, ctx:CPP14Parser.NonPtrNewDeclaratorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CPP14Parser#noptrnewdeclarator.
    def visitNoptrnewdeclarator(self, ctx:CPP14Parser.NoptrnewdeclaratorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CPP14Parser#newinitializer.
    def visitNewinitializer(self, ctx:CPP14Parser.NewinitializerContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CPP14Parser#deleteexpression.
    def visitDeleteexpression(self, ctx:CPP14Parser.DeleteexpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CPP14Parser#noexceptexpression.
    def visitNoexceptexpression(self, ctx:CPP14Parser.NoexceptexpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CPP14Parser#castexpression.
    def visitCastexpression(self, ctx:CPP14Parser.CastexpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CPP14Parser#pmexpression.
    def visitPmexpression(self, ctx:CPP14Parser.PmexpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CPP14Parser#multiplicativeexpression.
    def visitMultiplicativeexpression(self, ctx:CPP14Parser.MultiplicativeexpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CPP14Parser#additiveexpression.
    def visitAdditiveexpression(self, ctx:CPP14Parser.AdditiveexpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CPP14Parser#shiftexpression.
    def visitShiftexpression(self, ctx:CPP14Parser.ShiftexpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CPP14Parser#relationalexpression.
    def visitRelationalexpression(self, ctx:CPP14Parser.RelationalexpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CPP14Parser#equalityexpression.
    def visitEqualityexpression(self, ctx:CPP14Parser.EqualityexpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CPP14Parser#andexpression.
    def visitAndexpression(self, ctx:CPP14Parser.AndexpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CPP14Parser#exclusiveorexpression.
    def visitExclusiveorexpression(self, ctx:CPP14Parser.ExclusiveorexpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CPP14Parser#inclusiveorexpression.
    def visitInclusiveorexpression(self, ctx:CPP14Parser.InclusiveorexpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CPP14Parser#logicalandexpression.
    def visitLogicalandexpression(self, ctx:CPP14Parser.LogicalandexpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CPP14Parser#logicalorexpression.
    def visitLogicalorexpression(self, ctx:CPP14Parser.LogicalorexpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CPP14Parser#nonConditionalExpression.
    def visitNonConditionalExpression(self, ctx:CPP14Parser.NonConditionalExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CPP14Parser#realConditionalExpression.
    def visitRealConditionalExpression(self, ctx:CPP14Parser.RealConditionalExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CPP14Parser#assignmentexpression.
    def visitAssignmentexpression(self, ctx:CPP14Parser.AssignmentexpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CPP14Parser#assignmentoperator.
    def visitAssignmentoperator(self, ctx:CPP14Parser.AssignmentoperatorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CPP14Parser#expression.
    def visitExpression(self, ctx:CPP14Parser.ExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CPP14Parser#constantexpression.
    def visitConstantexpression(self, ctx:CPP14Parser.ConstantexpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CPP14Parser#statement.
    def visitStatement(self, ctx:CPP14Parser.StatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CPP14Parser#label.
    def visitLabel(self, ctx:CPP14Parser.LabelContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CPP14Parser#labeledstatement.
    def visitLabeledstatement(self, ctx:CPP14Parser.LabeledstatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CPP14Parser#expressionstatement.
    def visitExpressionstatement(self, ctx:CPP14Parser.ExpressionstatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CPP14Parser#compoundstatement.
    def visitCompoundstatement(self, ctx:CPP14Parser.CompoundstatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CPP14Parser#statementseq.
    def visitStatementseq(self, ctx:CPP14Parser.StatementseqContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CPP14Parser#ifStatement.
    def visitIfStatement(self, ctx:CPP14Parser.IfStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CPP14Parser#switchStatement.
    def visitSwitchStatement(self, ctx:CPP14Parser.SwitchStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CPP14Parser#condition.
    def visitCondition(self, ctx:CPP14Parser.ConditionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CPP14Parser#WhileStatement.
    def visitWhileStatement(self, ctx:CPP14Parser.WhileStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CPP14Parser#DoStatement.
    def visitDoStatement(self, ctx:CPP14Parser.DoStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CPP14Parser#ForStatement.
    def visitForStatement(self, ctx:CPP14Parser.ForStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CPP14Parser#ForRangeStatement.
    def visitForRangeStatement(self, ctx:CPP14Parser.ForRangeStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CPP14Parser#forinitstatement.
    def visitForinitstatement(self, ctx:CPP14Parser.ForinitstatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CPP14Parser#forrangedeclaration.
    def visitForrangedeclaration(self, ctx:CPP14Parser.ForrangedeclarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CPP14Parser#forrangeinitializer.
    def visitForrangeinitializer(self, ctx:CPP14Parser.ForrangeinitializerContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CPP14Parser#jumpstatement.
    def visitJumpstatement(self, ctx:CPP14Parser.JumpstatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CPP14Parser#declarationstatement.
    def visitDeclarationstatement(self, ctx:CPP14Parser.DeclarationstatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CPP14Parser#declarationseq.
    def visitDeclarationseq(self, ctx:CPP14Parser.DeclarationseqContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CPP14Parser#declaration.
    def visitDeclaration(self, ctx:CPP14Parser.DeclarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CPP14Parser#blockdeclaration.
    def visitBlockdeclaration(self, ctx:CPP14Parser.BlockdeclarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CPP14Parser#aliasdeclaration.
    def visitAliasdeclaration(self, ctx:CPP14Parser.AliasdeclarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CPP14Parser#simpledeclaration.
    def visitSimpledeclaration(self, ctx:CPP14Parser.SimpledeclarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CPP14Parser#static_assertdeclaration.
    def visitStatic_assertdeclaration(self, ctx:CPP14Parser.Static_assertdeclarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CPP14Parser#emptydeclaration.
    def visitEmptydeclaration(self, ctx:CPP14Parser.EmptydeclarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CPP14Parser#attributedeclaration.
    def visitAttributedeclaration(self, ctx:CPP14Parser.AttributedeclarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CPP14Parser#storageAttr.
    def visitStorageAttr(self, ctx:CPP14Parser.StorageAttrContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CPP14Parser#typeAttr.
    def visitTypeAttr(self, ctx:CPP14Parser.TypeAttrContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CPP14Parser#funcAttr.
    def visitFuncAttr(self, ctx:CPP14Parser.FuncAttrContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CPP14Parser#friendDecl.
    def visitFriendDecl(self, ctx:CPP14Parser.FriendDeclContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CPP14Parser#typedefDecl.
    def visitTypedefDecl(self, ctx:CPP14Parser.TypedefDeclContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CPP14Parser#constExprDecl.
    def visitConstExprDecl(self, ctx:CPP14Parser.ConstExprDeclContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CPP14Parser#declspecifierseq.
    def visitDeclspecifierseq(self, ctx:CPP14Parser.DeclspecifierseqContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CPP14Parser#storageclassspecifier.
    def visitStorageclassspecifier(self, ctx:CPP14Parser.StorageclassspecifierContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CPP14Parser#functionspecifier.
    def visitFunctionspecifier(self, ctx:CPP14Parser.FunctionspecifierContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CPP14Parser#typedefname.
    def visitTypedefname(self, ctx:CPP14Parser.TypedefnameContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CPP14Parser#otherDecl.
    def visitOtherDecl(self, ctx:CPP14Parser.OtherDeclContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CPP14Parser#classDecl.
    def visitClassDecl(self, ctx:CPP14Parser.ClassDeclContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CPP14Parser#enumDecl.
    def visitEnumDecl(self, ctx:CPP14Parser.EnumDeclContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CPP14Parser#trailingtypespecifier.
    def visitTrailingtypespecifier(self, ctx:CPP14Parser.TrailingtypespecifierContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CPP14Parser#typespecifierseq.
    def visitTypespecifierseq(self, ctx:CPP14Parser.TypespecifierseqContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CPP14Parser#trailingtypespecifierseq.
    def visitTrailingtypespecifierseq(self, ctx:CPP14Parser.TrailingtypespecifierseqContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CPP14Parser#simpletypespecifier.
    def visitSimpletypespecifier(self, ctx:CPP14Parser.SimpletypespecifierContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CPP14Parser#thetypename.
    def visitThetypename(self, ctx:CPP14Parser.ThetypenameContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CPP14Parser#decltypespecifier.
    def visitDecltypespecifier(self, ctx:CPP14Parser.DecltypespecifierContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CPP14Parser#elaboratedtypespecifier.
    def visitElaboratedtypespecifier(self, ctx:CPP14Parser.ElaboratedtypespecifierContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CPP14Parser#enumname.
    def visitEnumname(self, ctx:CPP14Parser.EnumnameContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CPP14Parser#enumspecifier.
    def visitEnumspecifier(self, ctx:CPP14Parser.EnumspecifierContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CPP14Parser#enumhead.
    def visitEnumhead(self, ctx:CPP14Parser.EnumheadContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CPP14Parser#opaqueenumdeclaration.
    def visitOpaqueenumdeclaration(self, ctx:CPP14Parser.OpaqueenumdeclarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CPP14Parser#enumkey.
    def visitEnumkey(self, ctx:CPP14Parser.EnumkeyContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CPP14Parser#enumbase.
    def visitEnumbase(self, ctx:CPP14Parser.EnumbaseContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CPP14Parser#enumeratorlist.
    def visitEnumeratorlist(self, ctx:CPP14Parser.EnumeratorlistContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CPP14Parser#enumeratordefinition.
    def visitEnumeratordefinition(self, ctx:CPP14Parser.EnumeratordefinitionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CPP14Parser#enumerator.
    def visitEnumerator(self, ctx:CPP14Parser.EnumeratorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CPP14Parser#namespacename.
    def visitNamespacename(self, ctx:CPP14Parser.NamespacenameContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CPP14Parser#originalnamespacename.
    def visitOriginalnamespacename(self, ctx:CPP14Parser.OriginalnamespacenameContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CPP14Parser#namespacedefinition.
    def visitNamespacedefinition(self, ctx:CPP14Parser.NamespacedefinitionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CPP14Parser#namednamespacedefinition.
    def visitNamednamespacedefinition(self, ctx:CPP14Parser.NamednamespacedefinitionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CPP14Parser#originalnamespacedefinition.
    def visitOriginalnamespacedefinition(self, ctx:CPP14Parser.OriginalnamespacedefinitionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CPP14Parser#extensionnamespacedefinition.
    def visitExtensionnamespacedefinition(self, ctx:CPP14Parser.ExtensionnamespacedefinitionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CPP14Parser#unnamednamespacedefinition.
    def visitUnnamednamespacedefinition(self, ctx:CPP14Parser.UnnamednamespacedefinitionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CPP14Parser#namespacebody.
    def visitNamespacebody(self, ctx:CPP14Parser.NamespacebodyContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CPP14Parser#namespacealias.
    def visitNamespacealias(self, ctx:CPP14Parser.NamespacealiasContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CPP14Parser#namespacealiasdefinition.
    def visitNamespacealiasdefinition(self, ctx:CPP14Parser.NamespacealiasdefinitionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CPP14Parser#qualifiednamespacespecifier.
    def visitQualifiednamespacespecifier(self, ctx:CPP14Parser.QualifiednamespacespecifierContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CPP14Parser#usingdeclaration.
    def visitUsingdeclaration(self, ctx:CPP14Parser.UsingdeclarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CPP14Parser#usingdirective.
    def visitUsingdirective(self, ctx:CPP14Parser.UsingdirectiveContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CPP14Parser#asmdefinition.
    def visitAsmdefinition(self, ctx:CPP14Parser.AsmdefinitionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CPP14Parser#linkagespecification.
    def visitLinkagespecification(self, ctx:CPP14Parser.LinkagespecificationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CPP14Parser#attributespecifierseq.
    def visitAttributespecifierseq(self, ctx:CPP14Parser.AttributespecifierseqContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CPP14Parser#attributespecifier.
    def visitAttributespecifier(self, ctx:CPP14Parser.AttributespecifierContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CPP14Parser#alignmentspecifier.
    def visitAlignmentspecifier(self, ctx:CPP14Parser.AlignmentspecifierContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CPP14Parser#attributelist.
    def visitAttributelist(self, ctx:CPP14Parser.AttributelistContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CPP14Parser#attribute.
    def visitAttribute(self, ctx:CPP14Parser.AttributeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CPP14Parser#attributetoken.
    def visitAttributetoken(self, ctx:CPP14Parser.AttributetokenContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CPP14Parser#attributescopedtoken.
    def visitAttributescopedtoken(self, ctx:CPP14Parser.AttributescopedtokenContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CPP14Parser#attributenamespace.
    def visitAttributenamespace(self, ctx:CPP14Parser.AttributenamespaceContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CPP14Parser#attributeargumentclause.
    def visitAttributeargumentclause(self, ctx:CPP14Parser.AttributeargumentclauseContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CPP14Parser#balancedtokenseq.
    def visitBalancedtokenseq(self, ctx:CPP14Parser.BalancedtokenseqContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CPP14Parser#balancedtoken.
    def visitBalancedtoken(self, ctx:CPP14Parser.BalancedtokenContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CPP14Parser#initdeclaratorlist.
    def visitInitdeclaratorlist(self, ctx:CPP14Parser.InitdeclaratorlistContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CPP14Parser#initdeclarator.
    def visitInitdeclarator(self, ctx:CPP14Parser.InitdeclaratorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CPP14Parser#declarator.
    def visitDeclarator(self, ctx:CPP14Parser.DeclaratorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CPP14Parser#nonPtrDecl.
    def visitNonPtrDecl(self, ctx:CPP14Parser.NonPtrDeclContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CPP14Parser#ptrDecl.
    def visitPtrDecl(self, ctx:CPP14Parser.PtrDeclContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CPP14Parser#noptrIgnore.
    def visitNoptrIgnore(self, ctx:CPP14Parser.NoptrIgnoreContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CPP14Parser#normalVarDecl.
    def visitNormalVarDecl(self, ctx:CPP14Parser.NormalVarDeclContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CPP14Parser#arrayDecl.
    def visitArrayDecl(self, ctx:CPP14Parser.ArrayDeclContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CPP14Parser#parametersandqualifiers.
    def visitParametersandqualifiers(self, ctx:CPP14Parser.ParametersandqualifiersContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CPP14Parser#trailingreturntype.
    def visitTrailingreturntype(self, ctx:CPP14Parser.TrailingreturntypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CPP14Parser#ptroperator.
    def visitPtroperator(self, ctx:CPP14Parser.PtroperatorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CPP14Parser#cvqualifierseq.
    def visitCvqualifierseq(self, ctx:CPP14Parser.CvqualifierseqContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CPP14Parser#cvqualifier.
    def visitCvqualifier(self, ctx:CPP14Parser.CvqualifierContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CPP14Parser#refqualifier.
    def visitRefqualifier(self, ctx:CPP14Parser.RefqualifierContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CPP14Parser#declaratorid.
    def visitDeclaratorid(self, ctx:CPP14Parser.DeclaratoridContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CPP14Parser#thetypeid.
    def visitThetypeid(self, ctx:CPP14Parser.ThetypeidContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CPP14Parser#abstractdeclarator.
    def visitAbstractdeclarator(self, ctx:CPP14Parser.AbstractdeclaratorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CPP14Parser#ptrabstractdeclarator.
    def visitPtrabstractdeclarator(self, ctx:CPP14Parser.PtrabstractdeclaratorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CPP14Parser#noptrabstractdeclarator.
    def visitNoptrabstractdeclarator(self, ctx:CPP14Parser.NoptrabstractdeclaratorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CPP14Parser#abstractpackdeclarator.
    def visitAbstractpackdeclarator(self, ctx:CPP14Parser.AbstractpackdeclaratorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CPP14Parser#noptrabstractpackdeclarator.
    def visitNoptrabstractpackdeclarator(self, ctx:CPP14Parser.NoptrabstractpackdeclaratorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CPP14Parser#parameterdeclarationclause.
    def visitParameterdeclarationclause(self, ctx:CPP14Parser.ParameterdeclarationclauseContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CPP14Parser#parameterdeclarationlist.
    def visitParameterdeclarationlist(self, ctx:CPP14Parser.ParameterdeclarationlistContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CPP14Parser#parameterdeclaration.
    def visitParameterdeclaration(self, ctx:CPP14Parser.ParameterdeclarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CPP14Parser#functiondefinition.
    def visitFunctiondefinition(self, ctx:CPP14Parser.FunctiondefinitionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CPP14Parser#functionbody.
    def visitFunctionbody(self, ctx:CPP14Parser.FunctionbodyContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CPP14Parser#initDeclWithAssignList.
    def visitInitDeclWithAssignList(self, ctx:CPP14Parser.InitDeclWithAssignListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CPP14Parser#initDeclWithCall.
    def visitInitDeclWithCall(self, ctx:CPP14Parser.InitDeclWithCallContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CPP14Parser#initDeclWithAssign.
    def visitInitDeclWithAssign(self, ctx:CPP14Parser.InitDeclWithAssignContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CPP14Parser#initDeclWithList.
    def visitInitDeclWithList(self, ctx:CPP14Parser.InitDeclWithListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CPP14Parser#normalAssign.
    def visitNormalAssign(self, ctx:CPP14Parser.NormalAssignContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CPP14Parser#arrayAssign.
    def visitArrayAssign(self, ctx:CPP14Parser.ArrayAssignContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CPP14Parser#initializerlist.
    def visitInitializerlist(self, ctx:CPP14Parser.InitializerlistContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CPP14Parser#bracedinitlist.
    def visitBracedinitlist(self, ctx:CPP14Parser.BracedinitlistContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CPP14Parser#classname.
    def visitClassname(self, ctx:CPP14Parser.ClassnameContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CPP14Parser#classspecifier.
    def visitClassspecifier(self, ctx:CPP14Parser.ClassspecifierContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CPP14Parser#classhead.
    def visitClasshead(self, ctx:CPP14Parser.ClassheadContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CPP14Parser#classheadname.
    def visitClassheadname(self, ctx:CPP14Parser.ClassheadnameContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CPP14Parser#classvirtspecifier.
    def visitClassvirtspecifier(self, ctx:CPP14Parser.ClassvirtspecifierContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CPP14Parser#classkey.
    def visitClasskey(self, ctx:CPP14Parser.ClasskeyContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CPP14Parser#memberspecification.
    def visitMemberspecification(self, ctx:CPP14Parser.MemberspecificationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CPP14Parser#memberVarDecl.
    def visitMemberVarDecl(self, ctx:CPP14Parser.MemberVarDeclContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CPP14Parser#memberFuncDecl.
    def visitMemberFuncDecl(self, ctx:CPP14Parser.MemberFuncDeclContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CPP14Parser#memberUsing.
    def visitMemberUsing(self, ctx:CPP14Parser.MemberUsingContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CPP14Parser#memberStaticAssert.
    def visitMemberStaticAssert(self, ctx:CPP14Parser.MemberStaticAssertContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CPP14Parser#memberTemplateDecl.
    def visitMemberTemplateDecl(self, ctx:CPP14Parser.MemberTemplateDeclContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CPP14Parser#memberAliasDecl.
    def visitMemberAliasDecl(self, ctx:CPP14Parser.MemberAliasDeclContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CPP14Parser#memberEmpty.
    def visitMemberEmpty(self, ctx:CPP14Parser.MemberEmptyContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CPP14Parser#memberdeclaratorlist.
    def visitMemberdeclaratorlist(self, ctx:CPP14Parser.MemberdeclaratorlistContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CPP14Parser#memberdeclarator.
    def visitMemberdeclarator(self, ctx:CPP14Parser.MemberdeclaratorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CPP14Parser#virtspecifierseq.
    def visitVirtspecifierseq(self, ctx:CPP14Parser.VirtspecifierseqContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CPP14Parser#virtspecifier.
    def visitVirtspecifier(self, ctx:CPP14Parser.VirtspecifierContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CPP14Parser#purespecifier.
    def visitPurespecifier(self, ctx:CPP14Parser.PurespecifierContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CPP14Parser#baseclause.
    def visitBaseclause(self, ctx:CPP14Parser.BaseclauseContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CPP14Parser#basespecifierlist.
    def visitBasespecifierlist(self, ctx:CPP14Parser.BasespecifierlistContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CPP14Parser#basespecifier.
    def visitBasespecifier(self, ctx:CPP14Parser.BasespecifierContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CPP14Parser#classordecltype.
    def visitClassordecltype(self, ctx:CPP14Parser.ClassordecltypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CPP14Parser#basetypespecifier.
    def visitBasetypespecifier(self, ctx:CPP14Parser.BasetypespecifierContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CPP14Parser#accessspecifier.
    def visitAccessspecifier(self, ctx:CPP14Parser.AccessspecifierContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CPP14Parser#conversionfunctionid.
    def visitConversionfunctionid(self, ctx:CPP14Parser.ConversionfunctionidContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CPP14Parser#conversiontypeid.
    def visitConversiontypeid(self, ctx:CPP14Parser.ConversiontypeidContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CPP14Parser#conversiondeclarator.
    def visitConversiondeclarator(self, ctx:CPP14Parser.ConversiondeclaratorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CPP14Parser#ctorinitializer.
    def visitCtorinitializer(self, ctx:CPP14Parser.CtorinitializerContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CPP14Parser#meminitializerlist.
    def visitMeminitializerlist(self, ctx:CPP14Parser.MeminitializerlistContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CPP14Parser#meminitializer.
    def visitMeminitializer(self, ctx:CPP14Parser.MeminitializerContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CPP14Parser#meminitializerid.
    def visitMeminitializerid(self, ctx:CPP14Parser.MeminitializeridContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CPP14Parser#operatorfunctionid.
    def visitOperatorfunctionid(self, ctx:CPP14Parser.OperatorfunctionidContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CPP14Parser#literaloperatorid.
    def visitLiteraloperatorid(self, ctx:CPP14Parser.LiteraloperatoridContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CPP14Parser#templatedeclaration.
    def visitTemplatedeclaration(self, ctx:CPP14Parser.TemplatedeclarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CPP14Parser#templateparameterlist.
    def visitTemplateparameterlist(self, ctx:CPP14Parser.TemplateparameterlistContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CPP14Parser#templateparameter.
    def visitTemplateparameter(self, ctx:CPP14Parser.TemplateparameterContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CPP14Parser#typeparameter.
    def visitTypeparameter(self, ctx:CPP14Parser.TypeparameterContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CPP14Parser#simpletemplateid.
    def visitSimpletemplateid(self, ctx:CPP14Parser.SimpletemplateidContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CPP14Parser#templateid.
    def visitTemplateid(self, ctx:CPP14Parser.TemplateidContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CPP14Parser#templatename.
    def visitTemplatename(self, ctx:CPP14Parser.TemplatenameContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CPP14Parser#templateargumentlist.
    def visitTemplateargumentlist(self, ctx:CPP14Parser.TemplateargumentlistContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CPP14Parser#templateargument.
    def visitTemplateargument(self, ctx:CPP14Parser.TemplateargumentContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CPP14Parser#typenamespecifier.
    def visitTypenamespecifier(self, ctx:CPP14Parser.TypenamespecifierContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CPP14Parser#explicitinstantiation.
    def visitExplicitinstantiation(self, ctx:CPP14Parser.ExplicitinstantiationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CPP14Parser#explicitspecialization.
    def visitExplicitspecialization(self, ctx:CPP14Parser.ExplicitspecializationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CPP14Parser#tryblock.
    def visitTryblock(self, ctx:CPP14Parser.TryblockContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CPP14Parser#functiontryblock.
    def visitFunctiontryblock(self, ctx:CPP14Parser.FunctiontryblockContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CPP14Parser#handlerseq.
    def visitHandlerseq(self, ctx:CPP14Parser.HandlerseqContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CPP14Parser#handler.
    def visitHandler(self, ctx:CPP14Parser.HandlerContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CPP14Parser#exceptiondeclaration.
    def visitExceptiondeclaration(self, ctx:CPP14Parser.ExceptiondeclarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CPP14Parser#throwexpression.
    def visitThrowexpression(self, ctx:CPP14Parser.ThrowexpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CPP14Parser#exceptionspecification.
    def visitExceptionspecification(self, ctx:CPP14Parser.ExceptionspecificationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CPP14Parser#dynamicexceptionspecification.
    def visitDynamicexceptionspecification(self, ctx:CPP14Parser.DynamicexceptionspecificationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CPP14Parser#typeidlist.
    def visitTypeidlist(self, ctx:CPP14Parser.TypeidlistContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CPP14Parser#noexceptspecification.
    def visitNoexceptspecification(self, ctx:CPP14Parser.NoexceptspecificationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CPP14Parser#rightShift.
    def visitRightShift(self, ctx:CPP14Parser.RightShiftContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CPP14Parser#rightShiftAssign.
    def visitRightShiftAssign(self, ctx:CPP14Parser.RightShiftAssignContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CPP14Parser#theoperator.
    def visitTheoperator(self, ctx:CPP14Parser.TheoperatorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CPP14Parser#literal.
    def visitLiteral(self, ctx:CPP14Parser.LiteralContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CPP14Parser#booleanliteral.
    def visitBooleanliteral(self, ctx:CPP14Parser.BooleanliteralContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CPP14Parser#pointerliteral.
    def visitPointerliteral(self, ctx:CPP14Parser.PointerliteralContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CPP14Parser#userdefinedliteral.
    def visitUserdefinedliteral(self, ctx:CPP14Parser.UserdefinedliteralContext):
        return self.visitChildren(ctx)



del CPP14Parser