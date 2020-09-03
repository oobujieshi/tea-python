import unittest
import re

from Tea.model import TeaModel


class TestTeaModel(unittest.TestCase):
    class TestRegModel(TeaModel):
        def __init__(self):
            super().__init__()
            self.requestId = "requestID"
            self.items = []
            self.nextMarker = "next"
            self.testNoAttr = "noAttr"
            self.subModel = None
            self.testListStr = ["str", "test"]

    class TestRegSubModel(TeaModel):
        def __init__(self):
            super().__init__()
            self.requestId = "subRequestID"
            self.testInt = 1
            self.test_dict = {'a': 1, 'b': {
                'a': 1, 'b': 2, 'c': '3'}, 'c': '3'}

    class TestModel(TeaModel):
        def __init__(self):
            super().__init__()
            self.a = "a"
            self.b = "b"
            self.c = "c"
            self.d = 0
            self.d = 1
            self.e = None
            self.f = ""
            self.requestId = "requestId"

    def test_validate_required(self):
        tm = TeaModel()
        tm.validate()
        tm.to_map()
        tm.from_map()

        n = tm.validate_required('test', 'prop_name')
        self.assertIsNone(n)

        try:
            tm.validate_required(None, 'prop_name')
            assert False
        except Exception as e:
            self.assertEqual('prop_name is required.', str(e))

    def test_validate_max_length(self):
        tm = TeaModel()
        tm.validate_max_length('test', 'prop_name', 10)

        try:
            tm.validate_max_length('test', 'prop_name', 1)
            assert False
        except Exception as e:
            self.assertEqual('prop_name is exceed max-length: 1', str(e))

    def test_validate_min_length(self):
        tm = TeaModel()
        tm.validate_min_length('test', 'prop_name', 1)

        try:
            tm.validate_min_length('test', 'prop_name', 10)
            assert False
        except Exception as e:
            self.assertEqual('prop_name is less than min-length: 10', str(e))

    def test_validate_pattern(self):
        tm = TeaModel()
        tm.validate_pattern('test', 'prop_name', 't')

        tm.validate_pattern(123.1, 'prop_name', '1')

        try:
            tm.validate_pattern('test', 'prop_name', '1')
            assert False
        except Exception as e:
            self.assertEqual('prop_name is not match: 1', str(e))

    def test_validate_maximum(self):
        tm = TeaModel()
        tm.validate_maximum(1, 10)

        try:
            tm.validate_maximum(10, 1)
            assert False
        except Exception as e:
            self.assertEqual('the number is greater than the maximum', str(e))

    def test_validate_minimum(self):
        tm = TeaModel()
        tm.validate_minimum(10, 1)

        try:
            tm.validate_minimum(1, 10)
            assert False
        except Exception as e:
            self.assertEqual('the number is less than the minimum', str(e))
