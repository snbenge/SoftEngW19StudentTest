import ast
import astor


target_path = "./source.py"
source = open(target_path).read()
tree = ast.parse(source, target_path)



visit_target = 1
visit_count = 0

class DeleteCall(ast.NodeTransformer):
    def visit_Call(self, node):
        global visit_count, visit_target
        self.generic_visit(node)
        visit_count = visit_count + 1
        #print(visit_count)
        if (visit_count == visit_target):
            #print("Hi")
            # THINK: do you always want to return a pass()? What if the
            # function call is in an assignment?
            return ast.Pass()
        return node

tree = DeleteCall().visit(tree)
print(astor.to_source(tree))
