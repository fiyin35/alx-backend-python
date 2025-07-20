#!/usr/bin/env python3
"""Unit tests for the GithubOrgClient class."""

import unittest
from unittest.mock import patch, PropertyMock
from parameterized import parameterized
from client import GithubOrgClient

from typing import Dict

class TestGithubOrgClient(unittest.TestCase):
    """Test cases for GithubOrgClient"""

    @parameterized.expand([
        ("google",),
        ("abc",),
    ])
    @patch("client.get_json")
    def test_org(self, org_name: str, mock_get_json) -> None:
        """Test that GithubOrgClient.org returns expected data from get_json."""
        expected = {"name": org_name, "info": "test"}
        mock_get_json.return_value = expected

        client = GithubOrgClient(org_name)
        self.assertEqual(client.org, expected)
        mock_get_json.assert_called_once_with(
            f"https://api.github.com/orgs/{org_name}"
        )

    def test_public_repos(self) -> None:
        """Test that _public_repos_url returns the correct repos_url from org payload."""
        test_url = "https://api.github.com/orgs/test/repos"

        with patch.object(
            GithubOrgClient,
            "org",
            new_callable=PropertyMock
        ) as mock_org:
            mock_org.return_value = {"repos_url": test_url}
            client = GithubOrgClient("test")
            result = client._public_repos_url
            self.assertEqual(result, test_url)
    

    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False),
    ])
    def test_has_license(
        self,
        repo: Dict[str, Dict[str, str]],
        license_key: str,
        expected: bool
    ) -> None:
        """Test that has_license returns True only when license matches."""
        result = GithubOrgClient.has_license(repo, license_key)
        self.assertEqual(result, expected)

