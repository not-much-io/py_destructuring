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
    def types_seq(first_type: type,                 # With type hint
                  cd: ("obj1", "obj2", "obj3"),     # Destructuring
                  regular_param,                    # Regular positional argument
                  *args) -> list:                   # Variable number arguments + return type (unlikely to be affected)
        cd_types = [type(o) for o in (obj1, obj2, obj3)]
        return [first_type] + cd_types + [regular_param] + list(args)

    def test_tuple_advanced(self):
        # Tests if:
        #   Type hints continue working.
        #   Destructuring works in random position
        #   Regular positional parameters are unaffected
        #   Variable number arguments are unaffected
        try:
            res = self.types_seq(tuple,
                                 self.object_dict,
                                 list,
                                 int, str, str)
        except NameError:
            raise AssertionError("A NameError was raised, destructured vars"
                                 " were probably not made available to function scope")
        self.assertEqual(res, [tuple,
                               int, str, FunctionType,
                               list,
                               int, str, str])

    # ToDo test destructuring with dictionary expression

if __name__ == "__main__":
    main()

