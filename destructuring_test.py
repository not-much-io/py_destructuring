from destructuring import destructure
from unittest import TestCase, main
from types import FunctionType


class TestDestructuring(TestCase):
    simple_dict = {"key1": 10,
                   "key2": 1}

    @staticmethod
    @destructure
    def sum_key1_and_key2(d: ('key1', 'key2')):
        return key1 + key2

    def test_tuple_simple(self):
        val_sum = self.sum_key1_and_key2(self.simple_dict)
        self.assertEqual(val_sum,
                         11)

    object_dict = {"obj1": 10,
                   "obj2": "Test String",
                   "obj3": lambda x: x}

    @staticmethod
    @destructure
    def types_seq(first_type: type, cd: ("obj1", "obj2", "obj3"), regular_param, *args) -> list:
        cd_types = [type(o) for o in (obj1, obj2, obj3)]
        return [first_type] + cd_types + [regular_param] + list(args)

    def test_tuple_advanced(self):
        # Tests if:
        #   Type hints continue working.
        #   Destructuring works in random position
        #   Regular positional parameters are unaffected
        #   Variable number arguments are unaffected
        res = self.types_seq(tuple,             # First type, with type hint
                             self.object_dict,  # Dictionary
                             list,              # Regular positional parameter
                             int, str, str)     # Variable number arguments
        self.assertEqual(res, [tuple,                   # First type, with type hint
                               int, str, FunctionType,  # Destructured dictionary
                               list,                    # Regular positional argument
                               int, str, str])          # From variable number arguments

    # ToDo test destructuring with dictionary expression

if __name__ == "__main__":
    main()

