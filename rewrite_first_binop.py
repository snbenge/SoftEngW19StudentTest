import ast
import astor


target_path = "./source.py"
source = open(target_path).read()
tree = ast.parse(source, target_path)



visit_target = 1
visit_count = 0

class RewriteBinOp(ast.NodeTransformer):
    def visit_BinOp(self, node):
        global visit_count, visit_target
        self.generic_visit(node)
        visit_count = visit_count + 1
        #print(visit_count)
        if (visit_count == visit_target):
            #print("Hi")
            node.op = ast.FloorDiv()
        return node

tree = RewriteBinOp().visit(tree)
print(astor.to_source(tree))
