# -*- coding: utf-8 -*-
import collections

def infinite_yield(ret_val=1):
    """
    «вечный» генератор, который выдаёт всё время одно значение;
    """
    while True:
        yield ret_val


def my_xrange(start, stop, step=1):
    """
    Реализация xrange
    """
    for var, var_name in ((start, 'start'), (stop, 'stop'), (step, 'step')):
        if not isinstance(var, int):
            raise TypeError('integer "{0}" argument expected, got {1}.'.format(var_name, type(start).__name__))

    if step == 0:
        raise ValueError('arg 3 must not be zero')

    current = start
    if start < stop and step > 0:
        while current < stop:
            yield current
            current += step
    elif start > stop and step < 0:
        while current > stop:
            yield current
            current += step
    else:
        raise StopIteration


def my_zip(*args):
    """
    Реализация zip
    """
    for i, arg in enumerate(args):
        if not isinstance(arg, collections.Iterable):
            raise TypeError('zip argument #{0} must support iteration'.format(i+1))

    if len(args) == 0:
        return list()

    if len(args) == 1:
        result = []
        result.append(tuple(args[0]))
        return result

    result = []
    i = 0
    while i < len(min(args, key=len)):
        element = []
        for arg in args:
            element.append(arg[i])
        result.append(tuple(element))
        i += 1

    return result