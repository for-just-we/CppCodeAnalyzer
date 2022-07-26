/*******************************************************************************
 * The MIT License (MIT)
 *
 * Copyright (c) 2015 Camilo Sanchez (Camiloasc1)
 *
 * Permission is hereby granted, free of charge, to any person obtaining a copy
 * of this software and associated documentation files (the "Software"), to deal
 * in the Software without restriction, including without limitation the rights
 * to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
 * copies of the Software, and to permit persons to whom the Software is
 * furnished to do so, subject to the following conditions:
 *
 * The above copyright notice and this permission notice shall be included in all
 * copies or substantial portions of the Software.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 * IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 * FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
 * AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 * LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
 * OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
 * SOFTWARE.
 ******************************************************************************/

/*******************************************************************************
 * C++14 Grammar for ANTLR v4
 *
 * Based on n4140 draft paper
 * https://github.com/cplusplus/draft/blob/master/papers/n4140.pdf
 * and
 * http://www.nongnu.org/hcb/
 *
 * Possible Issues:
 *
 * Input must avoid conditional compilation blocks (this grammar ignores any preprocessor directive)
 * GCC extensions not yet supported (do not try to parse the preprocessor output)
 * Right angle bracket (C++11) - Solution '>>' and '>>=' are not tokens, only '>'
 * Lexer issue with pure-specifier rule ('0' token) - Solution in embedded code
 *   Change it to match the target language you want in line 1097 or verify inside your listeners/visitors
 *   Java:
if($val.text.compareTo("0")!=0) throw new InputMismatchException(this);
 *   JavaScript:

 *   Python2:

 *   Python3:

 *   C#:

 ******************************************************************************/
grammar CPP14;

/*Basic concepts*/
translationunit
:
	declarationseq? EOF
;

/*Expressions*/
primaryexpression
:
	literal
	| This
	| '(' expression ')'
	| idexpression
	| lambdaexpression
;

idexpression
:
	unqualifiedid
	| qualifiedid
;

unqualifiedid
:
	Identifier
	| operatorfunctionid
	| conversionfunctionid
	| literaloperatorid
	| '~' classname
	| '~' decltypespecifier
	| templateid
;

qualifiedid // qualified通常包含::
:
	nestednamespecifier Template? unqualifiedid
;

nestednamespecifier
:
	'::' #normalGlobalIdentifier
	| thetypename '::' #classIdentifier
	| namespacename '::' #namespaceIdentifier
	| decltypespecifier '::' #decltypeIdentifier
	| nestednamespecifier Identifier '::' #nestedIdentifier
	| nestednamespecifier Template? simpletemplateid '::' #nestedTemplateIdentifier
;

lambdaexpression
:
	lambdaintroducer lambdadeclarator? compoundstatement
;

lambdaintroducer
:
	'[' lambdacapture? ']'
;

lambdacapture
:
	capturedefault
	| capturelist
	| capturedefault ',' capturelist
;

capturedefault
:
	'&'
	| '='
;

capturelist
:
	capture '...'?
	| capturelist ',' capture '...'?
;

capture
:
	simplecapture
	| initcapture
;

simplecapture
:
	Identifier
	| '&' Identifier
	| This
;

initcapture
:
	Identifier initializer
	| '&' Identifier initializer
;

lambdadeclarator
:
	'(' parameterdeclarationclause ')' Mutable? exceptionspecification?
	attributespecifierseq? trailingreturntype?
;

postfixexpression
:
	primaryexpression #postfixIgnore
	| postfixexpression '[' expression ']' #arrayIndexing
	| postfixexpression '[' bracedinitlist ']' #postfixIgnore//没见过这种语法，aaa[{1, 2, 3}];
	| postfixexpression '(' expressionlist? ')' #functionCall//funcCall
	| simpletypespecifier '(' expressionlist? ')' #postSimpleCastExpression// 类型转换，CastExpression，simpletypespecifier是castTarget
	| typenamespecifier '(' expressionlist? ')' #postTypeCastExpression// 调用静态方法？
	| simpletypespecifier bracedinitlist  #postfixIgnore//先忽视这种语法
	| typenamespecifier bracedinitlist #postfixIgnore//先忽视这种语法
	| postfixexpression '.' Template? idexpression #memberAccess//memberAccess
	| postfixexpression '->' Template? idexpression #ptrMemberAccess// ptrMemberAccess
	| postfixexpression '.' pseudodestructorname #memberAccess//memberAccess
	| postfixexpression '->' pseudodestructorname #ptrMemberAccess// ptrMemberAccess
	| postfixexpression '++' #incDecOp
	| postfixexpression '--' #incDecOp
	| Dynamic_cast '<' thetypeid '>' '(' expression ')' #CppCastExpression
	| Static_cast '<' thetypeid '>' '(' expression ')' #CppCastExpression
	| Reinterpret_cast '<' thetypeid '>' '(' expression ')' #CppCastExpression
	| Const_cast '<' thetypeid '>' '(' expression ')' #CppCastExpression
	| Typeid '(' expression ')' #TypeidExpression
	| Typeid '(' thetypeid ')' #TypeidExpression
;

expressionlist
:
	initializerlist
;

pseudodestructorname
:
	nestednamespecifier? thetypename '::' '~' thetypename
	| nestednamespecifier Template simpletemplateid '::' '~' thetypename
	| nestednamespecifier? '~' thetypename
	| '~' decltypespecifier
;

unaryexpression
:
	postfixexpression
	| '++' castexpression
	| '--' castexpression
	| unaryoperator castexpression
	| sizeofExpression
	| alignofExpression
	| noexceptexpression
	| newexpression
	| deleteexpression
;

sizeofExpression
:
    Sizeof unaryexpression
    | Sizeof '(' thetypeid ')'
    | Sizeof '...' '(' Identifier ')' //还从没见过可变参数语法，这里直接忽略了
;

alignofExpression
:
    Alignof '(' thetypeid ')'
;


unaryoperator
:
	'|'
	| '*'
	| '&'
	| '+'
	| '!'
	| '~'
	| '-'
;

newexpression
:
	'::'? New newplacement? newtypeid newinitializer?
	| '::'? New newplacement? '(' thetypeid ')' newinitializer?
;

newplacement
:
	'(' expressionlist ')'
;

newtypeid
:
	typespecifierseq newdeclarator?
;

newdeclarator
:
	ptroperator newdeclarator? #ptrNewDeclarator
	| noptrnewdeclarator #nonPtrNewDeclarator
;

noptrnewdeclarator
:
	'[' expression ']' attributespecifierseq?
	| noptrnewdeclarator '[' constantexpression ']' attributespecifierseq?
;

newinitializer
:
	'(' expressionlist? ')'
	| bracedinitlist
;

deleteexpression
:
	'::'? Delete castexpression
	| '::'? Delete '[' ']' castexpression
;

noexceptexpression
:
	Noexcept '(' expression ')'
;

castexpression
:
	unaryexpression
	| '(' thetypeid ')' castexpression
;

pmexpression
:
	castexpression
	| pmexpression '.*' castexpression
	| pmexpression '->*' castexpression
;

multiplicativeexpression
:
	pmexpression
	| multiplicativeexpression '*' pmexpression
	| multiplicativeexpression '/' pmexpression
	| multiplicativeexpression '%' pmexpression
;

additiveexpression
:
	multiplicativeexpression
	| additiveexpression '+' multiplicativeexpression
	| additiveexpression '-' multiplicativeexpression
;

shiftexpression
:
	additiveexpression
	| shiftexpression '<<' additiveexpression
	| shiftexpression rightShift additiveexpression
;

relationalexpression
:
	shiftexpression
	| relationalexpression '<' shiftexpression
	| relationalexpression '>' shiftexpression
	| relationalexpression '<=' shiftexpression
	| relationalexpression '>=' shiftexpression
;

equalityexpression
:
	relationalexpression
	| equalityexpression '==' relationalexpression
	| equalityexpression '!=' relationalexpression
;

andexpression
:
	equalityexpression
	| andexpression '&' equalityexpression
;

exclusiveorexpression
:
	andexpression
	| exclusiveorexpression '^' andexpression
;

inclusiveorexpression
:
	exclusiveorexpression
	| inclusiveorexpression '|' exclusiveorexpression
;

logicalandexpression
:
	inclusiveorexpression
	| logicalandexpression '&&' inclusiveorexpression
;

logicalorexpression
:
	logicalandexpression
	| logicalorexpression '||' logicalandexpression
;

conditionalexpression
:
	logicalorexpression #nonConditionalExpression
	| logicalorexpression '?' expression ':' assignmentexpression #realConditionalExpression
;

assignmentexpression
:
	conditionalexpression
	| logicalorexpression assignmentoperator initializerclause
	| throwexpression
;

assignmentoperator
:
	'='
	| '*='
	| '/='
	| '%='
	| '+='
	| '-='
	| rightShiftAssign
	| '<<='
	| '&='
	| '^='
	| '|='
;

expression
:
	assignmentexpression
	| expression ',' assignmentexpression
;

constantexpression
:
	conditionalexpression
;
/*Statements*/
statement
:
	labeledstatement
	| attributespecifierseq? expressionstatement // 表达式语句
	| attributespecifierseq? compoundstatement // 块语句
	| attributespecifierseq? selectionstatement // if-else, switch
	| attributespecifierseq? iterationstatement // for, forrange, while, do-while
	| attributespecifierseq? jumpstatement // break, continue, goto, return
	| declarationstatement // 定义
	| attributespecifierseq? tryblock
;

label
:
    attributespecifierseq? Identifier ':'
    | attributespecifierseq? Case constantexpression ':'
    | attributespecifierseq? Default ':'
;

labeledstatement
:
	label statement
;

expressionstatement
:
	expression? ';'
;

compoundstatement
:
	'{' statementseq? '}'
;

statementseq
:
	statement
	| statementseq statement
;

selectionstatement
:
	If '(' condition ')' statement  # ifStatement
	| If '(' condition ')' statement Else statement #ifStatement
	| Switch '(' condition ')' statement #switchStatement
;

condition
:
	expression
	| attributespecifierseq? declspecifierseq declarator '=' initializerclause
	| attributespecifierseq? declspecifierseq declarator bracedinitlist
;

iterationstatement
:
	While '(' condition ')' statement  #WhileStatement
	| Do statement While '(' condition ')' ';' #DoStatement
	| For '(' forinitstatement condition? ';' expression? ')' statement  #ForStatement
	| For '(' forrangedeclaration ':' forrangeinitializer ')' statement # ForRangeStatement
;

forinitstatement
:
	expressionstatement
	| simpledeclaration
;

forrangedeclaration
:
	attributespecifierseq? declspecifierseq declarator
;

forrangeinitializer
:
	expression
	| bracedinitlist
;

jumpstatement
:
	Break ';'
	| Continue ';'
	| Return expression? ';'
	| Return bracedinitlist ';'
	| Goto Identifier ';'
;

declarationstatement
:
	blockdeclaration
;

/*Declarations*/
declarationseq
:
	declaration
	| declarationseq declaration
;

declaration
:
	blockdeclaration
	| functiondefinition //函数定义
	| templatedeclaration
	| explicitinstantiation
	| explicitspecialization
	| linkagespecification
	| namespacedefinition
	| emptydeclaration
	| attributedeclaration
;

blockdeclaration
:
	simpledeclaration
	| asmdefinition
	| namespacealiasdefinition
	| usingdeclaration
	| usingdirective
	| static_assertdeclaration
	| aliasdeclaration
	| opaqueenumdeclaration
;

aliasdeclaration
:
	Using Identifier attributespecifierseq? '=' thetypeid ';'
;

simpledeclaration
:
	declspecifierseq? initdeclaratorlist? ';'
	| attributespecifierseq declspecifierseq? initdeclaratorlist ';'
;

static_assertdeclaration
:
	Static_assert '(' constantexpression ',' Stringliteral ')' ';'
;

emptydeclaration
:
	';'
;

attributedeclaration
:
	attributespecifierseq ';'
;

declspecifier
:
	storageclassspecifier # storageAttr
	| typespecifier # typeAttr
	| functionspecifier # funcAttr // inline, virtual, explicit
	| Friend #friendDecl //友元类
	| Typedef #typedefDecl // typedef long long LL，joern会将其解析为 LL = long long
	| Constexpr #constExprDecl // constexpr表达式定义
;

declspecifierseq
:
	declspecifier attributespecifierseq?
	| declspecifier declspecifierseq
;

storageclassspecifier
:
	Register
	| Static
	| Thread_local
	| Extern
	| Mutable
;

functionspecifier
:
	Inline
	| Virtual
	| Explicit
;

typedefname
:
	Identifier
;

typespecifier
:
	trailingtypespecifier #otherDecl
	| classspecifier #classDecl
	| enumspecifier #enumDecl
;

trailingtypespecifier
:
	simpletypespecifier
	| elaboratedtypespecifier
	| typenamespecifier
	| cvqualifier
;

typespecifierseq
:
	typespecifier attributespecifierseq?
	| typespecifier typespecifierseq
;

trailingtypespecifierseq
:
	trailingtypespecifier attributespecifierseq?
	| trailingtypespecifier trailingtypespecifierseq
;

simpletypespecifier
:
	nestednamespecifier? thetypename //c++ style
	| nestednamespecifier Template simpletemplateid //c++ style
	| Char
	| Char16
	| Char32
	| Wchar
	| Bool
	| Short
	| Int
	| Long
	| Signed
	| Unsigned
	| Float
	| Double
	| Void
	| Auto
	| decltypespecifier
;

thetypename
:
	classname
	| enumname
	| typedefname
	| simpletemplateid
;

decltypespecifier
:
	Decltype '(' expression ')'
	| Decltype '(' Auto ')'
;

elaboratedtypespecifier
:
	classkey attributespecifierseq? nestednamespecifier? Identifier
	| classkey simpletemplateid
	| classkey nestednamespecifier Template? simpletemplateid
	| Enum nestednamespecifier? Identifier
;

enumname
:
	Identifier
;

enumspecifier
:
	enumhead '{' enumeratorlist? '}'
	| enumhead '{' enumeratorlist ',' '}'
;

enumhead
:
	enumkey attributespecifierseq? Identifier? enumbase?
	| enumkey attributespecifierseq? nestednamespecifier Identifier enumbase?
;

opaqueenumdeclaration
:
	enumkey attributespecifierseq? Identifier enumbase? ';'
;

enumkey
:
	Enum
	| Enum Class
	| Enum Struct
;

enumbase
:
	':' typespecifierseq
;

enumeratorlist
:
	enumeratordefinition
	| enumeratorlist ',' enumeratordefinition
;

enumeratordefinition
:
	enumerator
	| enumerator '=' constantexpression
;

enumerator
:
	Identifier
;

namespacename
:
	originalnamespacename
	| namespacealias
;

originalnamespacename
:
	Identifier
;

namespacedefinition
:
	namednamespacedefinition
	| unnamednamespacedefinition
;

namednamespacedefinition
:
	originalnamespacedefinition
	| extensionnamespacedefinition
;

originalnamespacedefinition
:
	Inline? Namespace Identifier '{' namespacebody '}'
;

extensionnamespacedefinition
:
	Inline? Namespace originalnamespacename '{' namespacebody '}'
;

unnamednamespacedefinition
:
	Inline? Namespace '{' namespacebody '}'
;

namespacebody
:
	declarationseq?
;

namespacealias
:
	Identifier
;

namespacealiasdefinition
:
	Namespace Identifier '=' qualifiednamespacespecifier ';'
;

qualifiednamespacespecifier
:
	nestednamespecifier? namespacename
;

usingdeclaration
:
	Using Typename? nestednamespecifier unqualifiedid ';'
	| Using '::' unqualifiedid ';'
;

usingdirective
:
	attributespecifierseq? Using Namespace nestednamespecifier? namespacename ';'
;

asmdefinition
:
	Asm '(' Stringliteral ')' ';'
;

linkagespecification
:
	Extern Stringliteral '{' declarationseq? '}'
	| Extern Stringliteral declaration
;

attributespecifierseq
:
	attributespecifier
	| attributespecifierseq attributespecifier
;

attributespecifier
:
	'[' '[' attributelist ']' ']'
	| alignmentspecifier
;

alignmentspecifier
:
	Alignas '(' thetypeid '...'? ')'
	| Alignas '(' constantexpression '...'? ')'
;

attributelist
:
	attribute?
	| attributelist ',' attribute?
	| attribute '...'
	| attributelist ',' attribute '...'
;

attribute
:
	attributetoken attributeargumentclause?
;

attributetoken
:
	Identifier
	| attributescopedtoken
;

attributescopedtoken
:
	attributenamespace '::' Identifier
;

attributenamespace
:
	Identifier
;

attributeargumentclause
:
	'(' balancedtokenseq ')'
;

balancedtokenseq
:
	balancedtoken?
	| balancedtokenseq balancedtoken
;

balancedtoken
:
	'(' balancedtokenseq ')'
	| '[' balancedtokenseq ']'
	| '{' balancedtokenseq '}'
	/*any token other than a parenthesis , a bracket , or a brace*/
;

/*Declarators*/
initdeclaratorlist
:
	initdeclarator
	| initdeclaratorlist ',' initdeclarator
;

initdeclarator
:
	declarator initializer?
;

declarator
:
	ptrdeclarator
	| noptrdeclarator parametersandqualifiers trailingreturntype
;

ptrdeclarator
:
	noptrdeclarator #nonPtrDecl
	| ptroperator ptrdeclarator #ptrDecl
;

noptrdeclarator //非指针类型定义
:
	declaratorid attributespecifierseq? #normalVarDecl// 普通变量定义
	| noptrdeclarator parametersandqualifiers #noptrIgnore // 不清楚这是什么语法，先忽略
	| noptrdeclarator '[' constantexpression? ']' attributespecifierseq? #arrayDecl// 数组定义, Type var[100];
	| '(' ptrdeclarator ')' #noptrIgnore// char (*p)，这个语法可能会和强制类型转换 char(var)混淆，因此忽略
;

parametersandqualifiers
:
	'(' parameterdeclarationclause ')' cvqualifierseq? refqualifier?
	exceptionspecification? attributespecifierseq?
;

trailingreturntype
:
	'->' trailingtypespecifierseq abstractdeclarator?
;

ptroperator
:
	'*' attributespecifierseq? cvqualifierseq?
	| '&' attributespecifierseq?
	| '&&' attributespecifierseq?
	| nestednamespecifier '*' attributespecifierseq? cvqualifierseq?
;

cvqualifierseq
:
	cvqualifier cvqualifierseq?
;

cvqualifier
:
	Const
	| Volatile
;

refqualifier
:
	'&'
	| '&&'
;

declaratorid
:
	'...'? idexpression
;

thetypeid
:
	typespecifierseq abstractdeclarator?
;

abstractdeclarator
:
	ptrabstractdeclarator
	| noptrabstractdeclarator? parametersandqualifiers trailingreturntype
	| abstractpackdeclarator
;

ptrabstractdeclarator
:
	noptrabstractdeclarator
	| ptroperator ptrabstractdeclarator?
;

noptrabstractdeclarator
:
	noptrabstractdeclarator parametersandqualifiers
	| parametersandqualifiers
	| noptrabstractdeclarator '[' constantexpression? ']' attributespecifierseq?
	| '[' constantexpression? ']' attributespecifierseq?
	| '(' ptrabstractdeclarator ')'
;

abstractpackdeclarator
:
	noptrabstractpackdeclarator
	| ptroperator abstractpackdeclarator
;

noptrabstractpackdeclarator
:
	noptrabstractpackdeclarator parametersandqualifiers
	| noptrabstractpackdeclarator '[' constantexpression? ']'
	attributespecifierseq?
	| '...'
;

parameterdeclarationclause
:
	parameterdeclarationlist? '...'?
	| parameterdeclarationlist ',' '...'
;

parameterdeclarationlist // 参数列表
:
	parameterdeclaration
	| parameterdeclarationlist ',' parameterdeclaration
;

parameterdeclaration
:
	attributespecifierseq? declspecifierseq declarator
	| attributespecifierseq? declspecifierseq declarator '=' initializerclause
	| attributespecifierseq? declspecifierseq abstractdeclarator?
	| attributespecifierseq? declspecifierseq abstractdeclarator? '='
	initializerclause
;

functiondefinition
:
	attributespecifierseq? declspecifierseq? declarator virtspecifierseq?
	functionbody
;

functionbody // 函数体
:
	ctorinitializer? compoundstatement
	| functiontryblock
	| '=' Default ';'
	| '=' Delete ';'
;

initializer
:
	braceorequalinitializer #initDeclWithAssignList
	| '(' expressionlist ')' #initDeclWithCall
;

braceorequalinitializer
:
	'=' initializerclause #initDeclWithAssign// 普通赋值初始化
	| bracedinitlist #initDeclWithList // C++列表初始化
;

initializerclause //初始化语句
:
	assignmentexpression #normalAssign // 普通变量赋值
	| bracedinitlist #arrayAssign //数组，结构体赋值
;

initializerlist
:
	initializerclause '...'?
	| initializerlist ',' initializerclause '...'?
;

bracedinitlist
:
	'{' initializerlist ','? '}'
	| '{' '}'
;

/*Classes*/
classname
:
	Identifier
	| simpletemplateid
;

classspecifier
:
	classhead '{' memberspecification? '}'
;

classhead
:
	classkey attributespecifierseq? classheadname classvirtspecifier? baseclause?
	| classkey attributespecifierseq? baseclause?
;

classheadname
:
	nestednamespecifier? classname
;

classvirtspecifier
:
	Final
;

classkey
:
	Class
	| Struct
	| Union
;

memberspecification // 结构体/类成员定义
:
	memberdeclaration memberspecification?
	| accessspecifier ':' memberspecification?
;

memberdeclaration
:
	attributespecifierseq? declspecifierseq? memberdeclaratorlist? ';' #memberVarDecl
	| functiondefinition #memberFuncDecl
	| usingdeclaration #memberUsing
	| static_assertdeclaration #memberStaticAssert
	| templatedeclaration #memberTemplateDecl
	| aliasdeclaration #memberAliasDecl
	| emptydeclaration #memberEmpty
;

memberdeclaratorlist
:
	memberdeclarator
	| memberdeclaratorlist ',' memberdeclarator
;

memberdeclarator
:
	declarator virtspecifierseq? purespecifier?
	| declarator braceorequalinitializer?
	| Identifier? attributespecifierseq? ':' constantexpression
;

virtspecifierseq
:
	virtspecifier
	| virtspecifierseq virtspecifier
;

virtspecifier
:
	Override
	| Final
;

/*
purespecifier:
	'=' '0'//Conflicts with the lexer
 ;
 */
purespecifier
:
	Assign val = Octalliteral
	{if($val.text.compareTo("0")!=0) throw new InputMismatchException(this);}

;

/*Derived classes*/
baseclause
:
	':' basespecifierlist
;

basespecifierlist
:
	basespecifier '...'?
	| basespecifierlist ',' basespecifier '...'?
;

basespecifier
:
	attributespecifierseq? basetypespecifier
	| attributespecifierseq? Virtual accessspecifier? basetypespecifier
	| attributespecifierseq? accessspecifier Virtual? basetypespecifier
;

classordecltype
:
	nestednamespecifier? classname
	| decltypespecifier
;

basetypespecifier
:
	classordecltype
;

accessspecifier
:
	Private
	| Protected
	| Public
;

/*Special member functions*/
conversionfunctionid
:
	Operator conversiontypeid
;

conversiontypeid
:
	typespecifierseq conversiondeclarator?
;

conversiondeclarator
:
	ptroperator conversiondeclarator?
;

ctorinitializer
:
	':' meminitializerlist
;

meminitializerlist
:
	meminitializer '...'?
	| meminitializer '...'? ',' meminitializerlist
;

meminitializer
:
	meminitializerid '(' expressionlist? ')'
	| meminitializerid bracedinitlist
;

meminitializerid
:
	classordecltype
	| Identifier
;

/*Overloading*/
operatorfunctionid
:
	Operator theoperator
;

literaloperatorid
:
	Operator Stringliteral Identifier
	| Operator Userdefinedstringliteral
;

/*Templates*/
templatedeclaration
:
	Template '<' templateparameterlist '>' declaration
;

templateparameterlist
:
	templateparameter
	| templateparameterlist ',' templateparameter
;

templateparameter
:
	typeparameter
	| parameterdeclaration
;

typeparameter
:
	Class '...'? Identifier?
	| Class Identifier? '=' thetypeid
	| Typename '...'? Identifier?
	| Typename Identifier? '=' thetypeid
	| Template '<' templateparameterlist '>' Class '...'? Identifier?
	| Template '<' templateparameterlist '>' Class Identifier? '=' idexpression
;

simpletemplateid
:
	templatename '<' templateargumentlist? '>'
;

templateid
:
	simpletemplateid
	| operatorfunctionid '<' templateargumentlist? '>'
	| literaloperatorid '<' templateargumentlist? '>'
;

templatename
:
	Identifier
;

templateargumentlist
:
	templateargument '...'?
	| templateargumentlist ',' templateargument '...'?
;

templateargument
:
	thetypeid
	| constantexpression
	| idexpression
;

typenamespecifier
:
	Typename nestednamespecifier Identifier
	| Typename nestednamespecifier Template? simpletemplateid
;

explicitinstantiation
:
	Extern? Template declaration
;

explicitspecialization
:
	Template '<' '>' declaration
;

/*Exception handling*/
tryblock
:
	Try compoundstatement handlerseq
;

functiontryblock
:
	Try ctorinitializer? compoundstatement handlerseq
;

handlerseq
:
	handler handlerseq?
;

handler
:
	Catch '(' exceptiondeclaration ')' compoundstatement
;

exceptiondeclaration
:
	attributespecifierseq? typespecifierseq declarator
	| attributespecifierseq? typespecifierseq abstractdeclarator?
	| '...'
;

throwexpression
:
	Throw assignmentexpression?
;

exceptionspecification
:
	dynamicexceptionspecification
	| noexceptspecification
;

dynamicexceptionspecification
:
	Throw '(' typeidlist? ')'
;

typeidlist
:
	thetypeid '...'?
	| typeidlist ',' thetypeid '...'?
;

noexceptspecification
:
	Noexcept '(' constantexpression ')'
	| Noexcept
;

/*Preprocessing directives*/

MultiLineMacro
:
    '#' (~[\n]*? '\\' '\r'? '\n')+ ~[\n]+ -> channel(HIDDEN)
;

Directive
:
    '#' ~[\n]* -> channel(HIDDEN)
;

/*Lexer*/

/*Keywords*/
Alignas
:
	'alignas'
;

Alignof
:
	'alignof'
;

Asm
:
	'asm'
;

Auto
:
	'auto'
;

Bool
:
	'bool'
;

Break
:
	'break'
;

Case
:
	'case'
;

Catch
:
	'catch'
;

Char
:
	'char'
;

Char16
:
	'char16_t'
;

Char32
:
	'char32_t'
;

Class
:
	'class'
;

Const
:
	'const'
;

Constexpr
:
	'constexpr'
;

Const_cast
:
	'const_cast'
;

Continue
:
	'continue'
;

Decltype
:
	'decltype'
;

Default
:
	'default'
;

Delete
:
	'delete'
;

Do
:
	'do'
;

Double
:
	'double'
;

Dynamic_cast
:
	'dynamic_cast'
;

Else
:
	'else'
;

Enum
:
	'enum'
;

Explicit
:
	'explicit'
;

Export
:
	'export'
;

Extern
:
	'extern'
;

FalseToken
:
	'false'
;

Final
:
	'final'
;

Float
:
	'float'
;

For
:
	'for'
;

Friend
:
	'friend'
;

Goto
:
	'goto'
;

If
:
	'if'
;

Inline
:
	'inline'
;

Int
:
	'int'
;

Long
:
	'long'
;

Mutable
:
	'mutable'
;

Namespace
:
	'namespace'
;

New
:
	'new'
;

Noexcept
:
	'noexcept'
;

Nullptr
:
	'nullptr' | 'NULL'
;

Operator
:
	'operator'
;

Override
:
	'override'
;

Private
:
	'private'
;

Protected
:
	'protected'
;

Public
:
	'public'
;

Register
:
	'register'
;

Reinterpret_cast
:
	'reinterpret_cast'
;

Return
:
	'return'
;

Short
:
	'short'
;

Signed
:
	'signed'
;

Sizeof
:
	'sizeof'
;

Static
:
	'static'
;

Static_assert
:
	'static_assert'
;

Static_cast
:
	'static_cast'
;

Struct
:
	'struct'
;

Switch
:
	'switch'
;

Template
:
	'template'
;

This
:
	'this'
;

Thread_local
:
	'thread_local'
;

Throw
:
	'throw'
;

TrueToken
:
	'true'
;

Try
:
	'try'
;

Typedef
:
	'typedef'
;

Typeid
:
	'typeid'
;

Typename
:
	'typename'
;

Union
:
	'union'
;

Unsigned
:
	'unsigned'
;

Using
:
	'using'
;

Virtual
:
	'virtual'
;

Void
:
	'void'
;

Volatile
:
	'volatile'
;

Wchar
:
	'wchar_t'
;

While
:
	'while'
;

/*Operators*/
LeftParen
:
	'('
;

RightParen
:
	')'
;

LeftBracket
:
	'['
;

RightBracket
:
	']'
;

LeftBrace
:
	'{'
;

RightBrace
:
	'}'
;

Plus
:
	'+'
;

Minus
:
	'-'
;

Star
:
	'*'
;

Div
:
	'/'
;

Mod
:
	'%'
;

Caret
:
	'^'
;

And
:
	'&'
;

Or
:
	'|'
;

Tilde
:
	'~'
;

Not
:
	'!'
;

Assign
:
	'='
;

Less
:
	'<'
;

Greater
:
	'>'
;

PlusAssign
:
	'+='
;

MinusAssign
:
	'-='
;

StarAssign
:
	'*='
;

DivAssign
:
	'/='
;

ModAssign
:
	'%='
;

XorAssign
:
	'^='
;

AndAssign
:
	'&='
;

OrAssign
:
	'|='
;

LeftShift
:
	'<<'
;

rightShift
:
//'>>'
	Greater Greater
;

LeftShiftAssign
:
	'<<='
;

rightShiftAssign
:
//'>>='
	Greater Greater Assign
;

Equal
:
	'=='
;

NotEqual
:
	'!='
;

LessEqual
:
	'<='
;

GreaterEqual
:
	'>='
;

AndAnd
:
	'&&'
;

OrOr
:
	'||'
;

PlusPlus
:
	'++'
;

MinusMinus
:
	'--'
;

Comma
:
	','
;

ArrowStar
:
	'->*'
;

Arrow
:
	'->'
;

Question
:
	'?'
;

Colon
:
	':'
;

Doublecolon
:
	'::'
;

Semi
:
	';'
;

Dot
:
	'.'
;

DotStar
:
	'.*'
;

Ellipsis
:
	'...'
;

theoperator
:
	New
	| Delete
	| New '[' ']'
	| Delete '[' ']'
	| '+'
	| '-'
	| '*'
	| '/'
	| '%'
	| '^'
	| '&'
	| '|'
	| '~'
	| '!'
	| '='
	| '<'
	| '>'
	| '+='
	| '-='
	| '*='
	| '/='
	| '%='
	| '^='
	| '&='
	| '|='
	| '<<'
	| rightShift
	| rightShiftAssign
	| '<<='
	| '=='
	| '!='
	| '<='
	| '>='
	| '&&'
	| '||'
	| '++'
	| '--'
	| ','
	| '->*'
	| '->'
	| '(' ')'
	| '[' ']'
;

/*Lexer*/
fragment
Hexquad
:
	HEXADECIMALDIGIT HEXADECIMALDIGIT HEXADECIMALDIGIT HEXADECIMALDIGIT
;

fragment
Universalcharactername
:
	'\\u' Hexquad
	| '\\U' Hexquad Hexquad
;

Identifier
:
/*
	Identifiernondigit
	| Identifier Identifiernondigit
	| Identifier DIGIT
	*/
	Identifiernondigit
	(
		Identifiernondigit
		| DIGIT
	)*
;

fragment
Identifiernondigit
:
	NONDIGIT
	| Universalcharactername
	/* other implementation defined characters*/
;

fragment
NONDIGIT
:
	[a-zA-Z_]
;

fragment
DIGIT
:
	[0-9]
;

literal
:
	Integerliteral
	| Characterliteral
	| Floatingliteral
	| Stringliteral
	| booleanliteral
	| pointerliteral
	| userdefinedliteral
;

Integerliteral
:
	Decimalliteral Integersuffix?
	| Octalliteral Integersuffix?
	| Hexadecimalliteral Integersuffix?
	| Binaryliteral Integersuffix?
;

Decimalliteral
:
	NONZERODIGIT
	(
		'\''? DIGIT
	)*
;

Octalliteral
:
	'0'
	(
		'\''? OCTALDIGIT
	)*
;

Hexadecimalliteral
:
	(
		'0x'
		| '0X'
	) HEXADECIMALDIGIT
	(
		'\''? HEXADECIMALDIGIT
	)*
;

Binaryliteral
:
	(
		'0b'
		| '0B'
	) BINARYDIGIT
	(
		'\''? BINARYDIGIT
	)*
;

fragment
NONZERODIGIT
:
	[1-9]
;

fragment
OCTALDIGIT
:
	[0-7]
;

fragment
HEXADECIMALDIGIT
:
	[0-9a-fA-F]
;

fragment
BINARYDIGIT
:
	[01]
;

Integersuffix
:
	Unsignedsuffix Longsuffix?
	| Unsignedsuffix Longlongsuffix?
	| Longsuffix Unsignedsuffix?
	| Longlongsuffix Unsignedsuffix?
;

fragment
Unsignedsuffix
:
	[uU]
;

fragment
Longsuffix
:
	[lL]
;

fragment
Longlongsuffix
:
	'll'
	| 'LL'
;

Characterliteral
:
	'\'' Cchar+ '\''
	| 'u' '\'' Cchar+ '\''
	| 'U' '\'' Cchar+ '\''
	| 'L' '\'' Cchar+ '\''
;

fragment
Cchar
:
	~['\\\r\n]
	| Escapesequence
	| Universalcharactername
;

fragment
Escapesequence
:
	Simpleescapesequence
	| Octalescapesequence
	| Hexadecimalescapesequence
;

fragment
Simpleescapesequence
:
	'\\\''
	| '\\"'
	| '\\?'
	| '\\\\'
	| '\\a'
	| '\\b'
	| '\\f'
	| '\\n'
	| '\\r'
	| '\\t'
	| '\\v'
;

fragment
Octalescapesequence
:
	'\\' OCTALDIGIT
	| '\\' OCTALDIGIT OCTALDIGIT
	| '\\' OCTALDIGIT OCTALDIGIT OCTALDIGIT
;

fragment
Hexadecimalescapesequence
:
	'\\x' HEXADECIMALDIGIT+
;

Floatingliteral
:
	Fractionalconstant Exponentpart? Floatingsuffix?
	| Digitsequence Exponentpart Floatingsuffix?
;

fragment
Fractionalconstant
:
	Digitsequence? '.' Digitsequence
	| Digitsequence '.'
;

fragment
Exponentpart
:
	'e' SIGN? Digitsequence
	| 'E' SIGN? Digitsequence
;

fragment
SIGN
:
	[+-]
;

fragment
Digitsequence
:
	DIGIT
	(
		'\''? DIGIT
	)*
;

fragment
Floatingsuffix
:
	[flFL]
;

Stringliteral
:
	Encodingprefix? '"' Schar* '"'
	| Encodingprefix? 'R' Rawstring
;

fragment
Encodingprefix
:
	'u8'
	| 'u'
	| 'U'
	| 'L'
;

fragment
Schar
:
	~["\\\r\n]
	| Escapesequence
	| Universalcharactername
;

fragment
Rawstring /* '"' dcharsequence? '(' rcharsequence? ')' dcharsequence? '"' */
:
	'"' .*? '(' .*? ')' .*? '"'
;

booleanliteral
:
	FalseToken
	| TrueToken
;

pointerliteral
:
	Nullptr
;

userdefinedliteral
:
	Userdefinedintegerliteral
	| Userdefinedfloatingliteral
	| Userdefinedstringliteral
	| Userdefinedcharacterliteral
;

Userdefinedintegerliteral
:
	Decimalliteral Udsuffix
	| Octalliteral Udsuffix
	| Hexadecimalliteral Udsuffix
	| Binaryliteral Udsuffix
;

Userdefinedfloatingliteral
:
	Fractionalconstant Exponentpart? Udsuffix
	| Digitsequence Exponentpart Udsuffix
;

Userdefinedstringliteral
:
	Stringliteral Udsuffix
;

Userdefinedcharacterliteral
:
	Characterliteral Udsuffix
;

fragment
Udsuffix
:
	Identifier
;

Whitespace
:
	[ \t]+ -> skip
;

Newline
:
	(
		'\r' '\n'?
		| '\n'
	) -> skip
;

BlockComment
:
	'/*' .*? '*/' -> skip
;

LineComment
:
	'//' ~[\r\n]* -> skip
;