#!/usr/bin/env python3
"""
Tests the utils module
"""
from parameterized import parameterized
import unittest
from unittest.mock import patch, MagicMock
import client
from typing import (
    Mapping,
    Sequence,
    Dict,
)

class TestGithubOrgClient(unittest.TestCase):
    """
    class to test the client module that exits in this folder
    """
    @parameterized.expand(
        [
            ('google', {"name": "Google", "id": 1}),
            ('abc', {"name": "ABC", "id": 2}),
        ]
    )
    @patch('client.get_json')
    def test_org(self, org_name: str, result: dict, mocked_object: MagicMock):
        """
        Test to test that the org is called correctly
        """
        mocked_object.return_value = result
        org = client.GithubOrgClient(org_name)
        self.assertEqual(org.org, result)
        mocked_object.assert_called_once_with(client.GithubOrgClient.ORG_URL.format(org=org_name))
