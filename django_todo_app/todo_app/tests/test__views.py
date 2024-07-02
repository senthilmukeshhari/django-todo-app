from django.test import TestCase, Client
from django.urls import reverse
from todo_app.models import User, TodoList

class TestViews(TestCase):
    

    def setUp(self):
        self.client = Client()
        self.home_url = reverse('home')
        self.home_template = 'todo_app/home.html'

        self.add_item_url = reverse('add-item')
        self.add_item_template = 'todo_app/add_items.html'

        self.edit_item_url = reverse('edit-item', args=[1])
        self.edit_item_template = 'todo_app/edit_item.html'

        self.delete_item_url = reverse('delete-item', args=[1])

        self.username_validate_url = reverse('validate-username')
        self.email_validate_url = reverse('validate-email')

        self.signup_url = reverse('signup')
        self.signup_template = 'todo_app/signup.html'

        self.login_url = reverse('login')
        self.login_template = 'todo_app/login.html'

        self.edit_profile_url = reverse('edit-profile')
        self.edit_profile_template = 'todo_app/edit_profile.html'

        self.logout_url = reverse('logout')

        self.testuser = User.objects.create( username='testuser', email='testuser@gmail.com' )
        self.testuser.set_password('testuser')
        self.testuser.save()



    def test_signup_GET(self):
        response = self.client.get(self.signup_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, self.signup_template)


    def test_signup_without_data_POST(self):
        response = self.client.post(self.signup_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, self.signup_template)


    def test_signup_with_data_POST(self):
        response = self.client.post(self.signup_url, {
            'username' : 'testuser1',
            'email' : 'testuser1@gmail.com',
            'password' : 'testuser1',
        })
        test_user1 = User.objects.get(id=2)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(test_user1.username, 'testuser1')
        self.assertEqual(test_user1.email, 'testuser1@gmail.com')
        self.assertEqual(test_user1.profile_img.url, '/media/profile_images/default_user.png')
        self.assertRedirects(response, expected_url=self.login_url)

        
    def test_username_validate_without_data_POST(self):
        response = self.client.post(self.username_validate_url)
        self.assertEqual(response.status_code, 200)


    def test_username_validate_with_data_POST(self):
        # Test : If Username has exsist
        response = self.client.post(self.username_validate_url, {
            'username' : 'testuser1'
        })
        self.assertEqual(response.status_code, 200)
        # Test : If Username is doesn't exssist
        response = self.client.post(self.username_validate_url, {
            'username' : 'testuser'
        })
        self.assertEqual(response.status_code, 200)


    def test_email_validate_without_data_POST(self):
        response = self.client.post(self.email_validate_url)
        self.assertEqual(response.status_code, 200)


    def test_email_validate_with_data_POST(self):
        # Test : If Email has exsist
        response = self.client.post(self.email_validate_url, {
            'email' : 'testuser@gmail.com'
        })
        self.assertEqual(response.status_code, 200)
        # Test : If Email doesn't exsist
        response = self.client.post(self.email_validate_url, {
            'email' : 'testuser1@gmail.com'
        })
        self.assertEqual(response.status_code, 200)
        

    def test_login_GET(self):
        response = self.client.get(self.login_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, self.login_template)
        # Test : Already Login
        self.client.login(username='testuser', password='testuser')
        response = self.client.get(self.login_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, expected_url=self.home_url)


    def test_login_without_data_POST(self):
        response = self.client.post(self.login_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, self.login_template)


    def test_login_with_valid_data_POST(self):
        # Test : valid Username and Password
        response = self.client.post(self.login_url, {
            'username' : 'testuser',
            'password' : 'testuser'
        })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, expected_url=self.home_url)


    def test_login_with_invaild_data_POST(self):
        # Test : Invalid Username and Password
        response = self.client.post(self.login_url, {
            'username' : 'testuser',
            'password' : 'testuser1'
        })
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, self.login_template)

    
    def test_logout_alraady_login_GET(self):
        # Test : Already Login
        self.client.login(username='testuser', password='testuser')
        response = self.client.get(self.logout_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, expected_url=self.login_url)


    def test_logout_not_login_GET(self):
        # Test : Not Login
        response = self.client.get(self.logout_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, expected_url="/login?next=/logout")


    def test_home_GET(self):
        # Test : Already Login
        self.client.login(username='testuser', password='testuser')
        response = self.client.get(self.home_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, self.home_template)
        # Test : Not Login
        self.client.logout()
        response = self.client.get(self.home_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, expected_url='/login?next=/')

        
    def test_add_item_GET(self):
        # Test : Already Login
        self.client.login(username='testuser', password='testuser')
        response = self.client.get(self.add_item_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, self.add_item_template)
        # Test : Not Login
        self.client.logout()
        response = self.client.get(self.add_item_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, expected_url='/login?next=/add-item')

    
    def test_add_item_with_data_POST(self):
        # Test : Already Login
        self.client.login(username='testuser', password='testuser')
        # Test : With Data
        response = self.client.post(self.add_item_url, {
            'title' : 'test title',
            'desc' : 'test description',
            'is_completed' : 'on'
        })

        test_item = TodoList.objects.get(id=1)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(test_item.username.username, 'testuser')
        self.assertEqual(test_item.title, 'test title')
        self.assertEqual(test_item.description, 'test description')
        self.assertEqual(test_item.is_completed, True)
        self.assertRedirects(response, expected_url=self.home_url)

        # Test : Not Login
        self.client.logout()
        response = self.client.post(self.add_item_url, {
            'title' : 'test title',
            'desc' : 'test description',
            'is_completed' : 'on'
        })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, expected_url='/login?next=/add-item')


    def test_add_item_without_data_POST(self):
        # Test : Already Login
        self.client.login(username='testuser', password='testuser')
        # Test : Without Data
        response = self.client.post(self.add_item_url)
        test_item = TodoList.objects.filter(username=self.testuser)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(test_item.count(), 0)
        self.assertRedirects(response, expected_url=self.home_url)

        # Test : Not Login
        self.client.logout()
        response = self.client.post(self.add_item_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, expected_url='/login?next=/add-item')

    
    def test_edit_item_with_id_GET(self):
        # Tesst : Already Login
        self.client.login(username='testuser', password='testuser')
        TodoList.objects.create(
            username = self.testuser,
            title = 'test title'
        )
        response = self.client.get(self.edit_item_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, self.edit_item_template)

        # Tesst : Not Login
        self.client.logout()
        response = self.client.get(self.edit_item_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, expected_url='/login?next=/edit-item/1')

    
    def test_edit_item_with_data_POST(self):
        # Tesst : Already Login
        self.client.login(username='testuser', password='testuser')
        TodoList.objects.create(
            username = self.testuser,
            title = 'test title'
        )
        response = self.client.post(self.edit_item_url, {
            'title' : 'test title',
            'desc' : 'update the test description'
        })
        test_item = TodoList.objects.get(id=1)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(test_item.title, 'test title')
        self.assertEqual(test_item.description, 'update the test description')
        self.assertEqual(test_item.is_completed, False)
        self.assertRedirects(response, expected_url=self.home_url)

         # Tesst : Not Login
        self.client.logout()
        response = self.client.post(self.edit_item_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, expected_url='/login?next=/edit-item/1')

    
    def test_edit_item_without_data_POST(self):
        # Tesst : Already Login
        self.client.login(username='testuser', password='testuser')
        TodoList.objects.create(
            username = self.testuser,
            title = 'test title'
        )
        response = self.client.post(self.edit_item_url)
        test_item = TodoList.objects.get(id=1)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(test_item.title, 'test title')
        self.assertEqual(test_item.description, None)
        self.assertEqual(test_item.is_completed, False)
        self.assertRedirects(response, expected_url=self.home_url)

        # Tesst : Not Login
        self.client.logout()
        response = self.client.post(self.edit_item_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, expected_url='/login?next=/edit-item/1')


    def test_delete_item_GET(self):
        # Test : Already Login
        self.client.login(username='testuser', password='testuser')
        response = self.client.get(self.delete_item_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, expected_url=self.home_url)

        # Test : Not Login
        self.client.logout()
        response = self.client.get(self.delete_item_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, expected_url='/login?next=/delete-item/1')


    def test_delete_item_with_id_POST(self):
        # Test : Already Login
        self.client.login(username="testuser", password="testuser")
        TodoList.objects.create(
            username = self.testuser,
            title = "test title",
        )
        response = self.client.post(self.delete_item_url)
        todo_items = TodoList.objects.filter(username=self.testuser).count()
        self.assertEqual(response.status_code, 302)
        self.assertEqual(todo_items, 0)
        self.assertRedirects(response, expected_url=self.home_url)

        # Test : Not Login
        self.client.logout()
        response = self.client.post(self.delete_item_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, expected_url="/login?next=/delete-item/1")


    def test_delete_item_without_id_POST(self):
        # Test : Already Login
        self.client.login(username="testuser", password="testuser")
        response = self.client.post('/delete-item/')
        self.assertEqual(response.status_code, 404)

        # Test : Not Login
        self.client.logout()
        response = self.client.post(self.delete_item_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, expected_url="/login?next=/delete-item/1")

    