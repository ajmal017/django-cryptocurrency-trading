from django.test import TestCase
from django.urls import resolve

from wallet.models import User
class SSOTest(TestCase):
    """
    Test function used for testing the SSO for commento
    """
    def setUp(self):
        self.test_user = User.objects.create_user(username='test@example.com')
        self.test_user.email = 'test@example.com'
        self.test_user.set_password('123lalala321')
        self.test_user.save()

    def test_not_signed_on_sso(self):
        found = resolve('/blog/sso')
        response = self.client.get('/blog/sso')

        self.assertEqual(found.view_name, 'commento_sso.views.SingleSignOnView')
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/index')

    def test_invalid_hmac(self):
        token=b'566169446550756c614d65'
        hmac=b'fa551e1029498f06805417afcaf3649d'
        self.client.login(username='test@example.com', password='123lalala321')
        response = self.client.get('/blog/sso', {'token': token, 'hmac': hmac})

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/index')

    def test_valid_hmac(self):
        token = b'566169446550756c614d65'
        hmac = b'406d0a99d75482d2cd8feaada47c081f6ba48559fc27f19d76d876c8beb44071'
        self.client.login(username='test@example.com', password='123lalala321')
        response = self.client.get('/blog/sso', {'token': token, 'hmac': hmac})

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response,
            'https://commento.io/api/oauth/sso/callback',
            fetch_redirect_response=False
        )
