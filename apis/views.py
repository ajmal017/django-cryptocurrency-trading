import json
import random
from datetime import datetime

from django.shortcuts import render

# Create your views here.
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination
from rest_framework.generics import ListCreateAPIView, ListAPIView, RetrieveUpdateDestroyAPIView
from django.utils.crypto import get_random_string
from rest_framework.serializers import ValidationError

from cadmin import models, serializers
from django.http import JsonResponse, HttpResponse
from loremipsum import get_sentence
from slugify import slugify


class Logout(APIView):
    def get(self, request, format=None):
        request.user.auth_token.delete()
        return Response('success', status=status.HTTP_200_OK)


class FakePost(APIView):
    permission_classes = (IsAdminUser,)

    def get(self, request):
        item = models.Posts()
        item.created_at = datetime.now()
        item.posted_by = models.Users.objects.order_by('?').first()
        item.status =  'Publish'
        item.title = get_sentence(1)
        item.context = get_sentence(5)
        item.disallow_comments = False
        item.updated_on = datetime.now()
        item.save()
        return JsonResponse({'id': item.id, 'posted_by': item.posted_by.username, 'title': item.title, 'context': item.context})


class FakeComment(APIView):
    permission_classes = (IsAdminUser,)

    def get(self, request):
        print(request.user.id)
        item = models.Comments()
        item.post = models.Posts.objects.get(id=request.GET.get('p')) if request.GET.get('p') else models.Posts.objects.order_by('?').first()
        item.comment = models.Comments.objects.order_by('?').first() if random.random()<0.3 else None
        item.message = get_sentence(1)
        item.created_by = models.Users.objects.order_by('?').first()
        item.created_at = datetime.now()
        item.save()
        return JsonResponse({'id': item.id, 'post_id': item.post.id, 'comment': item.comment.id if item.comment else '', 'message': item.message})


class CustomPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 1000
    template = 'apis/pagination/numbers.html'

    def get_paginated_response(self, data):
        return Response({
            'get_html_context': self.get_html_context(),
            'to_html': self.to_html(),
            'count': self.page.paginator.count,
            'page_size': self.page_size,
            'results': data
        })


class PostList(ListCreateAPIView):
    permission_classes = (IsAuthenticated,)

    serializer_class = serializers.PostsSerializer
    pagination_class = CustomPagination
    search = None
    type = None
    user = None

    def get(self, request, *args, **kwargs):
        self.search = request.GET.get('s', '')
        self.type = request.GET.get('t', '')
        self.user = request.user
        return self.list(request, *args, **kwargs)

    def get_queryset(self):
        if self.type == 'new':
            return models.Posts.objects.filter(status='Publish').order_by('-updated_on')

        if self.type == 'top':
            queryset = models.Posts.objects.filter(status='Publish').order_by('-updated_on')
            queryset_ids = [item.id for item in queryset if item.upvotes_count > 0]
            queryset = queryset.filter(id__in=queryset_ids)
            return queryset

        if self.type == 'search':
            return models.Posts.objects.filter(status='Publish', title__icontains=self.search).order_by('-updated_on')

        if self.type == 'my':
            return models.Posts.objects.filter(status='Publish', posted_by=self.user).order_by('-updated_on')

        return models.Posts.objects.filter(status='Publish').order_by('-updated_on')

    def perform_create(self, serializer):
        serializer.save(created_at=datetime.now())
        serializer.save(posted_by=self.request.user)
        serializer.save(slug=slugify(serializer.validated_data['title']))


class PostDetail(RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated,)

    queryset = models.Posts.objects.all()
    serializer_class = serializers.PostsSerializer

    def put(self, request, *args, **kwargs):
        if self.request.user != self.get_object().posted_by:
            return JsonResponse({'non_field_errors': 'You can`t change this post.'}, status=500)
        return self.update(request, *args, **kwargs)


class CustomLimitOffset(LimitOffsetPagination):
    default_limit = 10
    max_limit = 1000
    # template = 'apis/pagination/numbers.html'


class CommentList(ListCreateAPIView):
    permission_classes = (IsAuthenticated,)

    serializer_class = serializers.CommentsSerializer
    pagination_class = CustomLimitOffset
    post_id = None

    def get(self, request, *args, **kwargs):
        self.post_id = request.GET.get('p', '')
        return self.list(request, *args, **kwargs)

    def get_queryset(self):
        return models.Comments.objects.filter(post_id=self.post_id, comment=None).order_by('-created_at')

    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(created_by=user)
        post = models.Posts.objects.get(id=self.request.data['post_id'])
        if models.Comments.objects.filter(post=post, created_by=user, comment=None).count() > 0:
            raise ValidationError('You commented to this post already.')
        else:
            serializer.save(post=post)
        # serializer.save(post=models.Comments.objects.get(id=self.request.data.comment_id))


class CommentDetail(RetrieveUpdateDestroyAPIView):
    queryset = models.Comments.objects.all()
    serializer_class = serializers.CommentsSerializer