import sys, os
from time import time
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
    parse_start = time()
    formula = CNFParser().parse_file(f)
    parse_end = time()
    solve_start = time()
    assignment = formula.dpll()
    solve_end = time()

    print '------------------------------------------------------------'
    print 'Runtime %d ms' % int((solve_end - parse_start) * 1000)
    print 'Parser %d ms' % int((parse_end - parse_start) * 1000)
    print 'DPLL %d ms' % int((solve_end - solve_start) * 1000)
    print 'Conflicts %d' % formula.conflicts
    print '------------------------------------------------------------'
    if assignment:
        print 'SATISFIABLE'
    else:
        print 'NOT SATISFIABLE'
    return 0

if __name__ == '__main__':
    sys.exit(main(sys.argv))
