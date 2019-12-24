from django.shortcuts import render, redirect
from django.views import View
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator
from django.http import HttpResponse, JsonResponse

from blog import models


class Blog(View):
    """
    View class for the blog page, which gets the pinned blog post
    """

    def get(self, request):
        try:
            last_pinned = models.BlogPost.objects.filter(pin_to_top=True).latest('creation_date')
        except ObjectDoesNotExist:
            last_pinned = models.BlogPost.objects.latest('creation_date')
        tags = last_pinned.tags.all()
        response = render(request, 'blog.html', {'post': last_pinned, 'tags': tags, 'show_archive': True})
        if not request.user.is_authenticated :
            response.delete_cookie('commentoCommenterToken')

        return response


class BlogPost(View):
    """
    View class for showing a Blog post based on its ID
    """

    def get(self, request, post_slug):
        post = models.BlogPost.objects.get(slug=post_slug)
        tags = post.tags.all()
        response = render(request, 'blog.html', {
            'post': post,
            'tags': tags,
            'show_archive': False
        })
        if not request.user.is_authenticated :
            response.delete_cookie('commentoCommenterToken')
        return response


class PostList(View):
    """
    View class for showing the blog list using pagination
    """

    def get(self, request):
        if request.GET.get('tag'):
            posts = models.BlogPost.objects.filter(tags__name__in=[request.GET.get('tag')]).order_by('-creation_date')
        else:
            posts = models.BlogPost.objects.order_by('-creation_date')
        paginator = Paginator(posts, 12)

        page = request.GET.get('page', 1)
        current_posts = paginator.get_page(page)
        has_next = current_posts.has_next()
        has_previous = current_posts.has_previous()

        return render(request, 'archive.html', {
            'posts': current_posts,
            'has_next': has_next,
            'has_previous': has_previous
        })


class PostData(View):
    """
    Class used for returning JSON data
    """

    def get(self, request):
        if request.GET.get('tag'):
            posts = models.BlogPost.objects.filter(tags__name__in=[request.GET.get('tag')]).order_by('-creation_date')
        else:
            posts = models.BlogPost.objects.order_by('-creation_date').order_by('-creation_date').values()
        paginator = Paginator(posts, 12)
        page = request.GET.get('page', 1)
        current_posts = paginator.get_page(page)

        return JsonResponse({
            'posts': list(current_posts),
            'page': int(page),
            'total_pages': paginator.num_pages,
        })
