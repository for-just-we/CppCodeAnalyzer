# from ast.ASTNode import ASTNode


class ASTNodeVisitor(object):
    def visitChildren(self, item):
        nChildren: int = item.getChildCount()
        for i in range(nChildren):
            child = item.getChild(i)
            child.accept(self)

    def visit(self, item):
        self.visitChildren(item)