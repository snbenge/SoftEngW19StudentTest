#!/usr/bin/python3

import ast
import astor
import random
import sys

MUT_MAX = 5


def mutate():
    # read in command line arguments
    if len(sys.argv) != 3:
        print ("Invalid number of command line arguments.")
        return
    src_pgm_name = str(sys.argv[1])
    src_pgm = open(src_pgm_name).read()
    num_mutants = int(sys.argv[2])

    this_num_mutations = 0

    # seed random func for pseudo-randomness
    random.seed(0)

    # for creating FOM mutants
    comparators = [ast.Eq, ast.Lt, ast.LtE, ast.Gt, ast.GtE, ast.Is, ast.IsNot, ast.In]
    bin_ops     = [ast.Add, ast.Sub, ast.Mult, ast.Div]

    # for creating HOM mutants
    mutations   = [ast.Compare, ast.Call, ast.FunctionDef, ast.ExceptHandler, ast.BinOp, ast.List, ast.Attribute, ast.BoolOp, ast.NameConstant, ast.For, ast.If, ast.Assign, ast.Compare, ast.Num, ast.Lambda, ast.Call]
    # removed mutations: ast.While, ast.UnaryOp, ast.Dict, ast.Import, ast.Tuple, ast.Try

    c = 0
    if num_mutants >= len(comparators):
        # create FOM comparator mutants
        for c in range(len(comparators)):
            tree = ast.parse(src_pgm, src_pgm_name)     # parse source program

            # go through every node and modify the same type of comparator only
            for node in ast.walk(tree):
                if this_num_mutations > MUT_MAX:
                    break
                if isinstance(node, ast.Compare) and isinstance(node.ops[0], comparators[c]):
                    this_num_mutations += 1
                    print("   CHANGING instance of", comparators[c])
                    print("old node is ", node)
                    # print("old node op ", node.ops[0])
                    node = MyTransformer().visit(node)
                    print("new node is ", node)
                    # print("new node op ", node.ops[0])
                    
            # save mutation to the next file
            print("gonna make file:", str(c) + ".py")
            curr_mutant_file = open(str(c) + ".py", "w")
            curr_mutant_file.write(str(astor.to_source(tree)))
            curr_mutant_file.close()
            print("  num mutations for this file =", this_num_mutations)
            this_num_mutations = 0

    # ensure that first iteration of for loop doesn't overwrite last .py file we just made
    if c == (len(comparators) - 1): c += 1
    b = c

    # create BinOp FOM mutants
    if num_mutants >= (len(comparators) + len(bin_ops)):
        # create 10 FOM binary operator mutants
        for b in range(c, c + len(bin_ops)):
            tree = ast.parse(src_pgm, src_pgm_name)     # parse source program
            
            # go through every node and modify the same type of comparator only
            print("checking for instances of", bin_ops[b % len(bin_ops)])
            for node in ast.walk(tree):
                if this_num_mutations > MUT_MAX:
                    break
                if isinstance(node, ast.BinOp) and isinstance(node.op, bin_ops[b % len(bin_ops)]):
                    this_num_mutations += 1
                    print("   CHANGING instance of", bin_ops[b % len(bin_ops)])
                    print("old node is ", node)
                    # print("old node op ", node.op)
                    node = MyTransformer().visit(node)
                    print("new node is ", node)
                    # print("new node op ", node.op)
                    
            # save mutation to the next file
            print("gonna make file:", str(b) + ".py")
            curr_mutant_file = open(str(b) + ".py", "w")
            curr_mutant_file.write(str(astor.to_source(tree)))
            curr_mutant_file.close()
            print("  num mutations for this file =", this_num_mutations)
            this_num_mutations = 0

    # ensure that first iteration of for loop doesn't overwrite last .py file we just made
    print("b =", b)
    if b == (len(comparators) + len(bin_ops) - 1): b += 1

    # create AND binary FOM
    tree = ast.parse(src_pgm, src_pgm_name)
    for node in ast.walk(tree):
        if this_num_mutations > MUT_MAX:
            break
        if isinstance(node, ast.BoolOp) and isinstance(node.op, ast.And) and (random.randint(1, 3) >= 2):
            this_num_mutations += 1
            node = MyTransformer().visit(node)
    # save mutation to the next file
    print("gonna make file:", str(b) + ".py")
    curr_mutant_file = open(str(b) + ".py", "w")
    curr_mutant_file.write(str(astor.to_source(tree)))
    curr_mutant_file.close()
    print("  num mutations for this file =", this_num_mutations)
    this_num_mutations = 0
    b += 1

    # create OR binary FOM
    tree = ast.parse(src_pgm, src_pgm_name)
    for node in ast.walk(tree):
        if this_num_mutations > MUT_MAX:
            break
        if isinstance(node, ast.BoolOp) and isinstance(node.op, ast.Or) and (random.randint(1, 3) >= 2):
            this_num_mutations += 1
            node = MyTransformer().visit(node)
    # save mutation to the next file
    print("gonna make file:", str(b) + ".py")
    curr_mutant_file = open(str(b) + ".py", "w")
    curr_mutant_file.write(str(astor.to_source(tree)))
    curr_mutant_file.close()
    print("  num mutations for this file =", this_num_mutations)
    this_num_mutations = 0
    b += 1

    # create Attribute FOM
    tree = ast.parse(src_pgm, src_pgm_name)
    for node in ast.walk(tree):
        if this_num_mutations > MUT_MAX:
            break
        if isinstance(node, ast.Attribute):
            this_num_mutations += 1
            node = MyTransformer().visit(node)

    # save mutation to the next file
    print("gonna make file:", str(b) + ".py")
    curr_mutant_file = open(str(b) + ".py", "w")
    curr_mutant_file.write(str(astor.to_source(tree)))
    curr_mutant_file.close()
    print("  num mutations for this file =", this_num_mutations)
    this_num_mutations = 0
    b += 1

    # create some HOM mutants with the rest 
    print("pre HOM loop, b=", b)
    i = b
    while i < (num_mutants - 10):
        tree = ast.parse(src_pgm, src_pgm_name)     # parse source program

        # negate 25% of the operators of this type
        print("checking for instances of", mutations[i % len(mutations)])  
        for node in ast.walk(tree): 
            if this_num_mutations > MUT_MAX:
                break                              
            if isinstance(node, mutations[i % len(mutations)]) and (random.randint(1, 4) >= 3):
                this_num_mutations += 1
                node = MyTransformer().visit(node)

        # only make python file if it compiles
        if this_num_mutations > 0 and create_py_file(i, tree):
            print("python file created successfully")
            print("  num mutations for this file =", this_num_mutations)
            this_num_mutations = 0
            i += 1
            b = i
        else: 
            # reset num_mutations for next while iteration
            this_num_mutations = 0

    # create more random HOMs
    print("creating super random HOMs")
    i = b
    while i < num_mutants:
        tree = ast.parse(src_pgm, src_pgm_name)     # parse source program
 
        for node in ast.walk(tree):
            if this_num_mutations > MUT_MAX:
                break                          
            if (random.randint(1, 10) >= 8):
                this_num_mutations += 1
                node = MyTransformer().visit(node)

        # only make python file if it compiles
        if this_num_mutations > 0 and create_py_file(i, tree):
            print("python file created successfully")
            print("  num mutations for this file =", this_num_mutations)
            this_num_mutations = 0
            i += 1
        else: 
            # reset num_mutations for next while iteration
            this_num_mutations = 0

    return



def create_py_file(this_name, code):
    # see if it's legit python file first
    print("creating temp python file...(" + str(this_name) + ")")
    try:
        temp = compile(str(astor.to_source(code)), 'fakemodule', 'exec')
        print("attempting to execute...")
        # exec(temp)
    except:
        print("not a valid python file")
        return False

    # create actual mutant
    print("gonna make file:", str(this_name) + ".py")
    curr_mutant_file = open(str(this_name) + ".py", "w")
    curr_mutant_file.write(str(astor.to_source(code)))
    curr_mutant_file.close()
    return True


class MyTransformer(ast.NodeTransformer):
    # overload visit_ functions
    # ast will figure out which one to use based on the operator

    # default visit_ function -- will "visit" here if that method's visit_ DNE
    def generic_visit(self, node):
        print("  in MyTransformer.generic_visit() for", node)
        # super().generic_visit(node)


    def visit_Assign(self, node):
        print("  in MyTransformer.visit_Assign()")
        # print("   targets =", node.targets[0].id)
        # print("   value   =", node.value)

        # create new node | Assign(expr* targets, expr value)
        new_node = node

        # assign random new value to this variable
        rand_num = random.randint(0, 8)

        new_value_dict = {
            0:  ast.Num(0),
            1:  ast.Str("random \x00 string"),
            2:  ast.NameConstant(False),
            3:  ast.NameConstant(True),
            4:  ast.List(elts=[ast.Num(0), ast.Num(1), ast.Str("2"), ast.Num(3), ast.Num(999999)], 
                         ctx=ast.Load()),
            # print("how did this happen?")
            5:  ast.Call(func=ast.Name(id='print', ctx=ast.Load()),
                         args=[ast.Str("how did this happen?")],
                         keywords=[]),
            # infinity
            6:  ast.Call(func=ast.Name(id='float', ctx=ast.Load()),
                         args=[ast.Str("inf")],
                         keywords=[]),
            # -infinity
            7:  ast.Call(func=ast.Name(id='float', ctx=ast.Load()),
                         args=[ast.Str("-inf")],
                         keywords=[]),
            # random dictionary
            8:  ast.Dict(keys=[ast.Num(0), ast.Num(1), ast.Str("key3")],
                         values=[ast.Str("Zero"), ast.Str("One"), ast.Num(3)])
        }

        new_value = new_value_dict[rand_num]
        print("   new_value =", new_value)

        new_node.value = new_value
        ast.copy_location(new_node, node)
        ast.fix_missing_locations(new_node)
        return new_node


    def visit_Attribute(self, node):
        print("  in MyTransformer.visit_Attribute()")
        print("   node  =", node)
        print("   val   =", node.value)
        print("   attr  =", node.attr)

        # create new node | Attribute(expr value, identifier attr, expr_context ctx)
        new_node = node
        new_node.attr = ast.Name(id="values", ctx=ast.Load())
        ast.copy_location(new_node, node)
        ast.fix_missing_locations(new_node)
        return new_node


    def visit_BinOp(self, node):
        # operator = Add | Sub | Mult | MatMult | Div | Mod | Pow | LShift | RShift | BitOr | BitXor | BitAnd | FloorDiv
        print("  in MyTransformer.visit_BinOp()")
        print("   curr op =", node.op)

        bin_negate = node.op

        # use pseudorandomness to determine whether to negate or just mix up
        rand_num = random.randint(1, 10)

        # negate
        if rand_num >= 4:
            print("   negating...")
            if isinstance(node.op,   ast.Add):      bin_negate = ast.Sub()
            elif isinstance(node.op, ast.Sub):      bin_negate = ast.Add()

            elif isinstance(node.op, ast.Mult):     bin_negate = ast.Div()
            elif isinstance(node.op, ast.Div):      bin_negate = ast.FloorDiv()
            elif isinstance(node.op, ast.FloorDiv): bin_negate = ast.Div()

            elif isinstance(node.op, ast.LShift):   bin_negate = ast.RShift()
            elif isinstance(node.op, ast.RShift):   bin_negate = ast.LShift() 

            elif isinstance(node.op, ast.BitOr):    bin_negate = ast.BitAnd()
            elif isinstance(node.op, ast.BitAnd):   bin_negate = ast.BitXor()
            elif isinstance(node.op, ast.BitXor):   bin_negate = ast.BitOr()

            elif isinstance(node.op, ast.Pow):      bin_negate = ast.Mult()
            elif isinstance(node.op, ast.Mod):      bin_negate = ast.Div()
            elif isinstance(node.op, ast.MatMult):  bin_negate = ast.Mult()

            else: print("    did not find negation for", node.op)
        # mix up
        else: 
            print("   mixing up...")
            if isinstance(node.op,   ast.Add):      bin_negate = ast.Mult()
            elif isinstance(node.op, ast.Sub):      bin_negate = ast.Div()

            elif isinstance(node.op, ast.Mult):     bin_negate = ast.Pow()
            elif isinstance(node.op, ast.Div):      bin_negate = ast.FloorDiv()
            elif isinstance(node.op, ast.FloorDiv): bin_negate = ast.Div()

            elif isinstance(node.op, ast.BitOr):    bin_negate = ast.BitXor()
            elif isinstance(node.op, ast.BitAnd):   bin_negate = ast.BitOr()
            elif isinstance(node.op, ast.BitXor):   bin_negate = ast.BitOr()

            elif isinstance(node.op, ast.Pow):      bin_negate = ast.Mult()
            elif isinstance(node.op, ast.Mod):      bin_negate = ast.FloorDiv()

            else: print("    did not find negation for", node.op)

        print ("   bin_negate =", bin_negate)

        # create negated node | BinOp(expr left, operator op, expr right)
        new_node = node
        new_node.op = bin_negate
        ast.copy_location(new_node, node)
        ast.fix_missing_locations(new_node)
        return new_node


    def visit_BoolOp(self, node):
        # boolop = And | Or
        print("  in MyTransformer.visit_BoolOp()")
        print("   node        =", node)
        print("   op          =", node.op)

        curr_op = node.op
        bool_negate = node.op

        if isinstance(curr_op, ast.And):  bool_negate = ast.Or()
        elif isinstance(curr_op, ast.Or): bool_negate = ast.And()
        else: print("    did not find negation for", curr_op)

        print("   bool_negate =", bool_negate)

        # create negated node | BoolOp(boolop op, expr* values)
        new_node = node
        new_node.op = bool_negate
        ast.copy_location(new_node, node)
        ast.fix_missing_locations(new_node)
        return new_node


    def visit_Call(self, node):
        print("  in MyTransformer.visit_Call()")
        print("   node  =", node)
        print("   func  =", node.func)
        # print("   args  =", node.args)
        
        # create new node | Call(expr func, expr* args, keyword* keywords)
        new_node = node

        # only modify about half of the function calls
        if random.randint(1, 2) == 2: 
            return node

        if isinstance(node.func, ast.Call):
            print("   name =", node.func.func)
            if   node.func.value == "int":   new_node.func = ast.Name(id='hex',   ctx=ast.Load())
            elif node.func.value == "float": new_node.func = ast.Name(id='int',   ctx=ast.Load())

            elif node.func.value == "len":     new_node.func = ast.Name(id='max',   ctx=ast.Load())

            elif node.func.value == "str":     new_node.func = ast.Name(id='chr',   ctx=ast.Load())
            elif node.func.value == "chr":     new_node.func = ast.Name(id='str',   ctx=ast.Load())
            elif node.func.value == "unicode": new_node.func = ast.Name(id='ascii', ctx=ast.Load())

            else: print("doing nothing")

        if isinstance(node.func, ast.Name):
            print("   name =", node.func.id)
            if   node.func.id == "int":   new_node.func = ast.Name(id='hex',   ctx=ast.Load())
            elif node.func.id == "float": new_node.func = ast.Name(id='int',   ctx=ast.Load())

            elif node.func.id == "len":     new_node.func = ast.Name(id='max',   ctx=ast.Load())

            elif node.func.id == "str":     new_node.func = ast.Name(id='chr',   ctx=ast.Load())
            elif node.func.id == "chr":     new_node.func = ast.Name(id='str',   ctx=ast.Load())
            elif node.func.id == "unicode": new_node.func = ast.Name(id='ascii', ctx=ast.Load())

            elif node.func.id == "validate_string": new_node.func = ast.Name(id='bool', ctx=ast.Load())

            elif node.func.id == "token_sort_ratio":         new_node.func = ast.Name(id='partial_token_sort_ratio', ctx=ast.Load())
            elif node.func.id == "partial_token_sort_ratio": new_node.func = ast.Name(id='token_sort_ratio',         ctx=ast.Load())

            elif node.func.id == "token_set_ratio":         new_node.func = ast.Name(id='partial_token_set_ratio', ctx=ast.Load())
            elif node.func.id == "partial_token_set_ratio": new_node.func = ast.Name(id='token_set_ratio',         ctx=ast.Load())

            elif node.func.id == "ratio":         new_node.func = ast.Name(id='partial_ratio', ctx=ast.Load())
            elif node.func.id == "partial_ratio": new_node.func = ast.Name(id='ratio',         ctx=ast.Load())

            elif node.func.id == "Qratio": new_node.func = ast.Name(id='Wratio', ctx=ast.Load())
            elif node.func.id == "Wratio": new_node.func = ast.Name(id='Qratio', ctx=ast.Load())

            elif node.func.id == "asciidammit": new_node.func = ast.Name(id='asciionly', ctx=ast.Load())
            elif node.func.id == "asciionly":   new_node.func = ast.Name(id='unicode',   ctx=ast.Load())

            elif node.func.id == "make_type_consistent":
                new_node.func = ast.Name(id='ascii', ctx=ast.Load())
                new_node.args.pop()

            else: print("doing nothing")

        ast.copy_location(new_node, node)
        ast.fix_missing_locations(new_node)
        return new_node


    def visit_Compare(self, node):
        # cmpop = Eq | NotEq | Lt | LtE | Gt | GtE | Is | IsNot | In | NotIn
        print("  in MyTransformer.visit_Compare()")
        print("   node     =", node)
        print("   op       =", node.ops[0])

        curr_op = node.ops[0]
        comp_negate = curr_op

        rand_num = random.randint(1, 10)
        if rand_num >= 7:
            print("   negating...")
            if isinstance(curr_op, ast.Eq):      comp_negate = ast.NotEq()
            elif isinstance(curr_op, ast.NotEq): comp_negate = ast.Eq()

            elif isinstance(curr_op, ast.Lt):    comp_negate = ast.GtE()
            elif isinstance(curr_op, ast.LtE):   comp_negate = ast.Gt()

            elif isinstance(curr_op, ast.Gt):    comp_negate = ast.LtE()
            elif isinstance(curr_op, ast.GtE):   comp_negate = ast.Lt()

            elif isinstance(curr_op, ast.Is):    comp_negate = ast.IsNot()
            elif isinstance(curr_op, ast.IsNot): comp_negate = ast.Is()

            elif isinstance(curr_op, ast.In):    comp_negate = ast.NotIn()
            elif isinstance(curr_op, ast.NotIn): comp_negate = ast.In()
            else: comp_negate = ast.Eq()
        else: 
            print("   mixing up...")
            if isinstance(curr_op, ast.Lt):      comp_negate = ast.LtE()
            elif isinstance(curr_op, ast.LtE):   comp_negate = ast.And()

            elif isinstance(curr_op, ast.Gt):    comp_negate = ast.Or()
            elif isinstance(curr_op, ast.GtE):   comp_negate = ast.Gt()

            elif isinstance(curr_op, ast.Is):    comp_negate = ast.Gt()
            elif isinstance(curr_op, ast.IsNot): comp_negate = ast.Lt()

            elif isinstance(curr_op, ast.In):    comp_negate = ast.In()     #leave the same for for loops (for x in this)
            elif isinstance(curr_op, ast.NotIn): comp_negate = ast.Lt()
            else: comp_negate = ast.Eq()

        print("   new comparator =", comp_negate)

        # create negated node | Compare(expr left, cmpop* ops, expr* comparators)
        new_node = node
        new_node.ops = [comp_negate]
        ast.copy_location(new_node, node)
        ast.fix_missing_locations(new_node)
        return new_node


    def visit_Dict(self, node):
        print("  in MyTransformer.visit_Dict()")
        print("   node     =", node)
        print("   keys     =", node.keys)
        print("   vals     =", node.values)

        # create new node | Dict(expr* keys, expr* values)
        new_node = node

        rand_num = random.randint(1, 10)
        if rand_num >= 5 and new_node.keys:
            # remove the last elt in dict
            print("   removing last dict elt")
            new_node.keys.pop()
            new_node.values.pop()
        else:
            # reverse key values
            print("   reversing key vals")
            new_node.keys.reverse()

        ast.copy_location(new_node, node)
        ast.fix_missing_locations(new_node)
        return new_node


    def visit_ExceptHandler(self, node):
        print("  in MyTransformer.visit_ExceptHandler()")
        print("   node     =", node)
        # print("   type     =", node.type.id)
        # print("   name     =", node.name)
        # print("   body     =", node.body)

        # create new node | ExceptHandler(expr? type, identifier? name, stmt* body)
        new_node = node

        new_body_dict = {
            1: [ast.Pass],
            2: [ast.Return(ast.Num(1))],
            3: [ast.Return(ast.Num(0))],
            4: [ast.Continue],
            5: [ast.Return(ast.NameConstant(True))],
            6: [ast.Return(ast.NameConstant(False))],
            7: [ast.Break]
        }

        # change how the except block handles the exception (by doing stupid stuff)
        new_node.body = new_body_dict[random.randint(1, (len(new_body_dict) - 1))]
        # print("   new body  =", new_node.body[0])
        ast.copy_location(new_node, node)
        ast.fix_missing_locations(new_node)
        return new_node


    def visit_For(self, node):
        print("  in MyTransformer.visit_For()")
        print("   node     =", node)
        # print("   target   =", node.target.id)
        # print("   iter     =", node.iter)
        # print("   body     =", node.body.value)

        # create negated node | For(expr target, expr iter, stmt* body, stmt* orelse)
        # replace iterator variable with "iterate_this"
        new_node = node
        new_node.target = ast.Name(id='iterate_this', ctx=ast.Load())
        ast.copy_location(new_node, node)
        ast.fix_missing_locations(new_node)
        return new_node


    def visit_FunctionDef(self, node):
        print("  in MyTransformer.visit_FunctionDef()")
        print("   node     =", node)
        print("   name     =", node.name)
        print("   body     =", node.body)

        # FunctionDef(identifier name, arguments args, stmt* body, expr* decorator_list, expr? returns)
        # change function() --> _function()
        new_node = node

        rand_num = random.randint(1, 10)
        if rand_num >= 5:
            print("   changing func body to Pass")
            new_node.body = [ast.Pass]
        else: 
            print("   adding _ before func name")
            new_node.name = "_" + node.name
        ast.copy_location(new_node, node)
        ast.fix_missing_locations(new_node)
        return new_node


    def visit_Lambda(self, node):
        print("  in MyTransformer.visit_Lambda()")
        print("   node     =", node)
        # print("   args     =", node.args.args[0].arg)
        # print("   body     =", node.body)

        # create new node | Lambda(arguments args, expr body)
        new_node = node

        # replace first arg in lambda with new variable named "var1"
        new_node.args.args[0].arg = ast.Name(id='var1', ctx=ast.Load())

        # replace body; just print the arguments
        new_node.body = ast.Call(func=ast.Name(id='hash', ctx=ast.Load()),
                                 args=[node.args],
                                 keywords=[])

        ast.copy_location(new_node, node)
        ast.fix_missing_locations(new_node)
        return new_node


    def visit_If(self, node):
        print("  in MyTransformer.visit_If()")
        print("   node     =", node)
        print("   test     =", node.test)
        # print("   body.id  =", node.body[0].value.func.id)
        # print("   body.arg =", node.body[0].value.args)
        # if node.orelse:
        #     print("   orelse   =", node.orelse[0].value.func.id)

        # create new node | If(expr test, stmt* body, stmt* orelse)
        new_node = node

        # add an orelse if one did not exist
        if not node.orelse:
            # add the following line:   else: print(everything_from_if)
            new_orelse = ast.Call(func=ast.Name(id='print', ctx=ast.Load()),
                                  args=[node.test],
                                  keywords=[])
            new_node.orelse = [new_orelse]
        # remove orelse if one did exist
        else:
            new_node.orelse = []

        ast.copy_location(new_node, node)
        ast.fix_missing_locations(new_node)
        return new_node


    # def visit_Import(self, node):
    #     print("  in MyTransformer.visit_Import()")
    #     print("   node     =", node)
    #     print("   names    =", node.names)

    #     # remove imports
    #     new_names = node.names
    #     new_names.pop()

    #     # Import(alias* names) | alias = (identifier name, identifier? asname)
    #     new_node = node
    #     new_node.names = new_names
    #     ast.copy_location(new_node, node)
    #     ast.fix_missing_locations(new_node)
    #     return new_node


    def visit_List(self, node):
        print("  in MyTransformer.visit_List()")
        print("   node   =", node)
        print("   elts   =", node.elts)

        # List(expr* elts, expr_context ctx)
        # create new_node and remove last elt from list (unless list is empty)
        new_node = node
        if new_node.elts:
            new_node.elts.pop()
        ast.copy_location(new_node, node)
        ast.fix_missing_locations(new_node)
        return new_node


    def visit_NameConstant(self, node):
        print("  in MyTransformer.visit_NameConstant()")
        print("   node   =", node)
        print("   val    =", node.value)

        new_val = node.value

        if node.value == None:    new_value = ast.Num(0)
        elif node.value == True:  new_value = False
        elif node.value == False: new_value = True

        print("   new val =", new_value)

        # create new node | NameConstant(singleton value)
        new_node = node
        new_node.value = new_value
        ast.copy_location(new_node, node)
        ast.fix_missing_locations(new_node)
        return new_node


    def visit_Num(self, node):
        print("  in MyTransformer.visit_Num()")
        print("   node     =", node)
        print("   num      =", node.n)

        # create new node
        new_node = node
        new_node.n = node.n - 1
        print("   new_num  =", new_node.n)
        ast.copy_location(new_node, node)
        ast.fix_missing_locations(new_node)
        return new_node


    def visit_Subscript(self, node):
        print("  in MyTransformer.visit_Subscript()")
        print("   node        =", node)
        print("   slce        =", node.slice)

        # create new node | Subscript(expr value, slice slice, expr_context ctx)
        new_node = node

        # if index is a number > 0, subtract 1
        if isinstance(node.slice, ast.Index) and isinstance(node.slice.value, ast.Num):
            print("   slce val    =", node.slice.value.n)
            if (new_node.slice.value.n > 0):
                new_node.slice.value.n = node.slice.value.n - 1
            print("   new  val    =", new_node.slice.value.n)
        if isinstance(node.slice, ast.Index) and isinstance(node.slice.value, ast.Name):
            print("   slce id     =", node.slice.value.id)

        ast.copy_location(new_node, node)
        ast.fix_missing_locations(new_node)
        return new_node


    # def visit_Try(self, node):
    #     print("  in MyTransformer.visit_Try())")
    #     print("   node     =", node)
    #     print("   body     =", node.body)

    #     # Try(stmt* body, excepthandler* handlers, stmt* orelse, stmt* finalbody)
    #     # ExceptHandler(expr? type, identifier? name, stmt* body)
    #     new_node = node

    #     # create new exception handler that just prints "oops"
    #     new_handler_body = ast.Call(func=ast.Name(id='print', ctx=ast.Load()),
    #                                 args=[ast.Str("oops")],
    #                                 keywords=[])
    #     new_handler = ast.ExceptHandler(type=ast.Name(id=None, ctx=ast.Load()),
    #                                     name=None,
    #                                     body=[new_handler_body])
    #     new_node.handlers = [new_handler]
    #     ast.copy_location(new_node, node)
    #     ast.fix_missing_locations(new_node)
    #     return new_node


    # def visit_Tuple(self, node):
    #     print("  in MyTransformer.visit_Tuple()")
    #     print("   node   =", node)
    #     print("   elts   =", node.elts)

    #     # Tuple(expr* elts, expr_context ctx)
    #     # create new_node and remove last elt from list (unless list is empty)
    #     new_node = node
    #     if new_node.elts:
    #         new_node.elts.pop()
    #     ast.copy_location(new_node, node)
    #     ast.fix_missing_locations(new_node)
    #     return new_node


    def visit_UnaryOp(self, node):
        # unaryop = Invert | Not | UAdd | USub
        print("  in MyTransformer.visit_UnaryOp()")
        print("   node     =", node)
        print("   op       =", node.op)

        curr_op = node.op
        unary_negate = node.op

        if isinstance(curr_op, ast.UAdd):     unary_negate = ast.USub()
        elif isinstance(curr_op, ast.USub):   unary_negate = ast.UAdd()
        elif isinstance(curr_op, ast.Invert): unary_negate = ast.Not()
        elif isinstance(curr_op, ast.Not):    unary_negate = ast.Invert()
        else: print("    did not find negation for", curr_op)

        print("   negation =", unary_negate)

        # create negated node | UnaryOp(unaryop op, expr operand)
        new_node = node
        new_node.op = unary_negate
        ast.copy_location(new_node, node)
        ast.fix_missing_locations(new_node)
        return new_node


    def visit_While(self, node):
        print("  in MyTransformer.visit_While()")
        print("   node     =", node)
        print("   test     =", node.test)
        print("   body     =", node.body)

        # create new node | While(expr test, stmt* body, stmt* orelse)
        new_node = node

        rand_num = random.randint(1, 10)
        if rand_num >= 5:
            # change loop to "while false"
            print("   changing while loop to while false")
            new_node.test = ast.Name(id='false', ctx=ast.Load())
        else:
            print("   changing while loop to while random.randint(0, 10)")
            new_node.test = ast.Call(func=ast.Name(id='random.randint', ctx=ast.Load()),
                                     args=[ast.Num(0), ast.Num(10)],
                                     keywords=[])

        ast.copy_location(new_node, node)
        ast.fix_missing_locations(new_node)
        return new_node


if __name__ == "__main__":
    mutate()
