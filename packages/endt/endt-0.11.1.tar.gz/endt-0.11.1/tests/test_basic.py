import endt as edt
import noout


@noout.noout
def test_simple_tree():
    x = edt.ContinuumData([1.,2.,3.])
    y = edt.ContinuumData([10.,20.,30.])
    tree = edt.Tree()
    tree.fit([x], y)
    for xi, yi in zip(x.data, y.data):
        assert tree.predict(xi) == yi

    tree = edt.Tree(deep=1)
    tree.fit([x], y)
    for xi in x.data:
        assert min(y.data) <= tree.predict(xi) <= max(y.data)
        assert min(y.data) <= tree.predict(xi + 0.5) <= max(y.data)


@noout.noout
def test_simple_discrete():
    x = edt.DiscreteData([1,2,3])
    y = edt.DiscreteData([10,20,30])
    tree = edt.Tree()
    tree.fit([x], y)
    for xi, yi in zip(x.data, y.data):
        assert tree.predict(xi) == yi

    tree = edt.Tree(deep=1)
    tree.fit([x], y)
    for xi in x.data:
        assert tree.predict(xi) in y.data
        assert tree.predict(xi+0.5) in y.data


@noout.noout
def test_simple_mixed():
    x1 = edt.ContinuumData([1.,1.,2.,2.])
    x2 = edt.DiscreteData([1,2,3,4])
    y = edt.ContinuumData([10.,20.,30.,40])
    tree = edt.Tree(save_data=True)
    tree.fit([x1, x2], y)
    for x1i, x2i, yi in zip(x1.data, x2.data, y.data):
        assert tree.predict(x1i, x2i) == yi


@noout.noout
def test_simple_ContinuumDataTree():
    x = [1.,2.,3.]
    y = [10.,20.,30.]
    tree = edt.ContinuumDataTree()
    tree.fit([x], y)
    for xi, yi in zip(x, y):
        assert tree.predict(xi) == yi

    tree = edt.ContinuumDataTree(deep=1)
    tree.fit([x], y)
    assert {tree.predict(xi) for xi in x} != set(y)


@noout.noout
def test_simple_ContinuumDataTree_mixed():
    x1 = edt.ContinuumData([1.,1.,2.,2.])
    x2 = edt.DiscreteData([1.,2.,3.,4.])
    y = edt.DiscreteData([10.,20.,30.,40])
    tree = edt.ContinuumDataTree()
    tree.fit([x1, x2], y)
    for x1i, x2i, yi in zip(x1.data, x2.data, y.data):
        assert tree.predict(x1i, x2i) == yi

    tree = edt.ContinuumDataTree(deep=1)
    tree.fit([x1, x2], y)
    assert {tree.predict(*xi) for xi in zip(x1.data, x2.data)} != set(y)

