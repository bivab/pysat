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
    SAT2 = """c A sample .cnf file.
p cnf 3 2
1 -3 0
2 3 -1 0"""

    def setup_method(self, mthd):
        self.parser = CNFParser()
        self.parser.prepared = True

    def test_parse(self):
        f = self.parser.parse_string(self.SAT)
        assert isinstance(f, Formula)
        assert len(f.variables) == 3
        assert len(f.clauses) == 3
        assert f.clauses[1].literals[1] == f.clauses[2].literals[0].var

    def test_parse2(self):
        f = self.parser.parse_string(self.SAT2)
        assert isinstance(f, Formula)
        assert len(f.variables) == 3
        assert len(f.clauses) == 2

