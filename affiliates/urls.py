from django.urls import path

from . import views
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                
app_name = 'affiliates'
urlpatterns = [
    # Not Logged In
    path('login/', views.Login.as_view(), name='login'),
    path('request/', views.Register.as_view(), name='register'),
    path('password/', views.ForgotPassword.as_view(), name='forgot-password'),
    path('reset/', views.ResetPassword.as_view(), name='reset-password'),
    
    # Login Required
    path('logout/', views.logout, name='logout'),

    path('', views.Index.as_view(), name='index'),
    path('dashboard/', views.Dashboard.as_view(), name='dashboard'),
    path('contact/', views.Contact.as_view(), name='contact'),
    path('profile/', views.Profile.as_view(), name='profile'),
    path('reports/', views.Reports.as_view(), name='reports'),
    path('campaigns/', views.Campaigns.as_view(), name='campaigns'),
    path('campaign-details/', views.CampaignDetails.as_view(), name='campaign-details')
]
