# -*- coding: utf-8 -*-


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
