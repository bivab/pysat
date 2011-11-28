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

    def check_clause(self, clause):
        for v in clause.literals:
            value = self.assignment.get(v, None)
            if value == True:
                return True
            elif isinstance(v, Negation):
                value = self.assignment.get(v.var, None)
                if value == False:
                    return True
        return False
    def is_satisfied(self):
        """Check if the formula is satisfied under the current assignment"""
        sat = True
        if self.assignment is None:
            raise Exception("No assignment given")
        for c in self.clauses:
            sat = sat and self.check_clause(c)
            if not sat:
                return False
        return True
