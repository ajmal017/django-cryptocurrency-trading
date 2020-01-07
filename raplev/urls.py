""" raplev URL Configuration

The `urlpatterns` list routes URLs to wallet_views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function wallet_views
    1. Add an import:  from my_app import wallet_views
    2. Add a URL to urlpatterns:  path('', wallet_views.home, name='home')
Class-based wallet_views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path, include
from django.contrib import admin
from wallet import views as wallet_views
from blog import views as blog_views
from commento_sso.views import SingleSignOnView
from django.contrib.auth import views as auth_views
from cadmin import views as cadmin_views

urlpatterns = [
    path('cadmin/', include('cadmin.urls')),
    path('super-admin/', admin.site.urls),
    path('', wallet_views.IndexView.as_view()),
    path('affiliates', wallet_views.AffiliatesView.as_view()),
    path('all-offers', wallet_views.AllOffersView.as_view()),
    path('balance', wallet_views.BalanceView.as_view()),
    path('blog', blog_views.Blog.as_view()),
    path('blog/sso', SingleSignOnView.as_view()),
    path('blog/archive', blog_views.PostList.as_view()),
    path('blog/archive/data', blog_views.PostData.as_view()),
    path('blog/archive/<slug:post_slug>', blog_views.BlogPost.as_view()),
    path('buy', wallet_views.BuyView.as_view()),
    path('contact', wallet_views.ContactView.as_view()),
    path('dispute-details', wallet_views.DisputeDetailsView.as_view()),
    path('support-center', wallet_views.DisputCenterView.as_view()),
    path('escrows', wallet_views.EscrowsView.as_view()),
    path('faq', wallet_views.FaqView.as_view()),
    path('fund', wallet_views.FundingView.as_view()),
    path('history', wallet_views.HistoryView.as_view()),
    path('index', wallet_views.IndexView.as_view()),
    path('initiate-trade', wallet_views.InitiateTradeView.as_view()),
    path('messages', wallet_views.MessagesView.as_view()),
    path('offers', wallet_views.OffersView.as_view()),
    path('offer-activity', wallet_views.OfferActivityView.as_view()),
    path('offer-process', wallet_views.OfferProcessView.as_view()),
    path('offer-waiting', wallet_views.OfferWaitingView.as_view()),
    path('overview', wallet_views.OverviewView.as_view()),
    path('receive', wallet_views.ReceiveView.as_view()),
    path('refer', wallet_views.ReferView.as_view()),
    path('send-offer', wallet_views.SendOfferView.as_view()),
    path('sell', wallet_views.SellView.as_view()),
    path('send', wallet_views.SendView.as_view()),
    path('submit', wallet_views.SubmitView.as_view()),
    path('support', wallet_views.SupportView.as_view()),
    path('new-offer', wallet_views.TradeView.as_view()),
    path('trade-completed', wallet_views.TradeCompletedView.as_view()),
    path('verification', wallet_views.VerificationView.as_view()),
    path('verification-b', wallet_views.VerificationBView.as_view()),
    path('wallets', wallet_views.WalletsView.as_view()),
    path('accounts/register', wallet_views.RegistrationView.as_view()),
    path('accounts/login', wallet_views.LogInView.as_view()),
    path('accounts/login/', wallet_views.LogInView.as_view()),
    path('accounts/validate_username', wallet_views.UserExistsView.as_view()),
    path('accounts/phone_validation', wallet_views.PhoneValidationView.as_view()),
    path('accounts/phone_activation', wallet_views.PhoneActivationView.as_view()),
    path('accounts/phone_resend_code', wallet_views.ResendPhoneValidationView.as_view()),
    path('accounts/send_new_email', wallet_views.SendNewEmailView.as_view()),
    path('accounts/logout', wallet_views.LogOutView.as_view()),
    path('accounts/change_password', wallet_views.ChangePasswordView.as_view()),

    # path('accounts/update', wallet_views.),
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('upload_proof_transaction_slip', wallet_views.ProofTransactionSlipView.as_view()),
    path('confirm_email', wallet_views.EmailConfirmationView.as_view()),
    path('edit_cc/<int:cc_id>', wallet_views.EditCreditCardView.as_view()),
    path('tinymce/', include('tinymce.urls')),
    path('api/get_exchange_rate/<str:currencies>', wallet_views.ExchangeRateView.as_view()),
    path('api/trades/<str:operation>', wallet_views.TradeDataView.as_view()),
    path('deposits-and-withdrawals', wallet_views.DepositsAndWithdrawalsView.as_view()),
    path('trade/<int:trade_id>', wallet_views.SingleTradeDetailsView.as_view()),
    path('<slug:link>/', cadmin_views.go_page),
]

from django.conf import settings
# if settings.DEBUG:
from django.conf.urls.static import static
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)