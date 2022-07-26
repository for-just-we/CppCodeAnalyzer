from extraTools.vuldetect.utils.environments import *
from mainTool.CPG import *
from typing import List, Set, Tuple



# symbolized variable names and function names
# however, here we don't actually symbolize them,
# we only collect the var name and func name to be symbolized
# and their corresponding symbolized name

symbolic_var_prefix = "VAR"
symbolic_func_prefix = "FUN"


class ASTVarAnalyzer(object):
    def __init__(self):
        self.environmentStack: List[VariableEnvironment] = list()
        self.variables: Set[str] = None
        self.var2type: Dict[str, str] = dict()
        self.funcNames: Set[str] = set()

    def reset(self):
        self.environmentStack.clear()
        self.variables = set()
        self.funcNames = set()
        # self.var2type = dict()

    def analyzeAST(self, astProvider: ASTProvider):
        self.reset()
        self.traverseAST(astProvider)


    def traverseAST(self, astProvider: ASTProvider):
        env: VariableEnvironment = self.createVarEnvironment(astProvider)
        self.traverseASTChildren(astProvider, env)


    def traverseASTChildren(self, astProvider: ASTProvider, env: VariableEnvironment):
        numChildren: int = astProvider.getChildCount()
        self.environmentStack.append(env)
        for i in range(numChildren):
            childProvider: ASTProvider = astProvider.getChild(i)
            self.traverseAST(childProvider)
        self.environmentStack.pop()
        self.variables.update(env.selfHandledSymbols())
        self.reportUpstream(env)
        self.var2type.update(env.var2type)
        self.funcNames.update(env.funcNames)


    def reportUpstream(self, env: VariableEnvironment):
        symbols: Set[str] = env.upstreamSymbols()
        astProvider: ASTProvider = env.astProvider
        if len(self.environmentStack) > 0:
            parentEnv: VariableEnvironment = self.environmentStack[-1]
            parentEnv.addChildSymbols(symbols, astProvider)



    def createVarEnvironment(self, astProvider: ASTProvider) -> VariableEnvironment:
        nodeType: str = astProvider.getTypeAsString()

        if nodeType == "IdentifierDecl" or nodeType == "Parameter":
            return VarDeclEnvironment(astProvider)
        elif nodeType == "CallExpression":
            return CallVarEnvironment(astProvider)
        elif nodeType == "ClassStaticIdentifier":
            return ClassStaticIdentifierVarEnvironment(astProvider)
        elif nodeType == "Identifier":
            return IdentifierVarEnvironment(astProvider)
        elif nodeType == "MemberAccess" or nodeType == "PtrMemberAccess":
            return MemberAccessVarEnvironment(astProvider)
        elif nodeType == "Callee":
            return CalleeEnvironment(astProvider)
        else:
            return VariableEnvironment(astProvider)


def getVarFuncNamesInFunc(statements: List[ASTNode]) -> Tuple[Set[str], Set[str]]:
    astVarAnalyzer: ASTVarAnalyzer = ASTVarAnalyzer()
    varSets: Set[str] = set()
    funcSets: Set[str] = set()
    for statement in statements:
        provider: ASTNodeASTProvider = ASTNodeASTProvider()
        provider.node = statement
        astVarAnalyzer.analyzeAST(provider)
        varSets.update(astVarAnalyzer.variables)
        funcSets.update(astVarAnalyzer.funcNames)

    return varSets, funcSets


class SymbolizingTool(object):
    def __init__(self, systemDefinedVars: Set[str], systemDefinedFuncs: Set[str]):
        self.systemDefinedVars: Set[str] = systemDefinedVars
        self.systemDefinedFuncs: Set[str] = systemDefinedFuncs
        self.var2symbol: Dict[str, str] = dict()
        self.func2symbol: Dict[str, str] = dict()

    # cpgs is all cpgs from functions of a program
    def getVarFuncNamesInFile(self, cpgs: List[CPG]):
        for cpg in cpgs:
            if cpg.name not in self.systemDefinedFuncs and cpg.name not in self.func2symbol.keys():
                self.func2symbol[cpg.name] = symbolic_func_prefix + str(len(self.func2symbol) + 1)
            varSets, funcSets = getVarFuncNamesInFunc(cpg.statements)
            for var in varSets:
                if var not in self.var2symbol.keys() and var not in self.systemDefinedVars:
                    self.var2symbol[var] = symbolic_var_prefix + str(len(self.var2symbol) + 1)
            for func in funcSets:
                if func not in self.systemDefinedFuncs and func not in self.func2symbol.keys():
                    self.func2symbol[func] = symbolic_func_prefix + str(len(self.func2symbol) + 1)



    def symbolize(self, code: str) -> str:
        tokens = code.split(' ')
        symbolized_tokens = []
        for token in tokens:
            symVarName: str = self.var2symbol.get(token, None)
            symFuncName: str = self.func2symbol.get(token, None)
            if symVarName is not None:
                symbolized_tokens.append(symVarName)
            elif symFuncName is not None:
                symbolized_tokens.append(symFuncName)
            else:
                symbolized_tokens.append(token)
        return " ".join(symbolized_tokens)