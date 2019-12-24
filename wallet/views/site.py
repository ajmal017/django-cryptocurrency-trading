import logging

from django.shortcuts import render, render_to_response
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin

from wallet import models

logger = logging.getLogger('raplev')
logger.setLevel(logging.INFO)


def handler404(request, exception, template_name="404-error.html"):
    response = render_to_response("404-error.html")
    response.status_code = 404
    return response


class ContactView(View):
    """
    View class for the contact page
    """

    def get(self, request):
        return render(request, 'contact.html')


class DisputCenterView(LoginRequiredMixin, View):
    """
    View class for the disput_center page
    """

    def get(self, request):
        return render(request, 'support-center.html')


class FaqView(View):
    """
    View class for the faq page
    """

    def get(self, request):
        return render(request, 'faq.html')


class IndexView(View):
    """
    View class for the index page
    """

    def get(self, request):
        btc_trades = models.Trade.get_n_newest_trades(4, 'BTC')
        eth_trades = models.Trade.get_n_newest_trades(4, 'ETH')
        xrp_trades = models.Trade.get_n_newest_trades(4, 'XRP')
        return render(request, 'index.html', {'btc': btc_trades, 'eth': eth_trades, 'xrp': xrp_trades})


class MessagesView(LoginRequiredMixin, View):
    """
    View class for the messages page
    """

    def get(self, request):
        return render(request, 'messages.html')


class SupportView(LoginRequiredMixin, View):
    """
    View class for the support page
    """

    def get(self, request):
        return render(request, 'support.html')


class SubmitView(LoginRequiredMixin, View):
    """
    View class for the submit page
    """

    def get(self, request):
        return render(request, 'submit-ticket.html')
