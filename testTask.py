# -*- coding: utf-8 -*-
import collections
import types
import operator

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
        oper = operator.lt
    elif start > stop and step < 0:
        oper = operator.gt
    else:
        raise StopIteration

    while oper(current, stop):
            yield current
            current += step


def my_zip(*args):
    """
    Реализация zip
    """
    for i, arg in enumerate(args):
        if not isinstance(arg, collections.Iterable):
            raise TypeError('zip argument #{0} must support iteration'.format(i+1))

    if len(args) == 0:
        return []

    result = []
    iter_list = [iter(arg) for arg in args]
    try:
        while True:
            result.append(tuple([el.next() for el in iter_list]))
    except StopIteration: None

    return result


#list comprehension
def square_list(i_list):
    """
    Возвращает список квадратов чисел
    """
    if not isinstance(i_list, types.ListType):
            raise TypeError('i_list arg must by type of List')

    for el in i_list:
        if not isinstance(el, (int, float)):
            raise TypeError('Expect numbers in input list')

    return [x**2 for x in i_list]

def every_second_in_list(i_list):
    """
    Возвращает каждый второй элемент списка
    (наверное, имелось ввиду четные элементы списка)
    """
    if not isinstance(i_list, types.ListType):
            raise TypeError('i_list arg must by type of List')

    for el in i_list:
        if not isinstance(el, (int, float)):
            raise TypeError('Expect numbers in input list')

    return [x for i, x in enumerate(i_list) if i % 2]

def list_comprehension_ex3(i_list):
    """
    Возвращает Квадраты чётных элементов на нечётных позициях
    """
    if not isinstance(i_list, types.ListType):
            raise TypeError('i_list arg must by type of List')

    for el in i_list:
        if not isinstance(el, (int, float)):
            raise TypeError('Expect numbers in input list')

    return [x**2 for i, x in enumerate(i_list) if not i % 2 and x % 2 == 0]