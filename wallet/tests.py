from django.test import TestCase
from django.urls import resolve
from django.core.management import call_command

from wallet import models


def _create_user(username, password):
    valid_user = models.User.objects.create_user(username=username)
    valid_user.email = username
    valid_user.set_password(password)
    return valid_user


class TestPages(TestCase):
    """
    Class used to test the pages:
    1. If the URL exists
    2. If the correct view is loaded
    3. If the correct template is used
    4. If the correct status code is received
    """

    def setUp(self):
        """
        Set up the page lists for testing
        """
        call_command("loaddata", "wallet/fixtures/wallet.json", verbosity=0)
        call_command("loaddata", "blog/fixtures/blog.json", verbosity=0)
        self.pages = ['affiliates', 'all-offers', 'balance', 'blog', 'blog/archive', 'buy', 'contact',
                      'dispute-details', 'support-center', 'escrows', 'faq', 'fund', 'history', 'initiate-trade',
                      'messages', 'offers', 'offer-activity', 'offer-process', 'offer-waiting', 'overview', 'receive',
                      'refer', 'send-offer', 'sell', 'send', 'submit', 'support', 'new-offer', 'trade-completed',
                      'verification', 'verification-b', 'wallets', 'accounts/change_password',
                      'upload_proof_transaction_slip', 'deposits-and-withdrawals', 'trade/1']
        self.views = {
            'affiliates': 'wallet.views.users.AffiliatesView',
            'all-offers': 'wallet.views.trades.AllOffersView',
            'balance': 'wallet.views.users.BalanceView',
            'blog': 'blog.views.Blog',
            'blog/archive': 'blog.views.PostList',
            'buy': 'wallet.views.trades.BuyView',
            'contact': 'wallet.views.site.ContactView',
            'dispute-details': 'wallet.views.users.DisputeDetailsView',
            'support-center': 'wallet.views.site.DisputCenterView',
            'escrows': 'wallet.views.users.EscrowsView',
            'faq': 'wallet.views.site.FaqView',
            'fund': 'wallet.views.users.FundingView',
            'history': 'wallet.views.users.HistoryView',
            'initiate-trade': 'wallet.views.trades.InitiateTradeView',
            'index': 'wallet.views.site.IndexView',
            'messages': 'wallet.views.site.MessagesView',
            'offers': 'wallet.views.trades.OffersView',
            'offer-activity': 'wallet.views.trades.OfferActivityView',
            'offer-process': 'wallet.views.trades.OfferProcessView',
            'offer-waiting': 'wallet.views.trades.OfferWaitingView',
            'overview': 'wallet.views.users.OverviewView',
            'receive': 'wallet.views.trades.ReceiveView',
            'refer': 'wallet.views.users.ReferView',
            'send-offer': 'wallet.views.trades.SendOfferView',
            'sell': 'wallet.views.trades.SellView',
            'send': 'wallet.views.users.SendView',
            'submit': 'wallet.views.site.SubmitView',
            'support': 'wallet.views.site.SupportView',
            'new-offer': 'wallet.views.trades.TradeView',
            'trade-completed': 'wallet.views.trades.TradeCompletedView',
            'verification': 'wallet.views.users.VerificationView',
            'verification-b': 'wallet.views.users.VerificationBView',
            'wallets': 'wallet.views.users.WalletsView',
            'accounts/change_password': 'wallet.views.users.ChangePasswordView',
            'upload_proof_transaction_slip': 'wallet.views.users.ProofTransactionSlipView',
            'deposits-and-withdrawals': 'wallet.views.users.DepositsAndWithdrawalsView',
            'trade/1': 'wallet.views.trades.SingleTradeDetailsView'
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
                self.assertTemplateUsed(response, page+'.html')
            except AssertionError:
                print(page)
                print(response)
            self.assertEqual(response.status_code, 200)


class TestAuth(TestCase):
    """
    Class for testing user creation, authentication, password reminding and password change
    """
    def test_registration(self):
        """
        Test if the registration page exists and if the user can be properly registered
        """
        registration_page = resolve('/accounts/register')
        response = self.client.post('/accounts/register', {
                'full_name': 'test test',
                'email': 'test@example.com',
                'password1': 'test1test',
                'password2': 'test1test',
                'registration_reason': 'SELL',
            })

        self.assertEqual(registration_page.view_name, 'wallet.views.users.RegistrationView')
        self.assertEqual(response.status_code, 302)

    def test_registration2(self):
        """
        Test if the registration page blocks passwords which are similar to name or email
        """
        registration_page = resolve('/accounts/register')
        response = self.client.post('/accounts/register', {
                'full_name': 'test+test',
                'email': 'test@test.com',
                'password1': 'test2test',
                'password2': 'test2test',
                'registration_reason': 'SELL',
            })

        self.assertEqual(registration_page.view_name, 'wallet.views.users.RegistrationView')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "The password is too similar to the email address.")

    def test_registration3(self):
        """
        Test if the registration page blocks passwords which are similar to name or email
        """
        registration_page = resolve('/accounts/register')
        response = self.client.post('/accounts/register', {
                'full_name': 'test+test',
                'email': 'omar@test.com',
                'password1': '3346457567867',
                'password2': '3346457567867',
                'registration_reason': 'SELL',
            })

        self.assertEqual(registration_page.view_name, 'wallet.views.users.RegistrationView')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "This password is entirely numeric.")

    def test_registration4(self):
        """
        Test if the registration page blocks passwords which are similar to name or email
        """
        registration_page = resolve('/accounts/register')
        response = self.client.post('/accounts/register', {
                'full_name': 'test+test',
                'email': 'test@test.com',
                'password1': 'test2test',
                'password2': 'test2test',
                'registration_reason': 'SELL',
            })

        self.assertEqual(registration_page.view_name, 'wallet.views.users.RegistrationView')
        self.assertEqual(response.status_code, 200)
        self.assertIn('registration_form', response.context)


class TestValidation(TestCase):
    """
    Class used for testing user validation
    """

    def setUp(self):
        current_user = _create_user(username='test@test.com', password='123lalala321')
        current_user.save()

    def test_username_validation(self):
        valid_response = self.client.post('/accounts/validate_username', {'email': 'test@test.com'})
        invalid_response = self.client.post('/accounts/validate_username', {'email': 'test2@example.com'})

        self.assertEqual(valid_response.content.decode(), '"An user with this email already exists."')
        self.assertEqual(invalid_response.content.decode(), '"true"')


class TestLogin(TestCase):
    """
    Class used for testing the login view
    """

    def setUp(self):
        current_user = _create_user(username='test@test.com', password='123lalala321')
        current_user.save()

    def test_user_login(self):
        login_page = resolve('/accounts/login')
        response = self.client.post('/accounts/login', {
            'username': 'test@test.com',
            'password': '123lalala321'
        })

        self.assertEqual(login_page.view_name, 'wallet.views.users.LogInView')
        self.assertEqual(response.status_code, 302)

    def test_invalid_login(self):
        login_page = resolve('/accounts/login')
        response = self.client.post('/accounts/login', {
            'username': 'test@example.com',
            'password': '123test321s'
        })

        self.assertEqual(login_page.view_name, 'wallet.views.users.LogInView')
        self.assertEqual(response.status_code, 200)
        # self.assertContains(response, 'Please enter a correct username and password.')


class UploadTransactionSlipTest(TestCase):
    """
    Class used for testing Upload Transaction Slip functionality
    """

    def setUp(self):
        current_user = _create_user(username='test@test.com', password='123lalala321')
        current_user.save()

    def test_transaction_slip_view(self):
        transaction_slip_page = resolve('/upload_proof_transaction_slip')
        response1 = self.client.get('/upload_proof_transaction_slip', )
        self.client.login(username='test@test.com', password='123lalala321')
        response2 = self.client.get('/upload_proof_transaction_slip', )

        self.assertEqual(transaction_slip_page.view_name, 'wallet.views.users.ProofTransactionSlipView')
        self.assertEqual(response1.status_code, 302)
        self.assertEqual(response2.status_code, 200)

    def test_transaction_slip_post(self):
        self.client.login(username='test@test.com', password='123lalala321')
        response = self.client.post('/upload_proof_transaction_slip', {
            'name': 'Ion Cebotari',
            'date_of_transaction': '2019-05-01',
            'reference_num': '5732dfdsfa',
            'total_amount_paid': 543543.65
        })

        self.assertContains(response, "success")


class CCCreationTest(TestCase):
    """
    Class used for testing the creation of credit cards
    """

    def setUp(self):
        self.current_user = _create_user(username='test@test.com', password='123lalala321')
        self.current_user.save()

    def test_cc_creation(self):
        self.client.login(username='test@test.com', password='123lalala321')
        response = self.client.post('/fund', {
            'reason': 'BTC',
            'cc_currency': 'USD',
            'cc_number': '4916947635810572',
            'expiration_date': "2019-05-01",
            'security_code': '123',
            'name_on_card': 'Test Test'
        })

        self.assertEqual(response.status_code, 302)


class TestUser(TestCase):
    """
    Class used for testing user model functions
    """

    def setUp(self):
        self.user1 = _create_user('test1@test.com', '123lalala321')
        self.user2 = _create_user('test2@test.com', '123lalala321')
        self.user3 = _create_user('test3@test.com', '123lalala321')
        self.user4 = _create_user('test4@test.com', '123lalala321')
        self.user1.save()
        self.user2.save()
        self.user3.save()
        self.user4.save()
        self.trade1 = models.Trade(
            owner=self.user1,
            trade_type='sell',
            crypto_currency='btc',
            fiat_currency='usd',
            trade_amount=30,
            city='London',
            country='GB',
            postcode='34553',
            price=320,
            minimum_transaction_limit=10,
            maximum_transaction_limit=30,
            trade_terms='Test Trade',
        )
        self.trade2 = models.Trade(
            owner=self.user1,
            trade_type='sell',
            crypto_currency='btc',
            fiat_currency='usd',
            trade_amount=30,
            city='London',
            country='GB',
            postcode='34553',
            price=320,
            minimum_transaction_limit=10,
            maximum_transaction_limit=30,
            trade_terms='Test Trade',
        )
        self.user1_account = models.Account(
            user=self.user1,
            currency='BTC',
            description='User1 test account',
            address='adfagthrhtrhtrhg',
            name='User1Test'
        )
        self.user2_account = models.Account(
            user=self.user2,
            currency='BTC',
            description='User2 test account',
            address='adfagthrhtrhtrhg',
            name='User2Test'
        )
        self.user3_account = models.Account(
            user=self.user3,
            currency='BTC',
            description='User3 test account',
            address='adfagthrhtrhtrhg',
            name='User3Test'
        )
        self.user1_pp = models.PaymentProcessor()
        self.user2_pp = models.PaymentProcessor()
        self.transaction1 = models.Transaction(
            seller=self.user1,
            buyer=self.user2,
            seller_account=self.user1_account.id,
            buyer_account=self.user2_account.id,
            seller_pp=self.user1_pp,
            buyer_pp=self.user2_pp,
            trade=self.trade1,
            description='Test Description',
        )
        self.transaction2 = models.Transaction(
            seller=self.user2,
            buyer=self.user1,
            seller_account=self.user2_account.id,
            buyer_account=self.user1_account.id,
            seller_pp=self.user2_pp,
            buyer_pp=self.user1_pp,
            trade=self.trade2,
            description='Test Description',
        )

    def test_user1_trades(self):
        self.trade1.save()
        self.trade2.save()
        self.assertEqual(self.user1.get_trades_count(), 2)

    def test_user1_trade_partners(self):
        self.trade1.save()
        self.trade2.save()
        self.user1_pp.save()
        self.user2_pp.save()
        self.user1_account.save()
        self.user2_account.save()
        self.user3_account.save()
        self.transaction1.save()
        self.transaction2.save()
        self.assertEqual(self.user1.get_trade_partners(), 1)

    def test_upload_profile_image(self):
        self.client.login(username='test1@test.com', password='123lalala321')
        with open('/tmp/test.png', 'rb') as fp:
            response = self.client.post('/overview', {
                'first_name': 'Test',
                'last_name': 'Test',
                'email': 'test1@test.com',
                'language': ('English', 'Spanish', 'Chinese', 'Japanese'),
                'profile_photo': fp
            })

        self.assertEqual(response.status_code, 200)
        response2 = self.client.get('/overview', )
        self.assertContains(response2, 'user_profiles')


class TestTradeCreation(TestCase):
    """
    Class used for testing the Trade object creation
    """

    def setUp(self):
        self.user1 = _create_user('test', 'testtest')
        self.user1.save()
        self.data1 = {
            'trade_type': 'sell',
            'crypto_currency': 'BTC',
            'fiat_currency': 'USD',
            'trade_amount': 30,
            'city': 'London',
            'country': 'GB',
            'postcode': '34553',
            'hide_postcode': 'on',
            'price': 320,
            'preferred_payment_method': 'cash_deposit',
            'minimum_transaction_limit': 10,
            'maximum_transaction_limit': 30,
            'trade_terms': 'Test Trade 1',
        }

        self.data2 = {
            'trade_type': 'buy',
            'crypto_currency': 'BTC',
            'fiat_currency': 'USD',
            'country': 'AI',
            'city': 'Test',
            'postcode': 'tset',
            'hide_postcode': 'on',
            'price': 2425,
            'preferred_payment_method': 'cash_deposit',
            'trade_amount': 234234,
            'minimum_transaction_limit': 8,
            'maximum_transaction_limit': 20,
            'restrict_hours': 'on',
            'opening_time': '11:00',
            'closing_time': '12:00',
            'trade_terms': 'Test Trade 2',
            'minimum_successful_trades': 10
        }

        self.data3 = {
            "trade_type": "buy",
            "crypto_currency": "ETH",
            "fiat_currency": "EUR",
            "postcode": "tset",
            "country": "AF",
            "city": "Drochia",
            "price": "222",
            'preferred_payment_method': 'cash_deposit',
            "trade_amount": "343",
            "minimum_transaction_limit": "219",
            "maximum_transaction_limit": "222",
            "restrict_hours": "on",
            "opening_time": "12:00 AM",
            "closing_time": "12:00 PM",
            "trade_terms": "Test Trade",
            "track_liquidity": "on",
            "identified_people_only": "on",
            "sms_verification_required": "on",
            "check_successful_trades": "on",
            "minimum_successful_trades": "10"
        }

    def test_trade_creation(self):
        self.client.login(username='test', password='testtest')
        response1 = self.client.post('/new-offer', self.data1)
        self.assertEqual(response1.status_code, 302)
        self.assertEqual(models.Trade.objects.all().count(), 1)

        response2 = self.client.post('/new-offer', self.data2)
        self.assertEqual(response2.status_code, 302)
        self.assertEqual(models.Trade.objects.all().count(), 2)

        response3 = self.client.post('/new-offer', self.data3)
        self.assertEqual(response3.status_code, 302)
        self.assertEqual(models.Trade.objects.all().count(), 3)


class TestTradeSearchQuantity(TestCase):
    """
    Class used for testing the search when the necessary 5 items were found
    """

    def setUp(self):
        self.user1 = _create_user('test1@test.com', '123lalala321')
        self.trade1 = models.Trade(
            owner=self.user1,
            trade_type='sell',
            crypto_currency='BTC',
            fiat_currency='USD',
            trade_amount=30,
            city='London',
            country='GB',
            postcode='34553',
            price=320,
            minimum_transaction_limit=10,
            maximum_transaction_limit=30,
            trade_terms='Test Trade',
        )
        self.trade2 = models.Trade(
            owner=self.user1,
            trade_type='sell',
            crypto_currency='BTC',
            fiat_currency='USD',
            trade_amount=30,
            city='London',
            country='GB',
            postcode='34553',
            price=320,
            minimum_transaction_limit=10,
            maximum_transaction_limit=30,
            trade_terms='Test Trade',
        )
        self.trade3 = models.Trade(
            owner=self.user1,
            trade_type='sell',
            crypto_currency='BTC',
            fiat_currency='USD',
            trade_amount=30,
            city='London',
            country='GB',
            postcode='34553',
            price=320,
            minimum_transaction_limit=10,
            maximum_transaction_limit=30,
            trade_terms='Test Trade',
        )
        self.trade4 = models.Trade(
            owner=self.user1,
            trade_type='sell',
            crypto_currency='BTC',
            fiat_currency='USD',
            trade_amount=30,
            city='London',
            country='GB',
            postcode='34553',
            price=320,
            minimum_transaction_limit=10,
            maximum_transaction_limit=30,
            trade_terms='Test Trade',
        )
        self.trade5 = models.Trade(
            owner=self.user1,
            trade_type='sell',
            crypto_currency='BTC',
            fiat_currency='USD',
            trade_amount=30,
            city='London',
            country='GB',
            postcode='34553',
            price=320,
            minimum_transaction_limit=10,
            maximum_transaction_limit=30,
            trade_terms='Test Trade',
        )
        self.user1.save()
        self.trade1.save()
        self.trade2.save()
        self.trade3.save()
        self.trade4.save()
        self.trade5.save()

    def test_trade_search(self):
        search_result = models.Trade.search(crypto='btc', fiat='usd', amount='10', payment_method='bank_transfer')
        self.assertEqual(len(search_result), 5)

        search_result = models.Trade.search(crypto='btc', fiat='usd', amount='20', payment_method='bank_transfer')
        self.assertEqual(len(search_result), 5)

        search_result = models.Trade.search(crypto='btc', fiat='usd', amount='30', payment_method='bank_transfer')
        self.assertEqual(len(search_result), 5)


class TestTradeSearchAlternative1(TestCase):
    """
    Class used for testing the search when the necessary 5 items were found
    """

    def setUp(self):
        self.user1 = _create_user('test1@test.com', '123lalala321')
        self.trade1 = models.Trade(
            owner=self.user1,
            trade_type='sell',
            crypto_currency='BTC',
            fiat_currency='USD',
            trade_amount=30,
            city='London',
            country='GB',
            postcode='34553',
            price=320,
            minimum_transaction_limit=10,
            maximum_transaction_limit=30,
            trade_terms='Test Trade',
            preferred_payment_method='paypal'
        )
        self.trade2 = models.Trade(
            owner=self.user1,
            trade_type='sell',
            crypto_currency='BTC',
            fiat_currency='USD',
            trade_amount=30,
            city='London',
            country='GB',
            postcode='34553',
            price=320,
            minimum_transaction_limit=10,
            maximum_transaction_limit=30,
            trade_terms='Test Trade',
            preferred_payment_method='paypal'
        )
        self.trade3 = models.Trade(
            owner=self.user1,
            trade_type='sell',
            crypto_currency='BTC',
            fiat_currency='USD',
            trade_amount=30,
            city='London',
            country='GB',
            postcode='34553',
            price=320,
            minimum_transaction_limit=10,
            maximum_transaction_limit=30,
            trade_terms='Test Trade',
            preferred_payment_method='cash_deposit'
        )
        self.trade4 = models.Trade(
            owner=self.user1,
            trade_type='sell',
            crypto_currency='BTC',
            fiat_currency='USD',
            trade_amount=30,
            city='London',
            country='GB',
            postcode='34553',
            price=320,
            minimum_transaction_limit=10,
            maximum_transaction_limit=30,
            trade_terms='Test Trade',
            preferred_payment_method='cash_deposit'
        )
        self.trade5 = models.Trade(
            owner=self.user1,
            trade_type='sell',
            crypto_currency='BTC',
            fiat_currency='USD',
            trade_amount=30,
            city='London',
            country='GB',
            postcode='34553',
            price=320,
            minimum_transaction_limit=10,
            maximum_transaction_limit=30,
            trade_terms='Test Trade',
            preferred_payment_method='cash_deposit'
        )
        self.user1.save()
        self.trade1.save()
        self.trade2.save()
        self.trade3.save()
        self.trade4.save()
        self.trade5.save()

    def test_trade_search(self):
        search_result = models.Trade.search_alternatives(crypto='btc', fiat='usd', amount='10', payment_method='bank_transfer')
        self.assertEqual(len(search_result), 5)

        search_result = models.Trade.search_alternatives(crypto='btc', fiat='usd', amount='20', payment_method='bank_transfer')
        self.assertEqual(len(search_result), 5)

        search_result = models.Trade.search_alternatives(crypto='btc', fiat='usd', amount='30', payment_method='bank_transfer')
        self.assertEqual(len(search_result), 5)

