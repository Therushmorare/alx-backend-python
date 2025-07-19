#!/usr/bin/env python3
import unittest
from unittest.mock import patch, PropertyMock
from parameterized import parameterized
from client import GithubOrgClient


class TestGithubOrgClient(unittest.TestCase):
    """Test the GithubOrgClient class."""
    @parameterized.expand([
        ("google",),
        ("abc",),
    ])
    @patch("client.get_json")
    def test_org(self, org_name, mock_get_json):
        """Test that GithubOrgClient.org returns correct data and calls get_json once."""
        expected = {"login": org_name}
        mock_get_json.return_value = expected

        client = GithubOrgClient(org_name)
        result = client.org

        self.assertEqual(result, expected)
        mock_get_json.assert_called_once_with(f"https://api.github.com/orgs/{org_name}")


class TestGithubOrgClient(unittest.TestCase):

    def test_public_repos_url(self):
        """Test that _public_repos_url returns the correct URL from .org"""
        test_payload = {"repos_url": "https://api.github.com/orgs/google/repos"}

        client = GithubOrgClient("google")

        with patch.object(GithubOrgClient, "org", new_callable=unittest.mock.PropertyMock) as mock_org:
            mock_org.return_value = test_payload
            url = client._public_repos_url
            self.assertEqual(url, test_payload["repos_url"])

class TestGithubOrgClient(unittest.TestCase):

    @patch('client.get_json')
    def test_public_repos(self, mock_get_json):
        """Test GithubOrgClient.public_repos returns the expected list of repo names"""

        # Mock the return value of get_json (simulate the API response)
        mock_payload = [
            {"name": "repo1"},
            {"name": "repo2"},
            {"name": "repo3"}
        ]
        mock_get_json.return_value = mock_payload

        # Instantiate client
        client = GithubOrgClient("test_org")

        # Mock _public_repos_url property to return a dummy URL
        with patch.object(GithubOrgClient, "_public_repos_url", new_callable=PropertyMock) as mock_public_repos_url:
            mock_public_repos_url.return_value = "https://api.github.com/orgs/test_org/repos"

            # Call the property
            repos = client.public_repos

            # Assert the returned list contains repo names as expected
            expected_repos = [repo["name"] for repo in mock_payload]
            self.assertEqual(repos, expected_repos)

            # Assert the mocked _public_repos_url property was called once
            mock_public_repos_url.assert_called_once()

        # Assert get_json was called once with the mocked URL
        mock_get_json.assert_called_once_with("https://api.github.com/orgs/test_org/repos")

if __name__ == "__main__":
    unittest.main()
