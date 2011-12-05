import py
from pysat import Formula as F, Clause as C, Variable as V, Negation as N

def test_satisfied():
    a = V()
    b = V()
    c = C([a, b])
    f = F([c], [a, b])
    assignment = {}
    assert f.is_satisfied(assignment) == False
    assignment[a] = True
    assignment[b] = False
    assert f.is_satisfied(assignment) == True
    assignment[a] = False
    assignment[b] = True
    assert f.is_satisfied(assignment) == True

def test_satisfied_negation():
    a = V()
    b = V()
    c = C([a, N(b)])
    f = F([c], [a, b])
    assignment= {b: True}
    assert f.is_satisfied(assignment) == False
    assignment[b] = False
    assert f.is_satisfied(assignment) == True
    assignment[a] = False
    assignment[b] = False
    assert f.is_satisfied(assignment) == True

def test_multiple_clauses():
    a = V()
    b = V()
    c = V()
    cs = [C([a, N(b)]), C([N(a), c])]
    f = F(cs, [a, b, c])
    assignment = {}
    assert f.is_satisfied(assignment) == False
    assignment = {a: True, b:True, c:True}
    assert f.is_satisfied(assignment) == True
    assignment = {a: True, b:True, c:False}
    assert f.is_satisfied(assignment) == False

def test_is_conflicting():
    a = V()
    b = V()
    c1 = C([a, b])
    c2 = C([N(a), b])
    f = F([c1], [a,b])
    assignment={a:False, b:False}
    assert f.is_satisfied(assignment) == False
    assert f.is_conflicting(assignment) == True
    f = F([c1], [a,b])
    assignment={a:True, b:False}
    assert f.is_satisfied(assignment) == True
    assert f.is_conflicting(assignment) == False

    f = F([c2], [a,b])
    assignment={a:False, b:False}
    assert f.is_satisfied(assignment) == True
    assert f.is_conflicting(assignment) == False
    f = F([c2], [a,b])
    assignment={a:True, b:False}
    assert f.is_satisfied(assignment) == False
    assert f.is_conflicting(assignment) == True

    f = F([c2], [a,b])
    assignment={a:True}
    assert f.is_satisfied(assignment) == False
    assert f.is_conflicting(assignment) == False

def test_choose_free_variable():
    a = V()
    b = V()
    c = V()
    c1 = C([a, b])
    c2 = C([N(a), c])
    f = F([c1, c2], [a, b, c])
    assert f.choose_free_variable({}) in [a, b, c]
    f = F([c1, c2], [a, b, c])
    assignment={a:True}
    assert f.choose_free_variable(assignment) in [b, c]
    f = F([c1, c2], [a, b, c])
    assignment={a:True, c:False}
    assert f.choose_free_variable(assignment) is b
    f = F([c1, c2], [a, b, c])
    assignment={a:True, c:False, b:True}
    py.test.raises(Exception, f, f.choose_free_variable, assignment)

def test_dpll():
    a = V()
    b = V()
    c = V()
    c1 = C([a, b])
    c2 = C([N(a), c])
    f = F([c1, c2], [a,b,c])
    assignment = f.dpll()
    assert f.is_satisfied(assignment) == True
