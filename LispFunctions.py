# Numerical functions
def addition(interpreter, code, bindings, depth):
    return (
        interpreter.eval_lisp(code[1], bindings, depth + 1)
        + interpreter.eval_lisp(code[2], bindings, depth + 1)
        )


def subtraction(interpreter, code, bindings, depth):
    return (
        interpreter.eval_lisp(code[1], bindings, depth + 1)
        - interpreter.eval_lisp(code[2], bindings, depth + 1)
        )


def multiplication(interpreter, code, bindings, depth):
    return (
        interpreter.eval_lisp(code[1], bindings, depth + 1)
        * interpreter.eval_lisp(code[2], bindings, depth + 1)
        )


def integer_division(interpreter, code, bindings, depth):
    return (
        interpreter.eval_lisp(code[1], bindings, depth + 1)
        // interpreter.eval_lisp(code[2], bindings, depth + 1)
        )


def modulo(interpreter, code, bindings, depth):
    return (
        interpreter.eval_lisp(code[1], bindings, depth + 1)
        % interpreter.eval_lisp(code[2], bindings, depth + 1)
        )


# Control functions
def conditional(interpreter, code, bindings, depth):
    """If operator"""
    if interpreter.eval_lisp(code[1], bindings, depth + 1):
        return interpreter.eval_lisp(code[2], bindings, depth + 1)
    else:
        return interpreter.eval_lisp(code[3], bindings, depth + 1)


#  Boolean functions
def not_function(interpreter, code, bindings, depth):
    return not interpreter.eval_lisp(code[1], bindings, depth + 1)


def and_function(interpreter, code, bindings, depth):
    return (
        interpreter.eval_lisp(code[1], bindings, depth + 1)
        and interpreter.eval_lisp(code[2], bindings, depth + 1)
    )


def or_function(interpreter, code, bindings, depth):
    return (
        interpreter.eval_lisp(code[1], bindings, depth + 1)
        or interpreter.eval_lisp(code[2], bindings, depth + 1)
    )


def equals(interpreter, code, bindings, depth):
    return (
        interpreter.eval_lisp(code[1], bindings, depth + 1)
        == interpreter.eval_lisp(code[2], bindings, depth + 1)
    )


def not_equals(interpreter, code, bindings, depth):
    return (
        interpreter.eval_lisp(code[1], bindings, depth + 1)
        != interpreter.eval_lisp(code[2], bindings, depth + 1)
    )


def less_than(interpreter, code, bindings, depth):
    return (
        interpreter.eval_lisp(code[1], bindings, depth + 1)
        < interpreter.eval_lisp(code[2], bindings, depth + 1)
    )


def greater_than(interpreter, code, bindings, depth):
    return (
        interpreter.eval_lisp(code[1], bindings, depth + 1)
        > interpreter.eval_lisp(code[2], bindings, depth + 1)
    )


def less_than_or_equals(interpreter, code, bindings, depth):
    return (
        interpreter.eval_lisp(code[1], bindings, depth + 1)
        <= interpreter.eval_lisp(code[2], bindings, depth + 1)
    )


def greater_than_or_equals(interpreter, code, bindings, depth):
    return (
        interpreter.eval_lisp(code[1], bindings, depth + 1)
        >= interpreter.eval_lisp(code[2], bindings, depth + 1)
    )


# List functions
def car(interpreter, code, bindings, depth):
    """Takes a list and returns the first element"""
    return interpreter.eval_lisp(code[1], bindings, depth + 1)[0]


def cdr(interpreter, code, bindings, depth):
    """Takes a list and returns a list of all the elements except
    the first
    """
    return interpreter.eval_lisp(code[1], bindings, depth + 1)[1:]


def cons(interpreter, code, bindings, depth):
    """Takes an element and a list and returns a list with the
    element inserted at the first place of the list
    """
    return (
        [interpreter.eval_lisp(code[1], bindings, depth + 1)]
        + interpreter.eval_lisp(code[2], bindings, depth + 1)
    )


def last(interpreter, code, bindings, depth):
    """Returns the last element of a list"""
    return [interpreter.eval_lisp(code[1], bindings, depth + 1)[-1]]


def reverse(interpreter, code, bindings, depth):
    """Reverses a list"""
    return interpreter.eval_lisp(code[1], bindings, depth + 1)[::-1]


# Other functions
def atom(interpreter, code, bindings, depth):
    """Checks if a value is an atom"""
    value = interpreter.eval_lisp(code[1], bindings, depth + 1)
    return (
        isinstance(value, int)
        or isinstance(value, str)
        or value is True
        or value is False
        or value == []
    )


def quote(interpreter, code, bindings, depth):
    """Stop evaluation"""
    return code[1]


def eval_function(interpreter, code, bindings, depth):
    """Evaluate to get the code, then evaluate the code. Must be a
    user function call.
    """
    return (
        interpreter.eval_lisp(
            interpreter.eval_lisp(code[1], bindings, depth + 1)
        )
    )


def define_operators():
    lisp_functions = {
        '+': addition,
        '-': subtraction,
        '*': multiplication,
        '/': integer_division,
        'mod': modulo,
        'if': conditional,
        'not': not_function,
        'and': and_function,
        'or': or_function,
        '=': equals,
        '/=': not_equals,
        '<': less_than,
        '>': greater_than,
        '<=': less_than_or_equals,
        '>=': greater_than_or_equals,
        'car': car,
        'cdr': cdr,
        'cons': cons,
        'last': last,
        'reverse': reverse,
        'atom': atom,
        'quote': quote,
        'eval': eval_function,
    }
