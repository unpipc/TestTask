# -*- coding: utf-8 -*-

import testTask
import types
from unittest import TestCase


class InfiniteYieldTest(TestCase):
    def test_ret_generator_type(self):
        gen = testTask.infinite_yield()
        self.assertIsInstance(gen, types.GeneratorType, 'infinite_yield() return not GeneratorType')

    def test_ret_same_value(self):
        gen = testTask.infinite_yield()
        val1 = gen.next()
        val2 = gen.next()
        self.assertEqual(val1, val2, 'Generator return different values')


class MyXrangeTest(TestCase):
    def test_exception_on_non_int_start_value(self):
        gen = testTask.my_xrange(1.0, 5)
        self.assertRaises(TypeError, gen.next)

    def test_exception_on_non_int_stop_value(self):
        gen = testTask.my_xrange(1, 5.0)
        self.assertRaises(TypeError, gen.next)

    def test_exception_on_non_int_step_value(self):
        gen = testTask.my_xrange(1, 5, 1.0)
        self.assertRaises(TypeError, gen.next)

    def test_exception_on_zero_step_value(self):
        gen = testTask.my_xrange(1, 5, 0)
        self.assertRaises(ValueError, gen.next)

    def test_correct_values_generated_1(self):
        correct_vals = []
        gen_vals = []
        for val in xrange(1, 5):
            correct_vals.append(val)
        for val in testTask.my_xrange(1, 5):
            gen_vals.append(val)

        self.assertEqual(correct_vals, gen_vals, 'Generator return incorrect values {0} expect {1}'
                         .format(gen_vals, correct_vals))

    def test_correct_values_generated_2(self):
        correct_vals = []
        gen_vals = []
        for val in xrange(5, 1, -1):
            correct_vals.append(val)
        for val in testTask.my_xrange(5, 1, -1):
            gen_vals.append(val)

        self.assertEqual(correct_vals, gen_vals, 'Generator return incorrect values {0} expect {1}'
                         .format(gen_vals, correct_vals))

    def test_correct_values_generated_3(self):
        correct_vals = []
        gen_vals = []
        for val in xrange(1, 5, -1):
            correct_vals.append(val)
        for val in testTask.my_xrange(1, 5, -1):
            gen_vals.append(val)

        self.assertEqual(correct_vals, gen_vals, 'Generator return incorrect values {0} expect {1}'
                         .format(gen_vals, correct_vals))

    def test_correct_values_generated_4(self):
        correct_vals = []
        gen_vals = []
        for val in xrange(5, 1):
            correct_vals.append(val)
        for val in testTask.my_xrange(5, 1):
            gen_vals.append(val)

        self.assertEqual(correct_vals, gen_vals, 'Generator return incorrect values {0} expect {1}'
                         .format(gen_vals, correct_vals))


class MyZipTest(TestCase):
    def test_exception_on_non_iterable_value(self):
        self.assertRaises(TypeError, testTask.my_zip, 123)

    def test_zip_without_args(self):
        retval = testTask.my_zip()
        self.assertTrue(isinstance(retval, types.ListType) and len(retval) == 0)

    def test_zip_with_one_arg(self):
        retval = testTask.my_zip('123')
        self.assertTrue(isinstance(retval, types.ListType) and len(retval) == 3 and
            isinstance(retval[0], types.TupleType) and len(retval[0]) == 1)

    def test_zip_with_several_args(self):
        retval = testTask.my_zip('123', '12345')
        self.assertTrue(isinstance(retval, types.ListType) and len(retval) == 3 and
            isinstance(retval[0], types.TupleType) and len(retval[0]) == 2)