import py
from pysat import Formula as F, Clause as C, Variable as V, Negation as N

def test_satisfied():
    a = V()
    b = V()
    c = C([a, b])
    f = F([c], [a, b])
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
    c = C([a, N(b)])
    f = F([c], [a, b])
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
    cs = [C([a, N(b)]), C([N(a), c])]
    f = F(cs, [a, b, c])
    assert f.is_satisfied() == False
    f.assignment = {a: True, b:True, c:True}
    assert f.is_satisfied() == True
    f.assignment = {a: True, b:True, c:False}
    assert f.is_satisfied() == False

def test_is_conflicting():
    a = V()
    b = V()
    c1 = C([a, b])
    c2 = C([N(a), b])
    f = F([c1], [a,b], assignment={a:False, b:False})
    assert f.is_satisfied() == False
    assert f.is_conflicting() == True
    f = F([c1], [a,b], assignment={a:True, b:False})
    assert f.is_satisfied() == True
    assert f.is_conflicting() == False

    f = F([c2], [a,b], assignment={a:False, b:False})
    assert f.is_satisfied() == True
    assert f.is_conflicting() == False
    f = F([c2], [a,b], assignment={a:True, b:False})
    assert f.is_satisfied() == False
    assert f.is_conflicting() == True

    f = F([c2], [a,b], assignment={a:True})
    assert f.is_satisfied() == False
    assert f.is_conflicting() == False

def test_choose_free_variable():
    a = V()
    b = V()
    c = V()
    c1 = C([a, b])
    c2 = C([N(a), c])
    f = F([c1, c2], [a, b, c])
    assert f.choose_free_variable() in [a, b, c]
    f = F([c1, c2], [a, b, c], assignment={a:True})
    assert f.choose_free_variable() in [b, c]
    f = F([c1, c2], [a, b, c], assignment={a:True, c:False})
    assert f.choose_free_variable() is b
    f = F([c1, c2], [a, b, c], assignment={a:True, c:False, b:True})
    py.test.raises(Exception, f, f.choose_free_variable)

def test_dpll():
    a = V()
    b = V()
    c = V()
    c1 = C([a, b])
    c2 = C([N(a), c])
    f = F([c1, c2], [a,b,c])
    assignment = f.dpll()
    f.assignment = assignment
    assert f.is_satisfied() == True
