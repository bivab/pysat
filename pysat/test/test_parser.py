import py
from pysat import Formula
from pysat.parser import CNFParser

class TestCNFParser(object):
    SAT = """
c This is a comment of the example file.
p cnf 3 3
1 2 -3 0
-1 2 0
-2 0
"""
    SAT2 = """
c A sample .cnf file.
p cnf 3 2
1 -3 0
2 3 -1 0"""

    COMMENT  = "c A sample .cnf file."
    COMMENT2 = "   c A sample .cnf file."

    CNF  = " p cnf 3 2"
    CNF2 = "p cnf 3 9"

    CLAUSE = "1 -3 0"
    CLAUSE2 = " 1 3 -2 0"


    def setup_method(self, mthd):
        self.parser = CNFParser()
        self.parser.prepared = True

    def test_parse(self):
        f = self.parser.parse_string(self.SAT2)
        assert isinstance(f, Formula)
        assert len(f.variables) == 3
        assert len(f.clauses) == 2

    def test_parse_comment(self):
        assert self.parser.parse_line(self.COMMENT) is None
        assert self.parser.parse_line(self.COMMENT2) is None

    def test_parse_formula(self):
        assert self.parser.parse_cnf(self.CNF) == (3, 2)
        assert self.parser.parse_cnf(self.CNF2) == (3, 9)

    def test_parse_clause(self):
        assert self.parser.parse_clause(self.CLAUSE) == (1, -3)
        assert self.parser.parse_clause(self.CLAUSE2) == (1, 3, -2)
