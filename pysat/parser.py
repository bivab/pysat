from pysat import Variable as Var, Negation, Clause, Formula
class CNFParser(object):
    def __init__(self):
        self.vars = None
        self.clauses = None
        self.prepared = False
        self.current_clause = 0

    def parse_file(self, f):
        with open(f, 'r') as fd:
            for line in fd:
                self.parse_line(line)
        assert None not in self.clauses
        assert None not in self.vars
        assert self.prepared
        return self.build_formula()

    def parse_string(self, string):
        for line in string.splitlines():
            self.parse_line(line)
        assert None not in self.clauses
        assert None not in self.vars
        assert self.prepared
        return self.build_formula()


    def parse_line(self, line):
        line = line.strip()
        if len(line) == 0:
            return
        if line[0] == 'c':
            return
        if line[0] == 'p':
            cnf = self.parse_cnf(line)
            self.setup_formula(cnf)
            return cnf
        else:
            clause = self.parse_clause(line)
            self.build_clause(clause)
            return clause

    def parse_cnf(self, line):
        line = line.strip()
        elements = line.split(' ')
        assert elements[0] == 'p'
        assert elements[1] == 'cnf'
        return (int(elements[2]), int(elements[3]))

    def parse_clause(self, line):
        line = line.strip()
        elements = tuple(int(x) for x in line.split(' '))
        assert elements[-1] == 0
        return elements[:-1]

    def build_clause(self, data):
        assert self.prepared
        literals = [None] * len(data)
        for i in range(len(data)):
            var = data[i]
            lit = self.var(abs(var))
            if var < 0:
                lit = Negation(lit)
            literals[i] = lit
        self.clauses[self.current_clause] = Clause(literals)
        self.current_clause += 1

    def build_formula(self):
        return Formula(self.clauses, self.vars)

    def setup_formula(self, cnf):
        self.prepared = True
        self.vars = [Var() for _ in range(cnf[0])]
        self.clauses = [None] * cnf[1]

    def var(self, i):
        assert 0 < i <= len(self.vars)
        return self.vars[i-1]

