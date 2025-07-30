#!/usr/bin/env python3
import numpy as np
import scipy.stats
import dataclasses
import abc
import functools
import itertools
from collections.abc import Callable
from typing import Any
import re
from .data import * 
from . import func


class LeastSquares:
    '''This class implements the least squares method

    :param y: An output parameter
    :type y: Data
    :param fs: An array of functions
    :type fs: list[LSQFunction]
    '''
    base_data_type = ContinuumData

    def __init__(self, x, fs):
        """Constructor method
        """
        self.x_names = [xi.name for xi in x]
        x = [xi.data for xi in x]
        self.fs = fs
        self.M = np.array([fi(*x) for fi in fs]).T

    def choose(self, y, my_ind):
        '''Chooses functions based on the least squares method

        :param y: An output parameter
        :type y: Data
        :param my_ind: Index of functions
        :type my_ind: int
        :return: Chosen functions as an instance of Choice class
        :rtype: Choice
        '''
        fs = self.fs
        coefs = np.linalg.lstsq(self.M, y.data, rcond=None)[0]
        data_name = self.choice_name(coefs)
        data = self.base_data_type(self.M @ coefs, name=data_name)
        choice = data.choose(y, my_ind=0)
        choice_f = choice.function
        choice.function = lambda *x: choice_f(sum([c*fi(*x) for fi,c
                                                   in zip(fs, coefs)]))
        return choice

    def clear(self):
        '''Сlears self
        '''
        self.M = None
        self.fs = None

    def choice_name(self, coefs):
        '''Chooses name for solutions obtained by the least squares method

        :param coefs: An array of solutions
        :type coefs: numpy.ndarray[float]
        :return: A name for solutions
        :rtype: str
        '''
        data_name = ""
        for c, f in zip(coefs, self.fs):
            data_name += (" - " if c<0 else " + ") + str(abs(c)) + "*"
            data_name += f.description(*self.x_names)
        data_name = data_name[1:]
        if data_name[0] == "+":
            data_name = data_name[2:]
        return data_name

class Tree:
    '''This is a class representation of an enhanced decision tree

    :param lsq_funcs: An array of function arrays
    :type lsq_funcs: list[list[LSQFunction]], optional
    :param deep: A deep of tree construction
    :type deep: int, optional
    :param save_data: `True` if self is need to save, `False` if not
    :type save_data: bool, optional
    '''

    lsq = LeastSquares

    def __init__(self, *, lsq_funcs = [], lsq_method=None, deep=None,
                 save_data=False):
        """Constructor method
        """
        self.lsq_funcs = lsq_funcs
        self.lsq_method = lsq_method
        self.deep = deep
        self.save_data = save_data

        self.next_trees = None
        self.x = None
        self.y = None
        self.t = []
        self.choice = Choice()
        self.y_aver = None

    def fit(self, x, y):
        '''Fill self and start bildining tree

        :param x: An input parameters
        :type x: list[BaseData]
        :param y: An output parameter
        :type y: Data
        :return: self
        :rtype: Tree
        '''
        self.fit_no_calc(x, y)
        self.calc()
        return self

    def fit_no_calc(self, x, y):
        '''Fills self.x, self.y and self.y_aver

        :param x: An input parameters
        :type x: list[BaseData]
        :param y: An output parameter
        :type y: Data
        :return: self
        :rtype: Tree
        '''
        self.x = [type(xi)(xi) for xi in x]
        self.y = type(y)(y)
        self.y_aver = self.y.average
        return self        

    def calc(self):
        '''Builds tree

        :raises RuntimeError: Called when a tree is attempted to be calculated multiple times
        '''
        if self.next_trees is not None:
            raise RuntimeError("Multiple calc call")
        if (self.deep is not None and self.deep < 1) or self.y.variants < 2:
            self.cut()
        else:
            self.t = [self.lsq(self.x, fs) for fs in self.lsq_funcs]
            x_all = self.x + self.t

            self.choice = max((xi.choose(self.y, i) for i, xi in enumerate(x_all)),
                         key=lambda a: a.entropy)
 
            if self.choice.entropy < 0:
                self.cut()
            else:
                self.next_trees = []
                for ind in self.choice.indexes:
                    nt = self.subtree()
                    nt.fit_no_calc([xi[ind] for xi in self.x], self.y[ind])
                    self.next_trees.append(nt)

                self.clear()
                for tree in self.next_trees:
                    tree.calc()                

    def cut(self):
        '''Cuts tree
        '''
        self.next_trees = []
        self.clear()

    def clear(self):
        '''Clears data
        '''
        if not self.save_data:
            for v in (*self.x, self.y , self.t, self.choice):
                v.clear()

    def predict(self, *args):
        '''Predicts behavior of output parameter based on the original data input parameters

        :param args: A tuple of input parameters
        :type args: tuple
        :return: An average value of output parameter if self.next_trees is empty and recursively calls itself if not
        :rtype: float
        '''
        if self.next_trees == []:
            return self.y_aver
        choice = self.choice.function(*args)
        tree = self.next_trees[int(choice)]
        return tree.predict(*args)

    def subtree(self):
        '''Returns the type of self 

        :return: type of self 
        :rtype: Tree
        '''
        return type(self)(lsq_funcs=self.lsq_funcs,
                          lsq_method=self.lsq_method,
                          deep=self.deep if self.deep is None \
                                         else self.deep - 1,
                          save_data=self.save_data)

    def __str__(self):
        '''Writing the constructed tree to a string

        :return: A string representation of tree
        :rtype: str
        '''
        if self.y.data is None:
            res = f"ya={self.y_aver} "
        else:
            res = f"y={self.y}, x={self.x}"
        if self.choice.description is not None:
            res += f", if({self.choice.description}) "
        if self.next_trees != []:
            res += "[" + ", ".join(map(str, self.next_trees)) + "]"
        return "{" + res + "}"


class ContinuumDataTree(Tree):
    ''''This is a class of an enhanced decision tree only for continuum data
    '''
    data_type = ContinuumData

    def fit(self, x, y):
        '''Sets the required data format and builds a tree

        :param x: An input parameters
        :type x: list[BaseData]
        :param y: An output parameter
        :type y: Data
        :return: A tree
        :rtype: NoneType
        '''
        x = map(self.convert_data, x)
        y = self.convert_data(y)
        return super().fit(x, y)

    @classmethod
    def convert_data(cls, data):
        '''Checks whether the original data is of the ContinuumData type and if not сonverts to it

        :param data: An original data
        :type data: Any
        :return: Converted or original data
        :rtype: ContinuumData
        '''
        return data if isinstance(data, cls.data_type) else cls.data_type(data)
