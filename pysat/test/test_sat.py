import py
from pysat import Formula as F, Clause as C, Variable as V, Negation as N

def test_satisfied():
    a = V()
    b = V()
    c = C(a, b)
    f = F(c)
    assert not f.is_satisfied()
    f.assignment[a] = True
    f.assignment[b] = False
    assert f.is_satisfied()
    f.assignment[a] = False
    f.assignment[b] = True
    assert f.is_satisfied()

def test_satisfied_negation():
    a = V()
    b = V()
    c = C(a, N(b))
    f = F(c)
    f.assignment[b] = True
    assert not f.is_satisfied()
    f.assignment[b] = False
    assert f.is_satisfied()
    f.assignment[a] = False
    f.assignment[b] = False
    assert f.is_satisfied()
    
