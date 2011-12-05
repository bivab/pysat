from pysat import Variable as Var, Negation, Clause, Formula
from pypy.rlib.streamio import open_file_as_stream
from pypy.rlib.parsing.ebnfparse import parse_ebnf, make_parse_function

regexs, rules, transformer = parse_ebnf("""
IGNORE: "\t| ";
DECIMAL: "(-)?(0|[1-9][0-9]*)";
COMMENT: "c [^\n]*\n*";
NEWLINE: "\n";
root: NEWLINE* COMMENT* formula EOF;
formula: declaration clauses;
declaration: "p" "cnf" <definition>;
definition: DECIMAL DECIMAL NEWLINE*;
clauses: (clause NEWLINE*)+;
clause: DECIMAL+ "0";
""")
_parse = make_parse_function(regexs, rules, eof=True)
class CNFParser(object):

    def __init__(self):
        self.vars = None
        self.clauses = []
        self.prepared = False
        self.current_clause = 0

    def parse_file(self, f):
        fd = open_file_as_stream(f, 'r')
        lines = fd.readall()
        fd.close()
        return self.parse_string(lines)

    def parse_string(self, string):
        ast = _parse(string)
        tree = transformer().transform(ast)
        return self.visit_root(tree)

    def visit_root(self, root):
        assert root.symbol == 'root'
        return self.visit_formula(root.children[-2])

    def visit_formula(self, formula):
        assert formula.symbol == 'formula'
        definition = formula.children[0]
        clauses = formula.children[1]
        assert len(formula.children) == 2
        definition = self.visit_definition(definition)
        self.visit_clauses(clauses)
        assert None not in self.clauses
        return Formula(self.clauses, self.vars)

    def visit_definition(self, definition):
        assert definition.symbol == 'definition'
        nvars = int(definition.children[0].additional_info)
        nclauses = int(definition.children[1].additional_info)
        self.vars = [Var() for _ in range(nvars)]
        self.clauses = [None] * nclauses

    def visit_clauses(self, clauses):
        assert clauses.symbol == 'clauses'
        data = clauses.children
        for child in data:
            if child.symbol != 'clause':
                assert child.symbol == 'NEWLINE'
                continue
            clause = self.visit_clause(child)
            i = self.current_clause
            self.clauses[i] = clause
            self.current_clause += 1

    def visit_clause(self, clause):
        assert clause.symbol == 'clause'
        data = clause.children
        children = len(data)-1
        assert data[-1].additional_info == '0'
        literals = [None] * children
        for i in range(children):
            index = int(data[i].additional_info)
            var = self.var(abs(index))
            if index < 0:
                var = Negation(var)
            literals[i] = var
        return Clause(literals)

    def var(self, i):
        assert 0 < i <= len(self.vars)
        return self.vars[i-1]
