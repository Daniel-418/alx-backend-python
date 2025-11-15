#!/usr/bin/env python3
from parameterized import parameterized
import unittest
import utils
from typing import (
    Mapping,
    Sequence,
)


class TestAccessNestedMap(unittest.TestCase):
    @parameterized.expand(
        [
            ({"a": 1}, ("a",), 1),
            ({"a": {"b": 2}}, ("a",), {"b": 2}),
            ({"a": {"b": 2}}, ("a", "b"), 2),
        ]
    )
    def test_acess_nested_map(
        self, nested_map: Mapping, path: Sequence, result: Sequence
    ):
        """
        Tests input and output
        """
        self.assertEqual(
            utils.access_nested_map(nested_map=nested_map, path=path), result
        )
