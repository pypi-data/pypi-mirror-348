def test_first():
    import endt

    x1 = endt.ContinuumData([1.,1.,2.,2.], name="x1")
    x2 = endt.ContinuumData([100.,200.,100.,200.], name="x2")
    y = endt.ContinuumData([10.,20.,30.,40])

    tree = endt.Tree()
    tree.fit([x1, x2], y)
    print(tree)

    res = tree.predict(1,2)
    print("predict y(1,2) =", res)


def test_second():
    import endt

    x1 = endt.ContinuumData([1.,1.,2.,2.], name="x1")
    x2 = endt.ContinuumData([100.,200.,100.,200.], name="x2")
    y = endt.ContinuumData([10.,20.,30.,40])

    funcs = endt.func.create_lsq_functions([x1, x2], order=2)

    tree = endt.Tree(lsq_funcs=funcs)
    tree.fit([x1, x2], y)
    print(tree)

    res = tree.predict(1,2)
    print("predict y(1,2) =", res)


def test_third():
    import endt
    import numpy as np

    data = np.loadtxt("tests/data.csv").T
    x = list(map(endt.ContinuumData, data[:-1]))
    y = endt.ContinuumData(data[-1])
    for i, xi in enumerate(x, start=1):
        xi.name = f"x{i}" # set name x1, x2, x3... for every feature parameters
    funcs = endt.func.create_lsq_functions(x, order=2)
    tree = endt.Tree(lsq_funcs=funcs)
    tree.fit(x, y)
    print(tree)

    res = tree.predict(1,2)
    print("predict y(1,2) =", res)

