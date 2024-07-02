from django.test import SimpleTestCase
from django.urls import reverse, resolve
from todo_app import views


class TestUrls(SimpleTestCase):

    def test_home_resolves(self):
        url = reverse('home')
        self.assertEqual(resolve(url).func, views.home)

    def test_add_item_resolves(self):
        url = reverse('add-item')
        self.assertEqual(resolve(url).func, views.add_item)

    def test_delete_item_resolves(self):
        url = reverse('delete-item', args=[1])
        self.assertEqual(resolve(url).func, views.delete_item)

    def test_edit_item_resolves(self):
        url = reverse('edit-item', args=[1])
        self.assertEqual(resolve(url).func, views.edit_item)

    def test_edit_profile_resolves(self):
        url = reverse('edit-profile')
        self.assertEqual(resolve(url).func, views.edit_profile)

    def test_username_validate_resolves(self):
        url = reverse('validate-username')
        self.assertEqual(resolve(url).func.view_class, views.UsernameValidation)

    def test_email_validate_resolves(self):
        url = reverse('validate-email')
        self.assertEqual(resolve(url).func.view_class, views.EmailValidation)

    def test_signup_resolves(self):
        url = reverse('signup')
        self.assertEqual(resolve(url).func, views.signup_user)

    def test_login_resolves(self):
        url = reverse('login')
        self.assertEqual(resolve(url).func, views.login_user)

    def test_logout_resolves(self):
        url = reverse('logout')
        self.assertEqual(resolve(url).func, views.logout_user)
    