class Literal(object):
    pass

names = {'var_count' : 0}
def get_var_name():
    global names
    names['var_count'] += 1
    return names['var_count']
class Variable(Literal):

    def __init__(self, name=None):
        if name is None:
            name = self.build_name()
        self.name = name


    def __repr__(self):
        return "%s" % self.name

    def build_name(self):
        name = get_var_name()
        return "var%d" % name

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
            value = assignment.get(v, -1)
            if value == True:
                return True
            elif isinstance(v, Negation):
                value = assignment.get(v.var, -1)
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

    @property
    def assignment(self):
        raise AssertionError, 'not supported'

    def __init__(self, clauses, vars):
        self.clauses = clauses
        self.variables = vars


    def is_conflicting(self, assignment):
        conflicting = False
        for c in self.clauses:
            conflicting = conflicting or c.is_conflicting(assignment)
            if conflicting:
                return True
        return False


    def is_satisfied(self, assignment):
        """Check if the formula is satisfied under the current assignment"""
        sat = True
        for c in self.clauses:
            sat = sat and c.is_satisfied(assignment)
            if not sat:
                return False
        return True

    def __repr__(self):
        return " and ".join("(%r)" % c for c in self.clauses)

    def choose_free_variable(self, assignment):
        for v in self.variables:
            if v in assignment:
                continue
            return v
        raise Exception

    def unit_propagation(self, assignment):
        return assignment.copy()

    def dpll(self, assignment=None):
        if assignment is None:
            assignment = {}
        else:
            assignment = self.unit_propagation(assignment)
        if self.is_satisfied(assignment):
            return assignment
        elif self.is_conflicting(assignment):
            return None
        v = self.choose_free_variable(assignment)
        assert isinstance(v, Variable)
        assignment[v] = True
        a2 = self.dpll(assignment)
        if a2 is not None:
            return a2
        else:
            assignment[v] = False
            return self.dpll(assignment)

