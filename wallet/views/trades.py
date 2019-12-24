import logging

from django.http import Http404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.shortcuts import render, redirect

from wallet import forms, models
from wallet.cache import GoogleMapsGeocoding


logger = logging.getLogger('raplev')
logger.setLevel(logging.INFO)


class AllOffersView(View):
    """
    View class for all-offers page
    """
    def get(self, request):
        return render(request, 'all-offers.html')


class BuyView(View):
    """
    View class for the buy page
    """

    def get(self, request):
        return render(request, 'buy.html')


class InitiateTradeView(View):
    """
    View class for the initiate-trade page
    """

    def get(self, request):
        return render(request, 'initiate-trade.html')


class OfferActivityView(View):
    """
    View class for offer-activity page
    """

    def get(self, request):
        return render(request, 'offer-activity.html')


class OfferProcessView(View):
    """
    View class for ofer-process page
    """

    def get(self, request):
        return render(request, 'offer-process.html')


class OfferWaitingView(View):
    """
    View class for ofer-waiting page
    """

    def get(self, request):
        return render(request, 'offer-waiting.html')


class OffersView(LoginRequiredMixin, View):
    """
    View class for the offers page
    """

    def get(self, request):
        return render(request, 'offers.html')


class ReceiveView(LoginRequiredMixin, View):
    """
    View class for the receive page
    """

    def get(self, request):
        return render(request, 'receive.html')


class SellDetailsView(LoginRequiredMixin, View):
    """
    View class for the sell_details page
    """

    def get(self, request):
        return render(request, 'sell-details.html')


class SellView(View):
    """
    View class for the sell page
    """

    def get(self, request):
        return render(request, 'sell.html')


class TradeView(LoginRequiredMixin, View):
    """
    View class for the trade page
    """

    def get(self, request):
        form = forms.NewTradeForm()
        return render(request, 'new-offer.html', {'trade_form': form})

    def post(self, request):
        form = forms.NewTradeForm(request.POST)
        if form.is_valid():
            new_trade = form.save(commit=False)
            new_trade.owner = request.user
            new_trade.save()
            logger.info('Saved trade: {}'.format(vars(new_trade)))
            return redirect('/trade')
        else:
            logger.info('Form errors: {}'.format(form.errors))
            return render(request, 'new-offer.html', {'trade_form': form})


class SingleTradeDetailsView(View):
    """
    View used for the deposits and withdrawals page
    """

    def get(self, request, trade_id):
        try:
            current_trade = models.Trade.objects.get(pk=trade_id)
        except:
            raise Http404()

        geolocation = GoogleMapsGeocoding().get_or_set_location(
            country=current_trade.country.name,
            city=current_trade.city,
            postcode=current_trade.postcode
        )
        return render(request, 'single-trade-details.html', {'trade': current_trade, 'location': geolocation})


class TradeDetailsView(View):
    """
    View used for the deposits and withdrawals page
    """

    def get(self, request):
        return render(request, 'trade-details.html')


class SendOfferView(View):
    """
    View used for the send-offer page
    """

    def get(self, request):
        return render(request, 'send-offer-form.html')


class TradeCompletedView(View):
    """
    View used for the trade-completed page
    """

    def get(self, request):
        return render(request, 'trade-completed.html')
