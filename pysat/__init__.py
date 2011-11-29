class Literal(object):
    pass

class Variable(Literal):
    index = 0

    def __init__(self, name=None):
        if name is None:
            name = self.build_name()
        self.name = name


    def __repr__(self):
        return "%s" % self.name

    def build_name(self):
        name = "var%d" % Variable.index
        Variable.index += 1
        return name

class Negation(Literal):
    def __init__(self, var):
        self.var = var

    def __repr__(self):
        return "not(%r)" % self.var

class Clause(object):
    literals = []
    def __init__(self, *args):
        self.literals = args
        self.vars = []
        for l in args:
            if isinstance(l, Negation):
                self.vars.append(l.var)
            else:
                self.vars.append(l)

    def is_satisfied(self, assignment):
        for v in self.literals:
            value = assignment.get(v, None)
            if value == True:
                return True
            elif isinstance(v, Negation):
                value = assignment.get(v.var, None)
                if value == False:
                    return True
        return False

    def is_conflicting(self, assignment):
        if not self.is_satisfied(assignment):
            for v in self.vars:
                if v in assignment:
                    continue
                return False
            return True
        return False

    def __repr__(self):
        return " or ".join(repr(var) for var in self.literals)


class Formula(object):
    clauses = []

    def __init__(self, *args, **kwargs):
        self.clauses = args
        if 'assignment' in kwargs:
            self.assignment = kwargs['assignment']
        else:
            self.assignment = {}


    def is_conflicting(self):
        conflicting = False
        for c in self.clauses:
            conflicting = conflicting or c.is_conflicting(self.assignment)
            if conflicting:
                return True
        return False


    def is_satisfied(self):
        """Check if the formula is satisfied under the current assignment"""
        sat = True
        if self.assignment is None:
            raise Exception("No assignment given")
        for c in self.clauses:
            sat = sat and c.is_satisfied(self.assignment)
            if not sat:
                return False
        return True

    def __repr__(self):
        return " and ".join("(%r)" % c for c in self.clauses)
