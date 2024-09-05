from django.test import TestCase
from django.contrib.auth import get_user_model
from store_app.models import Category
from django.urls import reverse
from django.contrib.auth.models import Permission

class StoreUserRegisterTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user_data = {
            'username': 'admin',
            'email': 'admin@admin.local',
            'password1': 'zaq123ZAQ123',
            'password2': 'zaq123ZAQ123',
        }
        cls.user_broken_data = {
            'username': 'admin',
            'email': 'admin@admin.local',
            'password1': 'zaq123ZAQ123',
            'password2': 'zaq123ZA',
        }
        
    def test_succ_register(self):
        response = self.client.get(
            '/auth/register/',
            # reverse('my_auth:register'),
        )
        # self.assertIn('Username:', response.content.decode())
        self.assertContains(response, 'Имя пользователя:', status_code=200)
        # self.assertEqual(200, response.status_code)

        # # post
        response = self.client.post(
            '/auth/register/',
            data=self.user_data,
        )
        
        self.assertEqual(302, response.status_code)

        # check user
        new_user = get_user_model().objects.get(
            username=self.user_data['username']
        )

        self.assertEqual(
            self.user_data['email'],
            new_user.email,
        )
    

    def test_fail_register(self):
        response = self.client.post(
            # reverse('my_auth:register'),
            '/auth/register/',
            data=self.user_broken_data,
        )
        self.assertEqual(200, response.status_code)

        self.assertFormError(
            response.context['form'],
            'password2',
            ['Введенные пароли не совпадают.']
            # _('The two password fields didn’t match.')
            # 'Введенные пароли не совпадают.'
        )


class ListCategoryTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user_with_permission = get_user_model().objects.create_user(
            username='admin',
            email='admin@admin.local',
            password='zaq123ZAQ123'
        )
        cls.user_without_permission = get_user_model().objects.create_user(
            username='user',
            email='user@user.local',
            password='userpassword'
        )
        cls.category1 = Category.objects.create(name='Category 1')
        cls.category2 = Category.objects.create(name='Category 2')
        cls.category3 = Category.objects.create(name='Category 3')
        cls.category4 = Category.objects.create(name='Category 4')

        # Предоставляем права пользователю с правами
        cls.user_with_permission.user_permissions.add(
            Permission.objects.get(codename='view_category')
        )

    def test_list_category_with_permission(self):
        self.client.login(username='admin', password='zaq123ZAQ123')
        response = self.client.get(reverse('store_app:list_category'))  # Запрос к первой странице
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Category 1')  # Проверка наличия Category 1
        self.assertContains(response, 'Category 2')  # Проверка наличия Category 2
        self.assertContains(response, 'Category 3')  # Проверка наличия Category 3
        self.assertContains(response, 'Category 4')  # Проверка наличия Category 4

    def test_list_category_without_permission(self):
        self.client.login(username='user', password='userpassword')
        response = self.client.get(reverse('store_app:list_category'))  # Запрос к первой странице
        self.assertEqual(response.status_code, 403)  # Доступ запрещен