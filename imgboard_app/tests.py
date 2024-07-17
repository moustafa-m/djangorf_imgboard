from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from django.conf import settings
from os import path

from .api import serializers
from . import models

# ----> Posts tests
class PostTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser1',
                                            password='testuser1')
        self.user2 = User.objects.create_user(username='testuser2',
                                            password='testuser2')
        self.token = Token.objects.get(user__username = self.user.get_username())
        self.token2 = Token.objects.get(user__username = self.user2.get_username())
        
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        
        # https://stackoverflow.com/a/50453780
        self.small_gif = (
                b'\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x00\x00\x00\x21\xf9\x04'
                b'\x01\x0a\x00\x01\x00\x2c\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02'
                b'\x02\x4c\x01\x00\x3b'
            )
        self.post = models.Post.objects.create(user=self.user,
                                               image=SimpleUploadedFile('small.gif', self.small_gif, content_type='image/gif'),
                                               title='test')
    
    def test_post_list(self):
        response = self.client.get(reverse('post_list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        self.client.force_authenticate(user=None)
        response = self.client.get(reverse('post_list'))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        models.Post.objects.get(pk=self.post.pk).image.delete()
        self.post.image.delete()
    
    def test_post_get(self):
        response = self.client.get(reverse('post_details', args=[self.post.pk]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        models.Post.objects.get(pk=self.post.pk).image.delete()
        self.post.image.delete()
    
    def test_post_post(self):
        data = {
            'image': SimpleUploadedFile('small.gif', self.small_gif, content_type='image/gif'),
            'title': 'test',
            'text': 'test',
        }
        response = self.client.post(reverse('post_create'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        self.client.force_authenticate(user=None)
        response = self.client.post(reverse('post_create'), data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
        for obj in models.Post.objects.all():
            obj.image.delete()
        self.post.image.delete()
    
    def test_post_put(self):
        img_path = path.join(settings.MEDIA_ROOT, 'test_img.png')
        data = {
            'image': SimpleUploadedFile('small.gif', content=open(img_path, 'rb').read()),
            'title': 'test',
            'text': 'new',
        }
        response = self.client.put(reverse('post_details', args=[self.post.pk]), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(models.Post.objects.get(pk=self.post.pk).text, data['text'])
        
        # different user
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token2.key)
        response = self.client.put(reverse('post_details', args=[self.post.pk]), data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        models.Post.objects.get(pk=self.post.pk).image.delete()
        self.post.image.delete()
    
    def test_post_delete(self):
        # different user
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token2.key)
        response = self.client.delete(reverse('post_details', args=[self.post.pk]))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(1, models.Post.objects.all().count())
        
        # post user
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        response = self.client.delete(reverse('post_details', args=[self.post.pk]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(0, models.Post.objects.all().count())
        self.post.image.delete()
# <---- Posts tests
