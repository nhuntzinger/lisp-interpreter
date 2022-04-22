import pathlib
import sys

import LispFunctions


class LispInterpreter(object):
    def __init__(self, path, debug):
        self.path = pathlib.Path.cwd().absolute() / path
        self.debug = debug

        self.numerical_functions = LispFunctions.NumericalFunctions(self)
        self.control_functions = LispFunctions.ControlFunctions(self)
        self.boolean_functions = LispFunctions.BooleanFunctions(self)
        self.list_functions = LispFunctions.ListFunctions(self)
        self.other_functions = LispFunctions.OtherFunctions(self)

        self.log_buffer_cache = {}

        self.functions = {
            '+': self.numerical_functions.addition,
            '-': self.numerical_functions.subtraction,
            '*': self.numerical_functions.multiplication,
            '/': self.numerical_functions.integer_division,
            'mod': self.numerical_functions.modulo,
            'if': self.control_functions.conditional,
            'not': self.boolean_functions.not_function,
            'and': self.boolean_functions.and_function,
            'or': self.boolean_functions.or_function,
            '=': self.boolean_functions.equals,
            '/=': self.boolean_functions.not_equals,
            '<': self.boolean_functions.less_than,
            '>': self.boolean_functions.greater_than,
            '<=': self.boolean_functions.less_than_or_equals,
            '>=': self.boolean_functions.greater_than_or_equals,
            'car': self.list_functions.car,
            'cdr': self.list_functions.cdr,
            'cons': self.list_functions.cons,
            'last': self.list_functions.last,
            'reverse': self.list_functions.reverse,
            'atom': self.other_functions.atom,
            'quote': self.other_functions.quote,
            'eval': self.other_functions.eval_function,
        }

    def run_program(self):
        """Reads the code in file name, parses it, and executes each
        statement
        """
        program = self.read_file()
        code_list = self.parse_program(program)
        self.eval_lisp_block(code_list, {})

    def read_file(self):
        """reads in a lisp program, returns as one big string"""
        print(f'Reading `{self.path}`')

        with self.path.open('r') as lisp_file:
            whole = ''
            for line in lisp_file:
                # ignore comment lines
                if not line.lstrip().startswith(';'):
                    whole = f'{whole}{self.space_out(line)}'
            return whole

    ########################################################################
    # SYNTAX
    ########################################################################
    def parse_program(self, program_string):
        """
        Takes a string that represents a program, multiple statements
        returns a list of list of tokens, each a being statement
        """
        tokens = program_string.split()
        code_list = []
        while tokens != []:
            code = self.create_code(tokens)
            code_list.append(code)
        return code_list

    def create_code(self, token_list):
        """Takes a token list and returns a parse tree"""
        token = token_list.pop(0)  # retrieve opening parenthesis or atom
        if token.isdigit() or token[0].isdigit():  # integer
            return int(token)
        if token != '(' and isinstance(token, str):  # atom
            return token

        args = []
        while token_list[0] != ')':
            args.append(self.create_code(token_list))

        token_list.pop(0)  # remove closing parenthesis
        return args

    ###########
    # semantics
    ###########
    def eval_lisp_block(self, block, binding):
        """Walks down the block (a list of expressions) evaluating each
        statement and accumulating bindings into this binding for this
        block
        """
        if len(block) == 0:
            return

        code = block[0]
        if isinstance(code, list) and code[0] == 'defun':
            binding[code[1] + "_defun"] = (code[2], code[3])
            self.log(
                0,
                'Create function->definition binding: '
                f'{code[1]} = [{str(code[2])}, {str(code[3])}]'
            )
            # keep working through block
            self.eval_lisp_block(block[1:], binding)
        else:  # found an expression, evaluate it with current bindings
            self.eval_lisp(block[0], [binding])
            self.eval_lisp_block(block[1:], binding)

    def eval_lisp(self, code, bindings=[], depth=0):
        """Evaluates the code with the bindings so far
        bindings is a list of dictionaries, each with a mapping from a symbol
        to its value. These are generated from def statements, and when
        a user-defined function is called
        """
        if self.debug or depth == 0:
            print(f'{self.log_buffer(depth)}Eval {self.to_string(code)}')

        answer = self.eval_lisp_helper(code, bindings, depth)
        if self.debug or depth == 0:
            print(f'{self.log_buffer(depth)}Ans  {self.to_string(answer)} ')

        return answer

    def eval_lisp_helper(self, code, bindings=[], depth=0):
        """Run Lisp commands as defined in self.functions"""
        # Base Cases
        if isinstance(code, int):
            return code
        if code == 'True':
            return True
        if code == 'False':
            return False
        if code == 'nil':
            return []
        if isinstance(code, str):  # variable
            return self.find_value(code, bindings, depth)

        lisp_function = code[0]
        if lisp_function in self.functions:
            return self.functions[lisp_function](code, bindings, depth)

        return self.eval_user_function(code[0], code[1:], bindings, depth + 1)

    def eval_user_function(self, function_name, args, bindings, depth):
        """Execute a user defined function"""
        self.log(depth, f'Calling function {function_name}')
        # lookup the function definition in bindings
        (params, body) = self.find_value(
                            function_name + '_defun',
                            bindings,
                            depth
                        )
        # create binding to hold local variables from parameters, sets and defs
        binding = {}
        # add the mapping from parameter names to values
        for (param, expression) in zip(params, args):
            value = self.eval_lisp(expression, bindings, depth + 1)
            binding[param] = value
            self.log(
                depth,
                f'Create parameter-value binding: {param} = {value}'
            )
        # work through each statement in block
        return (
            self.eval_lisp(body, [binding] + bindings, depth=depth + 1)
        )

    ###########
    # Utilities
    ###########
    def space_out(self, string):
        """Adds spaces around all perenthesis"""
        return string.replace('(', ' ( ').replace(')', ' ) ')

    def find_value(self, name, bindings, depth):
        """Name is a variable, bindings is a list of dictionaries ordered most
        recent first, search up the bindings seeing if this variable is in
        one of the dictionaries
        """
        for binding in bindings:
            if name in binding:
                self.log(
                    depth,
                    f'Found Value of `{name}` as `{binding[name]}`'
                )
                return binding[name]
        print(f'Did not find value `{str(name)}`')

    def simple_equal(self, a, b):
        """Compare if two primitives are equal"""
        if isinstance(a, int) and isinstance(b, int):
            return a == b
        if (a is True and b is True) or (a is False and b is False):
            return True
        return (a == []) and (b == [])

    def to_string(self, code):
        """Prints the parse tree in a more readable form"""
        if isinstance(code, int) or isinstance(code, str) or len(code) == 0:
            return str(code) + ' '
        string = '('
        for item in code:
            string = string + self.to_string(item)
        return string.rstrip(' ') + ')'

    def log_buffer(self, depth):
        """Creates a string of spaces and a pipe to use for indenting
        debug output
        """
        if depth not in self.log_buffer_cache:
            self.log_buffer_cache[depth] = '|  ' * depth
        return self.log_buffer_cache[depth]

    def log(self, depth, message):
        """Prints a debug message"""
        if self.debug:
            print(self.log_buffer(depth) + message)


########################################################################
if __name__ == '__main__':
    sys.setrecursionlimit(10 ** 5)  # Increase the recursion limit

    if len(sys.argv) > 2:
        interpreter = LispInterpreter(path=sys.argv[1], debug=True)
        interpreter.run_program()

    elif len(sys.argv) > 1 and sys.argv[1] != '--help' and sys.argv[1] != '-h':
        interpreter = LispInterpreter(path=sys.argv[1], debug=False)
        interpreter.run_program()

    else:
        print('Usage: python3 lisp.py <filepath> [--debug]')
