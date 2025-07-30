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


class BaseData(metaclass=abc.ABCMeta):
    '''This is a data class intended for implementing common constructor method and basic methods necessary for working with data
    '''
    def __init__(self, data, name=""):
        """Constructor method
        """
        if isinstance(data, BaseData):
            self.data = data.data
            self.name = data.name
        else:
            self.data = np.array(data)
            self.name = name

    def __getitem__(self, key):
        '''Returns an object of the same type as the self but with data after the slice

        :return: An object with data after the slice
        :rtype: BaseData
        '''
        return type(self)(self.data.__getitem__(key),
                          name=self.name)

    def __len__(self):
        '''Calcs length of a self.data

        :return: Length of a self.data
        :rtype: str
        '''
        return len(self.data)

    def __str__(self):
        '''Returns a string representation of a self.data

        :return: A string representation of a self.data
        :rtype: str
        '''
        return str(self.data)

    def __repr__(self):
        '''Returns a printable representation of self.data

        :return: A printable representation
        :rtype: str
        '''
        return repr(self.data)

    @abc.abstractmethod
    def choose(self, y, my_ind):
        '''Chooses slice with the lowest entropy

        :param y: An output parameter
        :type y: Data
        :param my_ind: An index of slice
        :type my_ind: int
        :return: Chosen slice with the lowest entropy
        :rtype: Choice
        '''
        pass

    def clear(self):
        '''Clears self.data
        '''
        self.data = None


class Data(BaseData):
    '''This is a class designed to implement a common method of choose slices for data of different types
    '''
    def choose(self, y, my_ind):
        '''Chooses slice with the lowest entropy

        :param y: An output parameter
        :type y: Data
        :param my_ind: An index of slice
        :type my_ind: int
        :raises ValueError: Called if the length of array of input parameters and output parameter isn't equal
        :return: Chosen slice with the lowest entropy
        :rtype: Choise
        '''
        N, N1 = map(len, (y, self))
        if N != N1:
            raise ValueError("Length of x and y should be equal")        
        if self.variants < 2:
            return Choice(entropy=-1)
        all_sl = ((sl, sum([y[ind].std*np.sum(ind) for ind in sl.indexes]))
                  for sl in self._slice_indexes())
        sl, entropy = min(all_sl, key=lambda x: x[1])

        entropy = y.std - entropy/N

        return self._do_choice(entropy, sl, my_ind)

    @property
    @abc.abstractmethod
    def std(self):
        '''Returns measure of distribution

        :return: A measure of distribution
        :rtype: float
        '''
        pass

    @property
    @abc.abstractmethod
    def average(self):
        '''Finds unique elements

        :return: The average value or the most common element of the unique
        :rtype: float
        '''
        pass

    @property
    @abc.abstractmethod
    def variants(self):
        '''Returns the number of unique elements

        :return: A number of unique elements
        :rtype: float
        '''
        pass

    @abc.abstractmethod
    def _do_choice(self, entropy, sl, my_ind):
        '''Creates an instance of Choice class

        :param entropy: An entropy
        :type entropy: float
        :param sl: Slise
        :type sl: Slice
        :param my_ind: An index of slice
        :type my_ind: int
        :return: An instance of Choice class
        :rtype: Choice
        '''
        pass

    @abc.abstractmethod
    def _slice_indexes(self):
        '''Returns indexes to slice in sorted array

        :return: An indexes to slice
        :rtype: Slice
        '''
        "Indexes to slice in sorted array"
        pass


class ContinuumData(Data):
    '''This is a class designed to work with continuum data
    '''
    def _slice_indexes(self):
        '''Returns indexes to slice in sorted array

        :return: An indexes to slice
        :rtype: Slice
        '''
        vals, rind = np.unique(self.data, return_inverse=True)
        for i in range(len(vals)-1):
            ind = rind <= i
            point = (vals[i] + vals[i+1])/2
            yield Slice(point=point, indexes=[ind, ~ind])

    def _do_choice(self, entropy, sl, my_ind):
        '''Creates an instance of Choice class for slice

        :param entropy: An entropy
        :type entropy: float
        :param sl: Slise
        :type sl: Slice
        :param my_ind: An index of slice
        :type my_ind: int
        :return: An instance of Choice class
        :rtype: Choice
        '''
        aver = sl.point
        return Choice(entropy=entropy,
                      indexes=sl.indexes,
                      function = lambda *x: not(x[my_ind]<aver),
                      description = self.name + " < " + str(aver))

    @functools.cached_property
    def std(self):
        '''Calcs a standard deviation of self.data

        :return: A standard deviation
        :rtype: float
        '''
        return np.std(self.data)

    @functools.cached_property
    def average(self):
        '''Computes the average value of self.data

        :return: An average value
        :rtype: float
        '''
        return np.average(self.data)

    @functools.cached_property
    def variants(self):
        '''Counts the number of unique elements in self.data

        :return: A number of unique elements
        :rtype: float
        '''
        return len(np.unique(self.data))


class DiscreteData(Data):
    '''This is a class designed to work with discrete data
    '''
    @functools.cached_property
    def std(self):
        '''Calcs entropy

        :return: An entropy
        :rtype: float
        '''
        return scipy.stats.entropy(np.unique(self.data,return_counts=True)[1],
                                   base=2)

    @functools.cached_property
    def average(self):
        '''Finds in self.data unique elements and returns the most common one

        :return: The most common element of the unique
        :rtype: float
        '''
        values, counts = np.unique(self.data,return_counts=True)
        return values[np.argmax(counts)]

    def _do_choice(self, entropy, sl, my_ind):
        '''Creates an instance of Choice class

        :param entropy: An entropy
        :type entropy: float
        :param sl: Slise
        :type sl: Slice
        :param my_ind: Index of slice
        :type my_ind: int
        :return: An instance of Choice class
        :rtype: Choice
        '''
        point = sl.point
        return Choice(entropy=entropy,
                      indexes=sl.indexes,
                      function = lambda *x: x[my_ind] != point,
                      description = self.name + " == " + str(point))

    def _slice_indexes(self):
        '''Returns indexes to slice in sorted array

        :return: An indexes to slice
        :rtype: Slice
        '''
        vals, rind = np.unique(self.data, return_inverse=True)
        for i,val in enumerate(vals):
            ind = rind == i
            yield Slice(point=val, indexes=[ind, ~ind])

    @functools.cached_property
    def variants(self):
        '''Returns the number of unique elements

        :return: A number of unique elements
        :rtype: int
        '''
        return len(np.unique(self.data))


class InfoData(BaseData):
    '''This is a class designed to work with info data
    '''
    def choose(self, *args, **kwargs):
        '''Creates an instance of Choice class

        :return: An instance of Choice class
        :rtype: Choice
        '''
        return Choice(entropy=-np.inf)

@dataclasses.dataclass
class Slice:
    '''This is a class of slices, each instance of which stores information about the slice corresponding to it

    :param point: A point relative to which the slice is being made
    :type point: float, optional
    :param indexes: An array of indexes
    :type indexes: list[numpy.ndarray[bool]], optional
    '''
    point: Any
    indexes: list[np.ndarray[bool]]  = None


@dataclasses.dataclass
class Choice:
    '''This is a class intended for storing information about the slices selected for constructing the tree

    :param entropy: An entropy
    :type entropy: float, optional
    :param function: A function
    :type function: Callable, optional
    :param indexes: An array of indexes
    :type indexes: list[numpy.ndarray[bool]], optional
    :param description: A description of the class instance
    :type description: str, optional
    '''
    entropy: float = None
    function: Callable[[Any, ...], bool] = None
    indexes: list[np.ndarray[bool]]  = None
    description: str = None

    def clear(self):
        '''Clears indexes
        '''
        self.indexes = None
