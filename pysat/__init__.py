from pypy.rlib.listsort import TimSort

class TupleSort(TimSort):
    def lt(self, a, b):
        return a[0] < b[0]

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

    def unit_propagation(self, assignment):
        # only propagate if clause is not satisfied
        if self.is_satisfied(assignment):
            return False
        free_literal = None
        for literal in self.literals:
            if isinstance(literal, Negation):
                var = literal.var
            else:
                var = literal
            # var is bound
            if var in assignment:
                continue
            # we have more than one free variable
            if free_literal is not None:
                return False
            free_literal = literal

        # no free variables
        if free_literal is None:
            return False
        if isinstance(free_literal, Negation):
            assignment[free_literal.var] = False
        else:
            assignment[free_literal] = True
        return True



    def __repr__(self):
        return " or ".join(repr(var) for var in self.literals)

class Formula(object):

    @property
    def assignment(self):
        raise AssertionError, 'not supported'

    def __init__(self, clauses, vars, sort_vars=True):
        self.clauses = clauses
        self.variables = vars
        self.conflicts = 0
        if sort_vars:
            self.sort_variables()

    def variable_freqs(self):
        freqs = {}
        for v in self.variables:
            freqs[v] = 0
        for clause in self.clauses:
            for literal in clause.literals:
                if isinstance(literal, Negation):
                    var = literal.var
                else:
                    var = literal
                freqs[var] += 1
        return freqs

    def sort_variables(self):
        freqs = self.variable_freqs()
        dec = [(freqs[v], v) for v in self.variables]
        ts = TupleSort(dec)
        ts.sort()
        self.variables = [dec[i][1] for i in range(len(dec)-1, -1, -1)]

    def is_conflicting(self, assignment):
        conflicting = False
        for c in self.clauses:
            conflicting |= c.is_conflicting(assignment)
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
        assign = assignment.copy()
        change = True
        while change:
            change = False
            for clause in self.clauses:
                change |= clause.unit_propagation(assign)
        return assign

    def dpll(self, assignment=None):
        if assignment is None:
            assignment = {}
        a1 = self.unit_propagation(assignment)
        if self.is_satisfied(a1):
            return a1
        elif self.is_conflicting(a1):
            self.conflicts += 1
            return None
        v = self.choose_free_variable(a1)
        assert isinstance(v, Variable)
        a1[v] = True
        a2 = self.dpll(a1)
        if a2 is not None:
            return a2
        else:
            a1[v] = False
            return self.dpll(a1)

