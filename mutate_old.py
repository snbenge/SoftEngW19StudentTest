import ast
import astor
import codegen
import astpretty
import sys

import pprint

# takes two arguments: source_program, number_of_mutants
#target_path = sys.argv[1]
#num_of_mutants = sys.argv[2]

# parse the target program to ast
target_path = "./source.py"
source = open(target_path).read()
tree = ast.parse(source, target_path)

class MyVisitor(ast.NodeVisitor):
    def visit_Str(self, node):
        print ('Found Str: "%s"' % node.s)

    def visit_Compare(self, node):
        print('Found CompOp: "%s"' % node.ops)

    def visit_BinOp(self, node):
        print('Found BinOp: "%s"' % node.op)

    def visit_Expr(self, node):
        print('Found Expr: "%s"' % node.value)

class MyTransformer(ast.NodeTransformer):
    def visit_IfExp(self, node):
        return node
    def visit_If(self, node):
        self.generic_visit(node)
        return node
    def visit_Compare(self, node):
        if isinstance(node.ops[0], ast.GtE):
            print ("GtE")
            newnode = ast.Compare(left=node.left, ops=[ast.Lt()], comparators=node.comparators)
            print(newnode.left)
            return newnode
        if isinstance(node.ops[0], ast.Lt):
            newnode = ast.Compare(left=node.left, ops=[ast.GtE()], comparators=node.comparators)
            return newnode

#    def visit_BinOp(self, node):
 #       if isinstance(node.op, ast.Sub):
  #          print("Sub")
   #         print(node)
    #        newnode = ast.BinOp(left=node.left, op=ast.Add(), right=node.right)
     #       print("HERE!")
      #      return newnode


    def visit_Str(self,node):
        return ast.Str("NEW"+node.s)

MyVisitor().visit(tree)
#tree = ast.fix_missing_locations(tree)

#ast.fix_missing_locations(tree)


astpretty.pprint(tree)

tree = MyTransformer().visit(tree)


#print(ast.dump(tree))
#ast.fix_missing_locations(tree)
print (astor.to_source(tree))
#astpretty.pprint(tree)
# Comparison operator negation operator(CON)
# >= : <
# <= : >
# > : <=
# < : >=
# == : !=
# != : ==

"""
class CON_operator():
    def CON_get(self, node):
        return ast.Lt()
        
    def CON_gt():
        
    def CON_let():
        
    def CON_lt():
        
    def CON_eq():
        
    def CON_neq():
"""
