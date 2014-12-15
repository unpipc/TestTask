# -*- coding: utf-8 -*-
import collections
import types

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

    #REVIEW: В целом, стандартный подход.
    # В качестве развития можно попробовать унифицировать и упростить код с помощью 
    # функций-операторов: operator.le, operator.gt
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
    #REVIEW: Функция не работает с генераторами. В принципе, это уже заметно 
    за счёт инструкции len().
    """
    for i, arg in enumerate(args):
        #REVIEW: Хотя, судя по всему, намерение использовать любые Iterable всё же было:

        if not isinstance(arg, collections.Iterable):
            raise TypeError('zip argument #{0} must support iteration'.format(i+1))

    if len(args) == 0:
        #REVIEW: Этот случай вырожденный; вроде бы незачем повторять код, когда 
        # всё равно далее надо будет писать код для общего случая.
        return list()

    if len(args) == 1:
        #REVIEW: тоже вырожденный случай.
        result = []
        result.append(tuple(args[0]))
        return result #REVIEW: В любом случае, проще было бы написать return [(args[0],)]

    result = []
    i = 0
    #REVIEW: В питоне принято использовать enumerate() для нумерации элементов Iterable,
    # или range()/xrange() для организации счётчиков. for i in xrange(len(min(args, key=len))):
    while i < len(min(args, key=len)):
        element = []
        for arg in args:
            element.append(arg[i])
        result.append(tuple(element))
        #REVIEW: массив заполнять всё же лучше с помощью list comprehension. Здесь вроде бы ничего
        # не мешает.
        i += 1

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
