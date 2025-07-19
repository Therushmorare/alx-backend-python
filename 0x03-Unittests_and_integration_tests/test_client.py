#!/usr/bin/env python3
import unittest
from unittest.mock import patch, PropertyMock
from parameterized import parameterized
from client import GithubOrgClient
from fixtures import org_payload, repos_payload, expected_repos, apache2_repos

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
        """Test public_repos returns repo names from mocked payload"""
        # Use popular repos as mock data
        mock_payload = [
            {'name': 'tensorflow'},
            {'name': 'react'},
            {'name': 'linux'}
        ]
        mock_get_json.return_value = mock_payload

        # Patch _public_repos_url
        with patch('client.GithubOrgClient._public_repos_url', new_callable=PropertyMock) as mock_url:
            mock_url.return_value = "https://api.github.com/orgs/test_org/repos"

            client = GithubOrgClient("test_org")
            result = client.public_repos()

            self.assertEqual(result, ['tensorflow', 'react', 'linux'])
            mock_get_json.assert_called_once()
            mock_url.assert_called_once()

class TestGithubOrgClient(unittest.TestCase):

    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False),
    ])
    def test_has_license(self, repo, license_key, expected):
        """Test that has_license returns correct boolean based on license key"""
        client = GithubOrgClient("test_org")
        self.assertEqual(client.has_license(repo, license_key), expected)

org_payload = {"login": "google", "url": "https://api.github.com/orgs/google"}
repos_payload = [
    {"name": "repo1", "license": {"key": "apache-2.0"}},
    {"name": "repo2", "license": {"key": "mit"}},
    {"name": "repo3", "license": {"key": "apache-2.0"}},
]
expected_repos = ["repo1", "repo2", "repo3"]
apache2_repos = ["repo1", "repo3"]

@parameterized_class([
    {
        "org_payload": org_payload,
        "repos_payload": repos_payload,
        "expected_repos": expected_repos,
        "apache2_repos": apache2_repos,
    }
])
class TestIntegrationGithubOrgClient(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.get_patcher = patch("requests.get")
        mock_get = cls.get_patcher.start()

        def side_effect(url):
            mock_response = MagicMock()
            if url == "https://api.github.com/orgs/google":
                mock_response.json.return_value = cls.org_payload
            elif url == "https://api.github.com/orgs/google/repos":
                mock_response.json.return_value = cls.repos_payload
            return mock_response

        mock_get.side_effect = side_effect

    @classmethod
    def tearDownClass(cls):
        cls.get_patcher.stop()

    def test_public_repos(self):
        from client import GithubOrgClient
        client = GithubOrgClient("google")
        self.assertEqual(client.public_repos(), self.expected_repos)

    def test_public_repos_with_license(self):
        from client import GithubOrgClient
        client = GithubOrgClient("google")
        self.assertEqual(client.public_repos(license="apache-2.0"), self.apache2_repos)

@parameterized_class([
    {
        "org_payload": {
            "login": "google",
            "url": "https://api.github.com/orgs/google"
        },
        "repos_payload": [
            {"name": "repo1", "license": {"key": "apache-2.0"}},
            {"name": "repo2", "license": {"key": "mit"}},
            {"name": "repo3", "license": {"key": "apache-2.0"}},
        ],
        "expected_repos": ["repo1", "repo2", "repo3"],
        "apache2_repos": ["repo1", "repo3"]
    }
])
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """Integration tests for GithubOrgClient"""

    @classmethod
    def setUpClass(cls):
        """Start patching requests.get and mock API responses."""
        cls.get_patcher = patch("requests.get")
        mock_get = cls.get_patcher.start()

        def side_effect(url):
            mock_response = MagicMock()
            if url == "https://api.github.com/orgs/google":
                mock_response.json.return_value = cls.org_payload
            elif url == "https://api.github.com/orgs/google/repos":
                mock_response.json.return_value = cls.repos_payload
            return mock_response

        mock_get.side_effect = side_effect

    @classmethod
    def tearDownClass(cls):
        """Stop patching requests.get"""
        cls.get_patcher.stop()

    def test_public_repos(self):
        """Test public_repos method returns all repository names"""
        from client import GithubOrgClient
        client = GithubOrgClient("google")
        self.assertEqual(client.public_repos(), self.expected_repos)

    def test_public_repos_with_license(self):
        """Test public_repos method filters by license correctly"""
        from client import GithubOrgClient
        client = GithubOrgClient("google")
        self.assertEqual(client.public_repos(license="apache-2.0"), self.apache2_repos)

if __name__ == "__main__":
    unittest.main()
