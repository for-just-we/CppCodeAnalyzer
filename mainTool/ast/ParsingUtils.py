from antlr4.ParserRuleContext import ParserRuleContext

# from ast.expressions.expressionHolders import

def childTokenString(ctx: ParserRuleContext) -> str:
    if ctx is None:
        return ""
    nChildren: int = ctx.getChildCount()

    if nChildren == 0:
        return ctx.getText()

    retval: str = ""

    for i in range(nChildren):
        child: ParserRuleContext = ctx.getChild(i)
        childText: str = childTokenString(child)

        if childText != "":
            retval = retval + childText + " "

    return retval.strip()