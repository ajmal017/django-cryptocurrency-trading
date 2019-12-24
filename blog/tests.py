from django.test import TestCase
from django.urls import resolve
from wallet.models import User
from django.core.management import call_command

from blog import models


def _create_user(username, password):
    valid_user = User.objects.create_user(username=username)
    valid_user.email = username
    valid_user.set_password(password)
    return valid_user


class TestBlogViews(TestCase):
    """
    Class used for testing the views of the Blog application
    """
    def setUp(self):
        test_user = _create_user(username='test@test.com', password='123lalala321')
        test_user.save()
        call_command("loaddata", "blog/fixtures/blog.json", verbosity=0)
        test_post = models.BlogPost(
            user=test_user,
            title='Test Post',
            slug='test-post',
            contents='<p>Test</p>',
            abstract='<p>Test</p>',
        )
        test_post.save()
        self.pages = ['blog', 'blog/archive', 'blog/archive/test-post']
        self.views = {
            'blog': 'blog.views.Blog',
            'blog/archive': 'blog.views.PostList',
            'blog/archive/test-post': 'blog.views.BlogPost',
        }
        self.templates = {
            'blog': 'blog.html',
            'blog/archive': 'archive.html',
            'blog/archive/test-post': 'blog.html',
        }

    def test_views(self):
        """
        Check if URLs are correct, views exist, use the correct template and render correctly
        """
        self.client.login(username='test@test.com', password='123lalala321')
        for page in self.pages:
            found = resolve('/' + page)
            response = self.client.get('/' + page, )

            self.assertEqual(found.view_name, self.views[page])
            try:
                self.assertTemplateUsed(response, self.templates[page])
            except AssertionError:
                print(page)
                print(response)
            self.assertEqual(response.status_code, 200)

    def test_archive_page(self):
        response = self.client.get('/blog/archive/data', )

        self.assertContains(response, 'posts')
        self.assertContains(response, 'page')
        self.assertContains(response, 'total_pages')


class TestBlogPosts(TestCase):
    """
    Class used for testing the blog posts
    """
    def setUp(self):
        self.admin = _create_user('admin', '123super321')
        self.admin.save()
        self.posts = []
        for i in range(23):
            new_post = models.BlogPost(
                user=self.admin,
                slug='post-{}'.format(i),
                title='Post {}'.format(i),
                contents='Contents {i}',
                abstract='Abstract {i}'
            )
            self.posts.append(new_post)
            new_post.save()

    def tearDown(self):
        blogs = models.BlogPost.objects.all()
        blogs.delete()

    def test_get_first_page(self):
        page1 = self.client.get('/blog/archive', )
        page2 = self.client.get('/blog/archive?page=2', )

        self.assertContains(page1, 'I want to load more')
        self.assertContains(page2, 'I want to load more')
