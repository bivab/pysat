from pysat.__main__ import main

entry_point = main

def target(driver, args):
    return entry_point, None

from pypy.jit.codewriter.policy import JitPolicy

def jitpolicy(driver):
    return JitPolicy()
# ____________________________________________________________


if __name__ == '__main__':
    import sys
    sys.exit(entry_point(sys.argv))
