class NumericalFunctions(object):
    def __init__(self, interpreter):
        self.interpreter = interpreter

    def addition(self, code, bindings, depth):
        return (
            self.interpreter.eval_lisp(code[1], bindings, depth + 1)
            + self.interpreter.eval_lisp(code[2], bindings, depth + 1)
            )

    def subtraction(self, code, bindings, depth):
        return (
            self.interpreter.eval_lisp(code[1], bindings, depth + 1)
            - self.interpreter.eval_lisp(code[2], bindings, depth + 1)
            )

    def multiplication(self, code, bindings, depth):
        return (
            self.interpreter.eval_lisp(code[1], bindings, depth + 1)
            * self.interpreter.eval_lisp(code[2], bindings, depth + 1)
            )

    def integer_division(self, code, bindings, depth):
        return (
            self.interpreter.eval_lisp(code[1], bindings, depth + 1)
            // self.interpreter.eval_lisp(code[2], bindings, depth + 1)
            )

    def modulo(self, code, bindings, depth):
        return (
            self.interpreter.eval_lisp(code[1], bindings, depth + 1)
            % self.interpreter.eval_lisp(code[2], bindings, depth + 1)
            )


class ControlFunctions(object):
    def __init__(self, interpreter):
        self.interpreter = interpreter

    def conditional(self, code, bindings, depth):
        """If operator"""
        if self.interpreter.eval_lisp(code[1], bindings, depth + 1):
            return self.interpreter.eval_lisp(code[2], bindings, depth + 1)
        else:
            return self.interpreter.eval_lisp(code[3], bindings, depth + 1)


class BooleanFunctions(object):
    def __init__(self, interpreter):
        self.interpreter = interpreter

    def not_function(self, code, bindings, depth):
        return not self.interpreter.eval_lisp(code[1], bindings, depth + 1)

    def and_function(self, code, bindings, depth):
        return (
            self.interpreter.eval_lisp(code[1], bindings, depth + 1)
            and self.interpreter.eval_lisp(code[2], bindings, depth + 1)
        )

    def or_function(self, code, bindings, depth):
        return (
            self.interpreter.eval_lisp(code[1], bindings, depth + 1)
            or self.interpreter.eval_lisp(code[2], bindings, depth + 1)
        )

    def equals(self, code, bindings, depth):
        return (
            self.interpreter.eval_lisp(code[1], bindings, depth + 1)
            == self.interpreter.eval_lisp(code[2], bindings, depth + 1)
        )

    def not_equals(self, code, bindings, depth):
        return (
            self.interpreter.eval_lisp(code[1], bindings, depth + 1)
            != self.interpreter.eval_lisp(code[2], bindings, depth + 1)
        )

    def less_than(self, code, bindings, depth):
        return (
            self.interpreter.eval_lisp(code[1], bindings, depth + 1)
            < self.interpreter.eval_lisp(code[2], bindings, depth + 1)
        )

    def greater_than(self, code, bindings, depth):
        return (
            self.interpreter.eval_lisp(code[1], bindings, depth + 1)
            > self.interpreter.eval_lisp(code[2], bindings, depth + 1)
        )

    def less_than_or_equals(self, code, bindings, depth):
        return (
            self.interpreter.eval_lisp(code[1], bindings, depth + 1)
            <= self.interpreter.eval_lisp(code[2], bindings, depth + 1)
        )

    def greater_than_or_equals(self, code, bindings, depth):
        return (
            self.interpreter.eval_lisp(code[1], bindings, depth + 1)
            >= self.interpreter.eval_lisp(code[2], bindings, depth + 1)
        )


class ListFunctions(object):
    def __init__(self, interpreter):
        self.interpreter = interpreter

    def car(self, code, bindings, depth):
        """Takes a list and returns the first element"""
        return self.interpreter.eval_lisp(code[1], bindings, depth + 1)[0]

    def cdr(self, code, bindings, depth):
        """Takes a list and returns a list of all the elements except
        the first
        """
        return self.interpreter.eval_lisp(code[1], bindings, depth + 1)[1:]

    def cons(self, code, bindings, depth):
        """Takes an element and a list and returns a list with the
        element inserted at the first place of the list
        """
        return (
            [self.interpreter.eval_lisp(code[1], bindings, depth + 1)]
            + self.interpreter.eval_lisp(code[2], bindings, depth + 1)
        )

    def last(self, code, bindings, depth):
        """Returns the last element of a list"""
        return [self.interpreter.eval_lisp(code[1], bindings, depth + 1)[-1]]

    def reverse(self, code, bindings, depth):
        """Reverses a list"""
        return self.interpreter.eval_lisp(code[1], bindings, depth + 1)[::-1]


class OtherFunctions(object):
    def __init__(self, interpreter):
        self.interpreter = interpreter

    def atom(self, code, bindings, depth):
        """Checks if a value is an atom"""
        value = self.interpreter.eval_lisp(code[1], bindings, depth + 1)
        return (
            isinstance(value, int)
            or isinstance(value, str)
            or value is True
            or value is False
            or value == []
        )

    def quote(self, code, bindings, depth):
        """Stop evaluation"""
        return code[1]

    def eval_function(self, code, bindings, depth):
        """Evaluate to get the code, then evaluate the code. Must be a
        user function call.
        """
        return (
            self.interpreter.eval_lisp(
                self.interpreter.eval_lisp(code[1], bindings, depth + 1)
            )
        )
