    
from django.contrib.auth import get_user_model

from django.test import Client, TestCase
from django.urls import reverse
from ..models import Group, Post
from django.core.cache import cache

User = get_user_model()


class PostPagesTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='auth')
        cls.group = Group.objects.create(
            title='Тестовая группа',
            slug='test-slug',
            description='Тестовое описание',
        )
        cls.post = Post.objects.create(
            author=cls.user,
            text='text',
            group=cls.group,
        )

    def setUp(self):
        self.user = User.objects.create_user(username='Andrey')
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)
        self.authorized_client.force_login(self.post.author)
    
    def test_cache_index(self):
        post = Post.objects.create(
            text='тест кэша',
            author=self.user,
        )
        content_add = self.authorized_client.get(
            reverse('posts:index')).content
        post.delete()
        content_delete = self.authorized_client.get(
            reverse('posts:index')).content
        self.assertEqual(content_add, content_delete)
        cache.clear()
        content_delete = self.authorized_client.get(
            reverse('posts:index')).content
        self.assertNotEqual(content_add, content_delete)