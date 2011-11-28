class Literal(object):
    pass

class Variable(Literal):
    pass

class Negation(Literal):
    def __init__(self, var):
        self.var = var

class Clause(object):
    literals = []
    def __init__(self, *args):
        self.literals = args

class Formula(object):
    clauses = []

    def __init__(self, *args):
        self.clauses = args
        self.assignment = {}

    def is_satisfied(self):
        """Check if the formula is satisfied under the current assignment"""
        if self.assignment is None:
            raise Exception("No assignment given")
        for c in self.clauses:
            for v in c.literals:
                if v in self.assignment and self.assignment[v]:
                    return True
                if isinstance(v, Negation):
                    v = v.var
                    if v in self.assignment and not self.assignment[v]:
                        return True
        return False

