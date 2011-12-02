import sys, os
from pysat.parser import CNFParser

def main(argv):
    f = argv[1]
    assert os.path.isfile(f)
    formula = CNFParser().parse_file(f)
    assignment = formula.dpll()
    #print repr(formula)
    if assignment:
        print 'SATISFIABLE'
    else:
        print 'NOT SATISFIABLE'

main(sys.argv)
