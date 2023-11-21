"""Tests for the django admin modifications
"""

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import Client


class AdminSiteTests(TestCase):
    """tests for django admin.
    """
    # as named. This runs before each test.
    def setUp(self):
        """
        Create user and client
        """

        self.client = Client()
        # We create one admin user to test with
        self.admin_user = get_user_model().objects.create_superuser(
            email="admin@example.com",
            password = "testpass123",
        )

        # this line forces login using the sudo user
        self.client.force_login(self.admin_user)
        # as well as one normal user
        self.user = get_user_model().objects.create_user(
            email = 'user@example.com',
            password = 'testpass123',
            name = 'Test User'
        )

    def test_users_lists(self):
        """
        Test that users are listed on page.
        """

        url = reverse('admin:core_user_changelist')
        res = self.client.get(url)
        self.assertContains(res, self.user.name)
        self.assertContains(res, self.user.email)

    def test_edit_user_page(self):
        """
        Tests that the edit user page works
        """

        url = reverse('admin:core_user_change', args=[self.user.id])
        res = self.client.url(url)

        self.assertEqual(res.status_code, 200)

    def test_edit_user_page(self):
        """
        Test that the edit user page works
        """

        url = reverse('admin:core_user_change', args=[self.user.id])
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)

    def test_add_user_page(self):
        """
        Tests that the create user page works
        """

        url = reverse('admin:core_user_add') # no args since we're creating a new user
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)