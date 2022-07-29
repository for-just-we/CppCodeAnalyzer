from extraTools.vuldetect.utils.symbolized import ASTVarAnalyzer
from mainTool.CPG import *
import re

# supproting IVDetect to extract variables and their types
# paper: Vulnerability Detection with Fine-Grained Interpretations

# In mainTool, CppCodeAnalyzer is able to produce AST, CDG and DDG, so there is no need here
# to write script to

# parsing the contents in a AST node into its sub token sequence, generating feature 1
# code in https://github.com/vulnerabilitydetection/VulnerabilityDetectionResearch/blob/new_implementation/IVDetect/utils/process.py#L138 could
# produce errors when parsing identifiers like TASK_SIZE_MAX with all upper case
def lexical_parse(line: str) -> List[str]:
    tokens = line.split(" ")
    filtered_set = ['', ' ', '	', ',', '\n', ';', '(', ')', '<', '>', '{', '}', '[', ']', '``', '\'\'', '\"', "'"]

    tokens = list(filter(lambda t: t not in filtered_set, tokens))
    new_tokens = list()
    for token in tokens:
        # 按下划线分割
        if '_' in token:
            new_tokens.extend([t for t in token.split('_') if t != ''])
        # 按大小写分割
        else:
            new_tokens.extend(re.findall('[a-zA-Z][^A-Z]*', token))
    return new_tokens


# 返回每个statement对应的astnode及其type token序列
def generate_feature3(statements: List[ASTNode]):
    astVarAnalyzer: ASTVarAnalyzer = ASTVarAnalyzer()
    varLists: List[list] = list()
    for statement in statements:
        provider: ASTNodeASTProvider = ASTNodeASTProvider()
        provider.node = statement
        astVarAnalyzer.analyzeAST(provider)

        vars = list()
        for variable in astVarAnalyzer.variables:
            vars.extend(lexical_parse(variable))
            if variable in astVarAnalyzer.var2type.keys():
                vars.extend(lexical_parse(astVarAnalyzer.var2type[variable]))
        varLists.append(vars)

    return varLists


# 返回和该statement有控制依赖的结点组成的token sequence，为了不让深度太大，我们暂时限制depth = 1
def find_control(cur_stmt_idx: int, cdg_edge_idxs: Dict[int, int], seq: List[int], depth: int, limit: int):
    record = []
    if cur_stmt_idx in cdg_edge_idxs.keys():
        control_stmt = cdg_edge_idxs[cur_stmt_idx]
        seq.append(control_stmt)
        record.append(control_stmt)
    if depth < limit:
        for stmt in record:
            find_control(stmt, cdg_edge_idxs, seq, depth + 1, limit)


def generate_feature4(cpg: CPG, limit: int = 1) -> List[List[List[str]]]:
    cdg_edge_idxs: Dict[int, int] = { edge.destination: edge.source for edge in cpg.CDGEdges }
    #  每个statement的控制依赖结点
    cd_idxs_for_stmt: List[List[int]] = list()
    for stmt_idx in range(len(cpg.statements)):
        seq: List[int] = list()
        find_control(stmt_idx, cdg_edge_idxs, seq, 1, limit)
        cd_idxs_for_stmt.append(seq)

    feature4_for_stmts: List[List[List[str]]] = list()
    for cd_idxs in cd_idxs_for_stmt:
        sub_tokens_in_stmts: List[List[str]] = [lexical_parse(cpg.statements[idx].getEscapedCodeStr())
                                                for idx in cd_idxs]
        feature4_for_stmts.append(sub_tokens_in_stmts)

    return feature4_for_stmts


def find_data(cur_stmt_idx: int, ddg_edge_idxs: Dict[int, Set[int]], seq: List[int], depth: int, limit: int):
    record = []
    if cur_stmt_idx in ddg_edge_idxs.keys():
        for data_stmt in ddg_edge_idxs[cur_stmt_idx]:
            seq.append(data_stmt)
            record.append(data_stmt)
    if depth < limit:
        for stmt in record:
            find_data(stmt, ddg_edge_idxs, seq, depth + 1, limit)


# feature5, data dependence
def generate_feature5(cpg: CPG, limit: int = 1) -> List[List[List[str]]]:
    ddg_edge_idxs: Dict[int, Set[int]] = dict()
    for edge in cpg.DDGEdges:
        if edge.destination not in ddg_edge_idxs.keys():
            ddg_edge_idxs[edge.destination] = {edge.source}
        else:
            ddg_edge_idxs[edge.destination].add(edge.source)
    #  每个statement的控制依赖结点
    dd_idxs_for_stmt: List[List[int]] = list()
    for stmt_idx in range(len(cpg.statements)):
        seq: List[int] = list()
        find_data(stmt_idx, ddg_edge_idxs, seq, 1, limit)
        dd_idxs_for_stmt.append(seq)

    feature5_for_stmts: List[List[List[str]]] = list()
    for dd_idxs in dd_idxs_for_stmt:
        sub_tokens_in_stmts: List[List[str]] = [lexical_parse(cpg.statements[idx].getEscapedCodeStr())
                                                for idx in dd_idxs]
        feature5_for_stmts.append(sub_tokens_in_stmts)

    return feature5_for_stmts