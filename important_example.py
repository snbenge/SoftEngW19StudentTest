import ast
import astor
import astpretty
import sys


# parse the target program to ast
target_path = "./source.py"
source = open(target_path).read()
tree = ast.parse(source, target_path)

class MyTransformer(ast.NodeTransformer):
    # Magic here:
    # you should know when you need generic_visit(), how visit() works?
    # How visit_calssname() works? How do they work together?
    def visit_If(self, node):
        self.generic_visit(node)
        return node

    def visit_Compare(self, node):
        if isinstance(node.ops[0], ast.GtE):
            print ("GtE")
            newnode = ast.Compare(left=node.left, ops=[ast.Lt()], comparators=node.comparators)
            print(newnode.left)
            return newnode



tree = MyTransformer().visit(tree)

print (astor.to_source(tree))

