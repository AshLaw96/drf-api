from django.contrib.auth.models import User
from .models import Post
from rest_framework import status
from rest_framework.test import APITestCase


class PostListViewTests(APITestCase):
    def setUp(self):
        User.objects.create_user(username='adam', password='pass')

    def test_can_list_posts(self):
        adam = User.objects.get(username='adam')
        Post.objects.create(owner=adam, title='a title')
        response = self.client.get('/posts/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        print(response.data)
        print(len(response.data))

    def test_logged_in_user_can_create_post(self):
        self.client.login(username='adam', password='pass')
        response = self.client.post('/posts/', {'title': 'a title'})
        count = Post.objects.count()
        self.assertEqual(count, 1)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_logged_out_user_cannot_create_post(self):
        response = self.client.post('/posts/', {'title': 'a title'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class PostDetailViewTests(APITestCase):
    def setUp(self):
        adam = User.objects.create_user(username='adam', password='pass')
        eve = User.objects.create_user(username='eve', password='pass')
        Post.objects.create(
            owner=adam, title='a title', content='adam content'
        )
        Post.objects.create(
            owner=eve, title='eve title', content='eve content'
        )

    def test_can_retrieve_post(self):
        response = self.client.get('/posts/1/')
        self.assertEqual(response.data['title'], 'a title')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_cannot_retrieve_post_with_invalid_id(self):
        response = self.client.get('/posts/100/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_logged_in_user_can_update_post(self):
        self.client.login(username='adam', password='pass')
        response = self.client.put('/posts/1/', {'title': 'new title'})
        post = Post.objects.filter(pk=1).first()
        self.assertEqual(post.title, 'new title')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_logged_in_user_cannot_update_post_of_other_user(self):
        self.client.login(username='adam', password='pass')
        response = self.client.put('/posts/2/', {'title': 'new title'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
