import ast
import astor


target_path = "./source.py"
source = open(target_path).read()
tree = ast.parse(source, target_path)

# Replace the first Comparator in the program
# To simplify this example, we will replace any compare operator with
# ">="


visit_target = 2
visit_count = 0

class RewriteCompare(ast.NodeTransformer):
    def visit_Compare(self, node):
        global visit_count, visit_target
        self.generic_visit(node)
        visit_count = visit_count + 1
        #print(visit_count)
        if (visit_count == visit_target):
            #print("Hi")
            newnode = ast.Compare(left=node.left, ops=[ast.Lt()], comparators=node.comparators)
            return newnode
        else:
            return node

tree = RewriteCompare().visit(tree)
print(astor.to_source(tree))
