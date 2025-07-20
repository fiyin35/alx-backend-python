#!/usr/bin/env python3
"""Unit tests for the GithubOrgClient class."""

import unittest
from unittest.mock import patch, PropertyMock
from parameterized import parameterized, parameterized_class
from client import GithubOrgClient

from client import GithubOrgClient
from fixtures import TEST_PAYLOAD

from fixtures import org_payload, repos_payload, expected_repos, apache2_repos


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
    def test_has_license(self,repo: Dict[str, Dict[str, str]],license_key: str,expected: bool) -> None:
        """Test that has_license returns True only when license matches."""
        result = GithubOrgClient.has_license(repo, license_key)
        self.assertEqual(result, expected)



@parameterized_class([
    {
        "org_payload": org_payload,
        "repos_payload": repos_payload,
        "expected_repos": expected_repos,
        "apache2_repos": apache2_repos,
    }
])
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """Integration tests for GithubOrgClient.public_repos"""

    @classmethod
    def setUpClass(cls) -> None:
        """Start patcher for requests.get with correct side effects."""
        cls.get_patcher = patch("requests.get")
        mock_get = cls.get_patcher.start()

        # Setup side effect for multiple sequential calls
        mock_get.side_effect = [
            MockResponse(cls.org_payload),
            MockResponse(cls.repos_payload)
        ]

    @classmethod
    def tearDownClass(cls) -> None:
        """Stop patcher."""
        cls.get_patcher.stop()

    def test_public_repos(self) -> None:
        """Test that public_repos returns expected repo names."""
        client = GithubOrgClient("test")
        self.assertEqual(client.public_repos(), self.expected_repos)

    def test_public_repos_with_license(self) -> None:
        """Test that public_repos filters by license key correctly."""
        client = GithubOrgClient("test")
        self.assertEqual(
            client.public_repos(license="apache-2.0"),
            self.apache2_repos
        )
    
    def test_public_repos(self):
        """Test public_repos without license filter"""
        result = self.client.public_repos()
        self.assertEqual(result, self.expected_repos)



class MockResponse:
    """Mock response object to mimic requests.get().json()."""
    def __init__(self, json_data):
        self._json_data = json_data

    def json(self):
        return self._json_data


