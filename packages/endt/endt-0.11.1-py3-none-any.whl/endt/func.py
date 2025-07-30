from . import ContinuumData
import numpy as np
import itertools


class LSQFunction:
    '''This is a general class of any functions

    :param func: A function
    :type func: Any
    :param description: A description of function
    :type description: str
    '''
    def __init__(self, func, description):
        '''Constructor method
        '''
        self.func = func
        self.description = description

    def __call__(self, *args):
        '''Implements access to a class instance as a function, returning a function from self

        :param args: A tuple of input parameters
        :type args: tuple
        :return: A function
        :rtype: Any
        '''
        return self.func(*args)


class LSQFunctionCase1(LSQFunction):
    '''This is a class of power functions

    :param powers: An array of powers of functions
    :type powers: numpy.ndarray[int]
    '''
    def __init__(self, powers):
        '''Constructor method
        '''
        self.powers = powers

    def func(self, *x):
        '''Creates functions of the specified power for input parameters

        :param x: An input parameter or an array of it 
        :type x: float, numpy.ndarray[float]
        :return: A function or an array of functions
        :rtype: float, numpy.ndarray[float]
        '''
        self._check_length(x)

        x_nz = np.array([xi for xi,p in zip(x, self.powers) if p != 0])        
        scalar = not isinstance(x[0], np.ndarray)
        if x_nz.shape[0] == 0:
            if scalar:
                return 1
            else:
                return np.ones(x[0].shape)
        p = np.array([p for p in self.powers if p != 0], dtype=int)
        if not scalar:
            p = p[:,np.newaxis]
        res = np.prod(x_nz**p, 0)
        if scalar:
            res = float(res)
        return res

    def description(self, *x):
        '''Creates the description of function of input parameters

        :param x: An input parameter or an array of it 
        :type x: float, numpy.ndarray[float]
        :return: A description of function
        :rtype: str
        '''
        self._check_length(x)

        res = "*".join([f"{xi}" if p==1 else f"{xi}^{p}"
                        for xi,p in zip(x, self.powers) if p != 0])
        return "1" if res == "" else res

    def _check_length(self, x):
        '''Checks the length of array of input parameters

        :param x: An input parameter or an array of it 
        :type x: float, numpy.ndarray[float]
        :raises RuntimeError: Called if the number of input parameters is not equal to the number of powers
        '''
        if len(x) != len(self.powers):
            raise RuntimeError("Length of arguments should be equal"
                               "length of powers")
         

def create_lsq_functions(x, order, group=None):
    '''Creates groups of functions of the specified order for input parameters

    :param x: An input parameter or an array of it 
    :type x: float, numpy.ndarray[float]
    :param order: An functons order
    :type order: int
    :param group: A number of functions in a group
    :type group: int, optional
    :return: An array of arrays of functions
    :rtype: list[list[LSQFunctionCase1]]
    '''
    index = [i for i,x in enumerate(x) if isinstance(x, ContinuumData)]
    funcs = []
    for i in range(order + 1):
        for pow_ind in itertools.combinations_with_replacement(index, i):
            powers = np.zeros(len(x), dtype=int)
            ind, count = np.unique(pow_ind, return_counts=True)
            ind = np.array(ind, dtype=int)
            powers[ind] = count
            funcs.append(LSQFunctionCase1(powers))
    if group is None:
        group = len(funcs) 
    return list(itertools.combinations(funcs, group))    
