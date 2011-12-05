import sys, os
from pysat.parser import CNFParser

def main(argv):
    """Main entry point of the stand-alone executable:
    takes a file and invokes the solver on it
    """
    if len(argv) < 2:
        print "Usage: %s filename" % (argv[0],)
        return 2
    f = argv[1]
    assert os.path.isfile(f)
    formula = CNFParser().parse_file(f)
    assignment = formula.dpll()
    if assignment:
        print 'SATISFIABLE'
    else:
        print 'NOT SATISFIABLE'
    return 0

if __name__ == '__main__':
    sys.exit(main(sys.argv))
