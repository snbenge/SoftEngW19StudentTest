import ast
import astor
import codegen
import astpretty
import sys

import pprint

# parse the target program to ast
target_path = "./ast2.py"
source = open(target_path).read()
tree = ast.parse(source, target_path)



astpretty.pprint(tree)


#print(ast.dump(tree))
print (astor.to_source(tree))
#astpretty.pprint(tree)
#pprint.pprint(ast.dump(tree))
