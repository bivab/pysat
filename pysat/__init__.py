class Literal(object):
    pass

class Variable(Literal):
    index = 1

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
    def __init__(self, literals):
        self.literals = literals
        self.vars = []
        for l in literals:
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

    def __init__(self, clauses, vars, assignment=None):
        self.clauses = clauses
        self.variables = vars
        if assignment is not None:
            self.assignment = assignment
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

    def choose_free_variable(self):
        for v in self.variables:
            if v in self.assignment:
                continue
            return v
        raise Exception

    def dpll(self):
        #self.unit_propagation()
        if self.is_satisfied():
            return self.assignment
        elif self.is_conflicting():
            return None
        v = self.choose_free_variable()
        self.assignment[v] = True
        a2 = self.dpll()
        if a2 is not None:
            return a2
        else:
            self.assignment[v] = False
            return self.dpll()

