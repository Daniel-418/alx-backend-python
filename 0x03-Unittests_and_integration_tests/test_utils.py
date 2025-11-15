#!/usr/bin/env python3
from parameterized import parameterized
import unittest
from unittest.mock import patch, MagicMock
import utils
from typing import (
    Mapping,
    Sequence,
    Dict,
)


class TestAccessNestedMap(unittest.TestCase):
    @parameterized.expand(
        [
            ({"a": 1}, ("a",), 1),
            ({"a": {"b": 2}}, ("a",), {"b": 2}),
            ({"a": {"b": 2}}, ("a", "b"), 2),
        ]
    )
    def test_access_nested_map(
        self, nested_map: Mapping, path: Sequence, result: Sequence
    ):
        """
        Tests input and output
        """
        self.assertEqual(
            utils.access_nested_map(nested_map=nested_map, path=path), result
        )

    @parameterized.expand([({}, ("a")), ({"a", 1}, ("a", "b"))])
    def test_access_nested_map_exception(self, nested_map: Mapping, path: Sequence):
        """
        Test the errors the function raises
        """
        with self.assertRaises(KeyError):
            utils.access_nested_map(nested_map=nested_map, path=path)


class TestGetJson(unittest.TestCase):
    @parameterized.expand(
        [
            ("http://example.com", {"payload": True}),
            ("http://holberton.io", {"payload": True}),
        ]
    )
    @patch("utils.get_json")
    def test_get_json(self, url: str, result: Dict, mocked_object: MagicMock):
        mocked_object.return_value = result
        self.assertEqual(utils.get_json(url), result)
        mocked_object.assert_called_once()


class TestMemoize(unittest.TestCase):
    """
    Tests the memoize method in utils
    """

    def test_memoize(self):
        class TestClass:
            def a_method(self):
                return 42

            @utils.memoize
            def a_property(self):
                return self.a_method()

        with patch.object(TestClass, "a_method", return_value=42) as mock_method:
            obj = TestClass()

            result_1 = obj.a_property
            result_2 = obj.a_property

            self.assertEqual(result_1, 42)
            self.assertEqual(result_2, 42)
            mock_method.assert_called_once()
