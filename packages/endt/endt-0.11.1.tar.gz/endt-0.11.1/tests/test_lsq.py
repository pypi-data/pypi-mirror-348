import endt as edt
import numpy as np
import pytest
import noout

func = edt.func

def exact(x, y, order, deep=None, group=None):
    funcs = func.create_lsq_functions(x, order=order, group=group)
    tree = edt.Tree(lsq_funcs=funcs, deep=deep)
    tree.fit(x, y)
    for yi, *xi in zip(y.data, *[xi.data for xi in x]):
        assert tree.predict(*xi) == yi


@noout.noout
def test_lsq_simple():
    x = edt.ContinuumData([0.,1.,2.])
    y = edt.ContinuumData([1.,0.,1.])
    exact([x], y, 2, deep=1)
    x = edt.ContinuumData([-1.,0.,1.])
    exact([x], y, 2, group=1, deep=1)
    exact([x], y, 2, group=2, deep=1)


@noout.noout
def test_lsq_two():
    x1 = [-1., 0., 1.]
    x2 = x1
    x1, x2 = np.meshgrid(x1 ,x2)
    x1, x2 = map(np.ndarray.flatten, [x1, x2])
    y = x1**2 + x2**2
    x1, x2, y = map(edt.ContinuumData, [x1, x2, y])
    exact([x1, x2], y, 2, deep=2)
    exact([x1, x2], y, 2, deep=2, group=1)

    x1 = edt.ContinuumData(x1.data-1)
    x2 = edt.ContinuumData(x2.data-2)
    y = edt.ContinuumData((x1.data+1)**2 + (x2.data+2)**2)
    exact([x1, x2], y, 2, deep=2)
