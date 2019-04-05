import random, sys
import copy 
import ast 
from ast import * 
import astor

# Replace Cmp to Not Cmp 
# Replace + -, * with / 
# Delete Statement (replace with Expr 0) 

compare_count = 0 
binop_count = 0 
stmt_count = 0 

class CountCompare(ast.NodeVisitor):
        def visit_Compare(self, node):
                global compare_count 
                self.generic_visit(node) 
                # print "compare ", compare_count, " = ", astor.to_source(node) 
                compare_count = compare_count + 1 
                return 

class CountBinOp(ast.NodeVisitor): 
        def visit_BinOp(self, node):
                global binop_count 
                self.generic_visit(node) 
                sym = node.op.__class__.__name__
                if sym in ["Add","Sub","FloorDiv","Mult"]: 
                        # print "binop ", binop_count, " = ", astor.to_source(node) 
                        binop_count = binop_count + 1 
                return 

class CountStatement(ast.NodeVisitor):
        def visit_Set(self, node):
                global stmt_count 
                self.generic_visit(node) 
                stmt_count = stmt_count + 1 
                return 
        def visit_Call(self, node):
                global stmt_count 
                self.generic_visit(node) 
                stmt_count = stmt_count + 1 
                return 

visit_count = 0
visit_target = 0 

class RewriteCompare(ast.NodeTransformer):
        def visit_Compare(self, node): 
                global visit_count, visit_target
                self.generic_visit(node)
                visit_count = visit_count + 1
                if (visit_count == visit_target):
                        newnode = UnaryOp(Not(), node) 
                        return newnode
                else: 
                        return node 

class RewriteBinOp(ast.NodeTransformer): 
        def visit_BinOp(self, node):
                global visit_count, visit_target
                self.generic_visit(node) 
                sym = node.op.__class__.__name__
                if sym in ["Add","Sub","FloorDiv","Mult"]: 
                        # print "binop ", binop_count, " = ", astor.to_source(node) 
                        visit_count = visit_count + 1 
                        if (visit_count == visit_target):
                                if sym == "Add":
                                        node.op = Sub() 
                                elif sym == "Sub":
                                        node.op = Add()
                                elif sym == "Mult":
                                        node.op = FloorDiv()
                                elif sym == "FloorDiv":
                                        node.op = Mult() 
                                return node 
                        else:
                                return node 
                return node 

class RewriteStatement(ast.NodeTransformer):
        def visit_Set(self, node):
                global visit_count, visit_target
                self.generic_visit(node) 
                visit_count = visit_count + 1 
                if (visit_count == visit_target):
                        return Expr(Num(1))  
                else: 
                        return node 
        def visit_Call(self, node):
                global visit_count, visit_target
                self.generic_visit(node) 
                visit_count = visit_count + 1 
                if (visit_count == visit_target):
                        return Expr(Num(1))  
                else: 
                        return node 

random.seed(0) 
filename = sys.argv[1]
count = int(sys.argv[2]) 
with open(filename, "r") as myfile: 
        contents = myfile.read() 
        original_ast = ast.parse(contents) 
        CountCompare().visit(original_ast) 
        # print "# compares = ", compare_count
        CountBinOp().visit(original_ast) 
        compare_order = range(compare_count)
        compare_order = random.sample(compare_order, k=len(compare_order))
        # random.shuffle(compare_order)
        # print "# binops = ", binop_count
        binop_order = range(binop_count)
        binop_order = random.sample(binop_order, k=len(binop_order))
        # random.shuffle(binop_order) 
        CountStatement().visit(original_ast) 
        # print "# stmts = ", stmt_count
        stmt_order = range(stmt_count)
        stmt_order = random.sample(stmt_order, k=len(stmt_order))
        ops = [ ("c",i) for i in compare_order ] + \
              [ ("b",i) for i in binop_order ] + \
              [ ("s",i) for i in stmt_order ] 
        ops = random.sample(ops, k=len(ops)) 
        # print(ops)
        # random.shuffle(stmt_order) 
        for i in range(count):
                ast = copy.deepcopy(original_ast)
                outname = str(i) + ".py" 
                print(outname, end=': ')

                while True: 
                        visit_count = 0 
                        (cmd, i) = ops[0]
                        print (ops[0], end='')
                        visit_target = i 
                        ops = ops[1:]
                        if cmd == "c":
                                ast = RewriteCompare().visit(ast) 
                        elif cmd == "b":
                                ast = RewriteBinOp().visit(ast) 
                        elif cmd == "s":
                                ast = RewriteStatement().visit(ast) 
                        if bool(random.getrandbits(1)):
                                break 

                print(".") 

                with open(outname, "w") as outfile:
                        source = astor.to_source(ast) 
                        outfile.write(source) 
