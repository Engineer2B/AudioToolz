__author__ = 'Boris Breuer'
import inspect


def assert_str(input_str):
    assert isinstance(input_str, str), \
        'Incorrect value "%s", it should be a string!' % input_str


def assert_int_or_float(input_number):
    assert (isinstance(input_number, float) or isinstance(input_number, int)), \
        'Incorrect value "%s", it should be a float or an integer!' % input_number


def str_name(variable):
    callers_local_vars = inspect.currentframe().f_back.f_locals.items()
    print callers_local_vars
    return [var_name for var_name, var_val in callers_local_vars if var_val is variable]
