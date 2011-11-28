import py
from pysat import Formula as F, Clause as C, Variable as V, Negation as N

def test_satisfied():
    a = V()
    b = V()
    c = C(a, b)
    f = F(c)
    assert f.is_satisfied() == False
    f.assignment[a] = True
    f.assignment[b] = False
    assert f.is_satisfied() == True
    f.assignment[a] = False
    f.assignment[b] = True
    assert f.is_satisfied() == True

def test_satisfied_negation():
    a = V()
    b = V()
    c = C(a, N(b))
    f = F(c)
    f.assignment[b] = True
    assert f.is_satisfied() == False
    f.assignment[b] = False
    assert f.is_satisfied() == True
    f.assignment[a] = False
    f.assignment[b] = False
    assert f.is_satisfied() == True

def test_multiple_clauses():
    a = V()
    b = V()
    c = V()
    cs = [C(a, N(b)), C(N(a), c)]
    f = F(*cs)
    assert f.is_satisfied() == False
    f.assignment = {a: True, b:True, c:True}
    assert f.is_satisfied() == True
    f.assignment = {a: True, b:True, c:False}
    assert f.is_satisfied() == False



