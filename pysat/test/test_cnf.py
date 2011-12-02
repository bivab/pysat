from pysat.parser import CNFParser as parser


class BaseCNFTest(object):
    @classmethod
    def define_test(cls, test, CNF):
        def f(self):
            formula = parser().parse_string(CNF)
            assignment = formula.dpll()
            if test:
                assert assignment is not None
            else:
                assert assignment is None
        return f

    @classmethod
    def define_tests(cls):
        formulas = []
        for key in cls.__dict__:
            if not key.startswith("CNF"):
                continue
            formulas.append((key[3], getattr(cls, key)))
        for i, value in formulas:
            test = cls.define_test(value[0], value[1])
            setattr(cls, 'test_cnf_' + i, test)

class TestCNF(BaseCNFTest):

    CNF1 = True, """
    p cnf 2 1
    1 2 0
    """

    CNF2 = False, """
    p cnf 2 4
    1 2 0
    -1 2 0
    1 -2 0
    -1 -2 0"""
TestCNF.define_tests()
