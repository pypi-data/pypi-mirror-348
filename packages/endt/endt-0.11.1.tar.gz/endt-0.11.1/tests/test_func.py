import endt as edt
import numpy as np
import pytest
import noout

func = edt.func

@noout.noout
def test_create_func():
    x = edt.ContinuumData([])
    funcs = func.create_lsq_functions([x], 3)
    for ff in funcs:
        for f in ff:
           assert isinstance(f,  func.LSQFunctionCase1)
    assert len(funcs) == 1
    assert len(funcs[0]) == 4
    descs = {f.description("x") for f in funcs[0]}
    assert descs == {"1", "x", "x^2", "x^3"}
    xd = np.random.rand(5)
    assert {tuple(xd**n) for n in range(4)} == {tuple(f(xd)) for f in funcs[0]}
    assert {2**n for n in range(4)} == {f(2) for f in funcs[0]}


@noout.noout   
def test_create_func_multiple():
    x1 = edt.ContinuumData([])
    x2 = edt.DiscreteData([])
    x3 = edt.ContinuumData([])
    funcs = func.create_lsq_functions([x1, x2, x3], 2)
    for ff in funcs:
        for f in ff:
           assert isinstance(f,  func.LSQFunctionCase1)
    assert len(funcs) == 1
    assert len(funcs[0]) == 6
    descs = {f.description("x1", "x2", "x3") for f in funcs[0]}

    assert descs == {"1", "x1", "x1^2", "x3", "x3^2", "x1*x3"}
    xd1 = np.random.rand(5)
    xd3 = np.random.rand(5)
    predict = [xd1**0, xd1, xd1**2, xd3, xd3**2, xd1*xd3]
    predict = set(map(tuple, predict))
    assert predict == {tuple(f(xd1, "aa", xd3)) for f in funcs[0]}


@noout.noout
def test_create_func_group():
    x1 = edt.ContinuumData([])
    x2 = edt.ContinuumData([])
    funcs = func.create_lsq_functions([x1, x2], 2, group=5)
    for ff in funcs:
        assert len(ff) == 5
        for f in ff:
           assert isinstance(f,  func.LSQFunctionCase1)
    assert len(funcs) == 6

    descs = [{f.description("x1", "x2") for f in ff} for ff in funcs]
    descs_predict = [{"1", "x1", "x1^2", "x2", "x2^2"},
                    {"1", "x1", "x1^2", "x2", "x1*x2"},
                    {"1", "x1", "x1^2", "x2^2", "x1*x2"},
                    {"1", "x1", "x2", "x2^2", "x1*x2"},
                    {"1", "x1^2", "x2", "x2^2", "x1*x2"},
                    {"x1", "x1^2", "x2", "x2^2", "x1*x2"}]
    descs = set(map(frozenset, descs))
    descs_predict = set(map(frozenset, descs_predict))

    assert descs == descs_predict


@noout.noout
def test_exceptions():
    x = edt.ContinuumData([])
    funcs = func.create_lsq_functions([x], 3)
    for ff in funcs:
        for f in ff:
            with pytest.raises(RuntimeError):
                f.description("x1", "x2")
            with pytest.raises(RuntimeError):
                f(1, 2)
