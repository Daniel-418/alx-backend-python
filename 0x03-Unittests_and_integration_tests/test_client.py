#!/usr/bin/env python3
"""
Tests the utils module
"""
from parameterized import parameterized
import unittest
from unittest.mock import patch, MagicMock, PropertyMock
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

    def test_public_repos_url(self):
        """
        Test to test the public repos urls
        """
        known_org_payload = {"repos_url": "https://api.github.com/orgs/test/repos"}
        with patch("client.GithubOrgClient.org", 
                   new_callable=PropertyMock,
                   return_value=known_org_payload) as mock_method:
            dummy = client.GithubOrgClient('google')

            result_url = dummy._public_repos_url

            self.assertEqual(result_url, known_org_payload['repos_url'])
            mock_method.assert_called_once()

    @patch('client.get_json')
    def test_public_repos(self, mocked_object: MagicMock):
        """
        Test to test the public repos url method
        """
        mocked_object.return_value = [
            {"name": "repo-one"},
            {"name": "repo-two"},
            {"name": "repo-three"},
        ]
        with patch('client.GithubOrgClient._public_repos_url', 
                   new_callable=PropertyMock,
                   return_value="https://api.github.com/orgs/test/repos") as mocked_method:
            dummy = client.GithubOrgClient("google")
            self.assertEqual(dummy.public_repos(), ["repo-one", "repo-two", "repo-three"])
            mocked_method.assert_called_once()
            mocked_object.assert_called_once()
            mocked_object.assert_called_once_with("https://api.github.com/orgs/test/repos")
            
