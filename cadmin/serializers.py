from rest_framework import serializers
from . import models


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Users
        fields = ['username']


class MediasSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Medias
        fields = '__all__'


class PostsSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Posts
        fields = ['id', 'slug', 'title', 'status', 'context', 'tags', 'featured_images', 'disallow_comments', 'updated_on', 'posted_by_name', 'created_at',
            'upvotes_count', 'comments_count', 'get_update_time', 'beauty_context', 'hidden_context']
        extra_kwargs = {'created_at': {'required': False}}

class ThirdSubCommentsSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = models.Comments
        fields = ['id', 'post', 'comment', 'message', 'created_at', 'get_update_time', 'posted_by_name', 'created_at',
            'upvotes_count', 'comments_count', 'get_update_time', 'beauty_context', 'hidden_context']


class SubCommentsSerializer(serializers.ModelSerializer):
    sub_comment_list = ThirdSubCommentsSerializer(many=True, read_only=True)
    
    class Meta:
        model = models.Comments
        fields = ['id', 'post', 'comment', 'message', 'created_at', 'get_update_time', 'posted_by_name', 'created_at',
            'upvotes_count', 'comments_count', 'get_update_time', 'beauty_context', 'hidden_context', 'sub_comment_list']


class CommentsSerializer(serializers.ModelSerializer):
    sub_comment_list = SubCommentsSerializer(many=True, read_only=True)

    class Meta:
        model = models.Comments
        fields = ['id', 'post', 'comment', 'message', 'created_at', 'get_update_time', 'posted_by_name', 'created_at',
            'upvotes_count', 'comments_count', 'get_update_time', 'beauty_context', 'hidden_context', 'sub_comment_list']