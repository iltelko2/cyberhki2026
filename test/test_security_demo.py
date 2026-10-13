from django.contrib.auth import get_user_model
from django.test import TestCase


class SecurityLoginTest(TestCase):
	def setUp(self):
		self.user = get_user_model().objects.create_user(
			username='demo-user',
			password='test-only-password',
		)

	def test_password_is_stored_as_a_hash_in_the_user_database(self):
		self.user.refresh_from_db()

		self.assertNotEqual(self.user.password, 'test-only-password')
		self.assertTrue(self.user.check_password('test-only-password'))

	def test_login_accepts_known_username_without_checking_password(self):
		response = self.client.post(
			'/security/login/',
			{'username': 'demo-user', 'password': 'wrong-password'},
		)

		self.assertContains(response, 'Welcome, demo-user!')
		self.assertTrue(self.client.session['is_authenticated'])

	def test_login_rejects_unknown_username(self):
		response = self.client.post(
			'/security/login/',
			{'username': 'missing-user', 'password': 'any-password'},
		)

		self.assertContains(response, 'Invalid credentials')
		self.assertNotIn('is_authenticated', self.client.session)
