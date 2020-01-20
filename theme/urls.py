from django.conf.urls import include, url
from django.urls import path
from django.views.generic import TemplateView

from . import views
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                
app_name = 'theme'
urlpatterns = [
    # Login Not Required
    path('', views.Index.as_view(), name='index'),
    path('index/', views.Index.as_view()),
    path('blog-listing/', views.BlogListing.as_view(), name='blog-listing'),
    path('blog-detail/', views.BlogDetail.as_view(), name='blog-detail'),
    path('contact/', views.Contact.as_view(), name='contact'),
    path('support-center/', views.SupportCenter.as_view(), name='support-center'),
    path('submit-ticket/', views.SubmitTicket.as_view(), name='submit-ticket'),
    path('ticket-details/', views.TicketDetails.as_view(), name='ticket-details'),

    # Not Logged In
    path('login/', views.Login.as_view(), name='login'),
    path('register/', views.Register.as_view(), name='register'),
    path('forgot-password/', views.ForgotPassword.as_view(), name='forgot-password'),
    path('forgot-password-email/', views.ForgotPasswordEmail.as_view(), name='forgot-password-email'),
    path('forgot-password-phone/', views.ForgotPasswordPhone.as_view(), name='forgot-password-phone'),
    path('resend-forgot-password-email/', views.ResendConfirmEmail.as_view(), name='resend-forgot-password-email'), #for forgot password with email
    path('resend-forgot-password-phone/', views.ResendConfirmPhone.as_view(), name='resend-forgot-password-phone'), #for forgot password with phone
    path('confirm-forgot-password-phone-code/', views.ConfirmForgotPWPhoneCode.as_view(), name='resend-forgot-password-phone-code'), #for forgot password get phone code
    path('confirm-forgot-password-email/', views.ConfirmForgotPWEmail.as_view(), name='confirm-forgot-password-email'), #for reset password with email
    path('confirm-forgot-password-phone/', views.ConfirmForgotPWPhone.as_view(), name='confirm-forgot-password-phone'), #for reset password with email
    path('reset-password/', views.ResetPassword.as_view(), name='reset-password'),
    
    # Login Required
    path('logout/', views.logout, name='logout'),
    path('resend-verify-email/', views.ResendVerifyEmail.as_view(), name='resend-verify-email'), #for email verify
    path('resend-verify-phone/', views.ResendVerifyPhone.as_view(), name='resend-verify-phone'), #for phone verify
    path('verify-phone-code/', views.VerifyPhoneCode.as_view(), name='resend-confirm-phone-code'), #for verify phone code
    path('verify-email/', views.VerifyEmail.as_view(), name='verify-email'), #for verify email
    path('verify-phone/', views.VerifyPhone.as_view(), name='verify-phone'), #for verify phone

    path('new-offer/', views.NewOffer.as_view(), name='new-offer'),
    path('profile-overview/', views.ProfileOverview.as_view(), name='profile-overview'),
    path('received-offers/', views.ReceivedOffers.as_view(), name='received-offers'),
    # path('buy-sell-coins/', views.BuySellCoins.as_view(), name='buy-sell-coins'),
    path('funding/', views.Funding.as_view(), name='funding'),
    path('user-public-profile/', views.UserPublicProfile.as_view(), name='user-public-profile'),
    path('offer-activity/', views.OfferActivity.as_view(), name='offer-activity'),
    path('edit-offer/', views.EditOffer.as_view(), name='edit-offer'),
    path('all-offers/', views.AllOffers.as_view(), name='all-offers'),
    path('offer-detail/', views.OfferDetail.as_view(), name='offer-detail'),
    path('offer-listing/', views.OfferListing.as_view(), name='offer-listing'),
    # path('buy-listing/', views.BuyListing.as_view(), name='buy-listing'),
    # path('sell-listing/', views.SellListing.as_view(), name='sell-listing'),
    path('single-offer-detail/', views.SingleOfferDetail.as_view(), name='single-offer-detail'),
    path('initiate-trade/', views.InitiateTrade.as_view(), name='initiate-trade'),
    path('trade-processed/', views.TradeProcessed.as_view(), name='trade-processed'),
    path('proof-of-transaction/', views.ProofOfTransaction.as_view(), name='proof-of-transaction'),
    path('trade-complete/', views.TradeComplete.as_view(), name='trade-complete'),
    path('send-counter-offer/', views.SendCounterOffer.as_view(), name='send-counter-offer'),
    path('watch-list/', views.WatchList.as_view(), name='watch-list'),
    path('flag-feedback/', views.FlagFeedback.as_view(), name='flag-feedback'),
    path('leave-review/', views.LeaveReview.as_view(), name='leave-review'),
    path('independent-escrow/', views.IndependentEscrow.as_view(), name='independent-escrow'),
    path('vendor-proof-of-transaction/', views.VendorProofOfTransaction.as_view(), name='vendor-proof-of-transaction'),
    path('vpof-gift-card-steps', views.VPOFGiftCardSteps.as_view(), name='vpof-gift-card-steps'),
    path('vpof-gift-card-open-code', views.VPOFGiftCardOpenCode.as_view(), name='vpof-gift-card-open-code'),
    path('send/', views.Send.as_view(), name='send'),
    path('receive/<slug:crypto>', views.receive, name='receive'),
    path('transaction-history/', views.TransactionHistory.as_view(), name='transaction-history'),
    path('saved-wallets/', views.SavedWallets.as_view(), name='saved-wallets'),
    path('my-balance/', views.MyBalance.as_view(), name='my-balance'),
    path('withdraw-funds/', views.WithdrawFunds.as_view(), name='withdraw-funds'),
    path('deposits/', views.Deposits.as_view(), name='deposits'),
    path('withdrawals/', views.Withdrawals.as_view(), name='withdrawals'),
    path('messages/', views.Messages.as_view(), name='messages'),
    path('invitation-in-message/', views.InvitationInMessage.as_view(), name='invitation-in-message'),
    path('id-verification/', views.IdVerification.as_view(), name='id-verification'),
    path('notifications/', views.Notifications.as_view(), name='notifications'),
    path('vendors/', views.Vendors.as_view(), name='vendors'),
    path('referrals/', views.Referrals.as_view(), name='referrals'),

    path('buy/', views.Buy.as_view(), name='buy'), #landing page as multi language.
    path('add-message/', views.AddMessage.as_view(), name='buy'), 
    path('upload/', views.UploadView.as_view(), name='upload'),


    # path('messages/', views.Messages.as_view(), name='messages'),
    # path('confirm/<slug:mode>', views.confirm, name='confirm'),
    # path('all-offers/', views.AllOffers.as_view(), name='all-offers'),


    # path('00_styleguide/', TemplateView.as_view(template_name="theme/__src__/00_styleguide.html")),
    # path('p/', TemplateView.as_view(template_name="theme/__src__/01_pages.html")),
    # path('02_popups/', TemplateView.as_view(template_name="theme/__src__/02_popups.html")),
    # path('03_sample-page/', TemplateView.as_view(template_name="theme/__src__/03_sample-page.html")),
    # path('landing-china-all-coins/', TemplateView.as_view(template_name="theme/__src__/landing-china-all-coins.html")),
    # path('landing-china-bitcoin/', TemplateView.as_view(template_name="theme/__src__/landing-china-bitcoin.html")),
    # path('landing-russia-all-coins/', TemplateView.as_view(template_name="theme/__src__/landing-russia-all-coins.html")),
    # path('landing-russia-bitcoin/', TemplateView.as_view(template_name="theme/__src__/landing-russia-bitcoin.html")),
    # path('landing-nigeria-all-coins/', TemplateView.as_view(template_name="theme/__src__/landing-nigeria-all-coins.html")),
    # path('landing-nigeria-bitcoin/', TemplateView.as_view(template_name="theme/__src__/landing-nigeria-bitcoin.html")),
    # path('user-public-profile/', TemplateView.as_view(template_name="theme/__src__/user-public-profile.html")),
    # path('index/', TemplateView.as_view(template_name="theme/__src__/index.html")),
    # path('index-logged/', TemplateView.as_view(template_name="theme/__src__/index-logged.html")),
    # path('fund/', TemplateView.as_view(template_name="theme/__src__/fund.html")),
    # path('received-offers/', TemplateView.as_view(template_name="theme/__src__/received-offers.html")),
    # path('all-offers/', TemplateView.as_view(template_name="theme/__src__/all-offers.html")),
    # path('buy-listing/', TemplateView.as_view(template_name="theme/__src__/buy-listing.html")),
    # path('sell-listing/', TemplateView.as_view(template_name="theme/__src__/sell-listing.html")),
    # path('trade-processed-awaiting-proof/', TemplateView.as_view(template_name="theme/__src__/trade-processed-awaiting-proof.html")),
    # path('trade-processed-uploaded-proof/', TemplateView.as_view(template_name="theme/__src__/trade-processed-uploaded-proof.html")),
    # path('trade-completed/', TemplateView.as_view(template_name="theme/__src__/trade-completed.html")),
    # path('trade-processed-awaiting-code-gift-card/', TemplateView.as_view(template_name="theme/__src__/trade-processed-awaiting-code-gift-card.html")),
    # path('trade-processed-code-added-gift-card/', TemplateView.as_view(template_name="theme/__src__/trade-processed-code-added-gift-card.html")),
    # path('404-error/', TemplateView.as_view(template_name="theme/__src__/404-error.html")),
    # path('contact/', TemplateView.as_view(template_name="theme/__src__/contact.html")),
    # path('faq/', TemplateView.as_view(template_name="theme/__src__/faq.html")),
    # path('blog/', TemplateView.as_view(template_name="theme/__src__/blog.html")),
    # path('blog-listing/', TemplateView.as_view(template_name="theme/__src__/blog-listing.html")),
    # path('send-offer/', TemplateView.as_view(template_name="theme/__src__/send-offer.html")),
    # path('initiate-trade/', TemplateView.as_view(template_name="theme/__src__/initiate-trade.html")),
    # path('independent-escrow/', TemplateView.as_view(template_name="theme/__src__/independent-escrow.html")),
    # path('dashboard/', TemplateView.as_view(template_name="theme/__src__/dashboard.html")),
    # path('id-verification/', TemplateView.as_view(template_name="theme/__src__/id-verification.html")),
    # path('id-verification-uploading/', TemplateView.as_view(template_name="theme/__src__/id-verification-uploading.html")),
    # path('withdrawals/', TemplateView.as_view(template_name="theme/__src__/withdrawals.html")),
    # path('deposits/', TemplateView.as_view(template_name="theme/__src__/deposits.html")),
    # path('my-balance/', TemplateView.as_view(template_name="theme/__src__/my-balance.html")),
    # path('saved-wallet/', TemplateView.as_view(template_name="theme/__src__/saved-wallet.html")),
    # path('support-center/', TemplateView.as_view(template_name="theme/__src__/support-center.html")),
    # path('submit-ticket/', TemplateView.as_view(template_name="theme/__src__/submit-ticket.html")),
    # path('send/', TemplateView.as_view(template_name="theme/__src__/send.html")),
    # path('trade-history/', TemplateView.as_view(template_name="theme/__src__/trade-history.html")),
    # path('receive/', TemplateView.as_view(template_name="theme/__src__/receive.html")),
    # path('messages/', TemplateView.as_view(template_name="theme/__src__/messages.html")),
    # path('individual-2factor-auth/', TemplateView.as_view(template_name="theme/__src__/individual-2factor-auth.html")),
    # path('individual-forgot-password-with-phone/', TemplateView.as_view(template_name="theme/__src__/individual-forgot-password-with-phone.html")),
    # # path('reset-password/', TemplateView.as_view(template_name="theme/__src__/reset-password.html")),
    # path('individual-login/', TemplateView.as_view(template_name="theme/__src__/individual-login.html")),
    # path('individual-signup/', TemplateView.as_view(template_name="theme/__src__/individual-signup.html")),
    # path('individual-2factor-auth/', TemplateView.as_view(template_name="theme/__src__/individual-2factor-auth.html")),
    # path('enter-code-from-phone/', TemplateView.as_view(template_name="theme/__src__/enter-code-from-phone.html")),
    # path('withdraw-funds/', TemplateView.as_view(template_name="theme/__src__/withdraw-funds.html")),
    # path('flag-feedback/', TemplateView.as_view(template_name="theme/__src__/flag-feedback.html")),
    # path('leave-review/', TemplateView.as_view(template_name="theme/__src__/leave-review.html")),
    # path('notifications/', TemplateView.as_view(template_name="theme/__src__/notifications.html")),
    # path('offer-details/', TemplateView.as_view(template_name="theme/__src__/offer-details.html")),
    # path('vendor-review-proof-of-transaction-gift-card-steps/', TemplateView.as_view(template_name="theme/__src__/vendor-review-proof-of-transaction-gift-card-steps.html")),
    # path('vendor-review-proof-of-transaction-gift-card-open-code/', TemplateView.as_view(template_name="theme/__src__/vendor-review-proof-of-transaction-gift-card-open-code.html")),
    # path('vendor-review-proof-of-transaction/', TemplateView.as_view(template_name="theme/__src__/vendor-review-proof-of-transaction.html")),
    # path('proof-of-transaction/', TemplateView.as_view(template_name="theme/__src__/proof-of-transaction.html")),
    # path('ticket-details/', TemplateView.as_view(template_name="theme/__src__/ticket-details.html")),
    # path('seller-directory/', TemplateView.as_view(template_name="theme/__src__/seller-directory.html")),
    # path('watch-list/', TemplateView.as_view(template_name="theme/__src__/watch-list.html")),
    # path('referrals/', TemplateView.as_view(template_name="theme/__src__/referrals.html")),
    # path('proof-of-transaction-gift-card/', TemplateView.as_view(template_name="theme/__src__/proof-of-transaction-gift-card.html")),
    # path('offer-activity/', TemplateView.as_view(template_name="theme/__src__/offer-activity.html")),
    # path('single-offer-details/', TemplateView.as_view(template_name="theme/__src__/single-offer-details.html")),
    # path('new-offer/', TemplateView.as_view(template_name="theme/__src__/new-offer.html")),
]
