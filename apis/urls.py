from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from apis import views

urlpatterns = [
    path('fake-post/', views.FakePost.as_view(), name='fake-post'),
    path('fake-comment/', views.FakeComment.as_view(), name='fake-comment'),
    path('api-token-auth/', obtain_auth_token, name='api_token_auth'),
    path('api-token-logout/', views.Logout.as_view(), name='api_token_logout'),
    path('posts/', views.PostList.as_view(), name='post-list'),
    path('posts/<int:pk>/', views.PostDetail.as_view(), name='single-post'),
    path('comments/', views.CommentList.as_view(), name='comment-list'),
    path('comments/<int:pk>/', views.CommentDetail.as_view(), name='single-comment'),
]