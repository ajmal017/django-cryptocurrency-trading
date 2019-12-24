import logging

from django.views import View
from django.http import JsonResponse, HttpResponseBadRequest

from django.core.paginator import Paginator
from wallet import models
from wallet.cache import CurrencyExchangeData

logger = logging.getLogger('raplev')
logger.setLevel(logging.INFO)


class ExchangeRateView(View):
    """
    Class used for getting the current exchange rates for crypto
    """

    def get(self, request, currencies):
        valid_currencies = ('usd', 'eur', 'gbp', 'jpy', 'btc', 'eth', 'xrp')
        c1 = currencies[:3]
        c2 = currencies[4:]
        if c1 not in valid_currencies or c2 not in valid_currencies:
            return JsonResponse({'error': 'Invalid currency'})
        else:
            return JsonResponse(CurrencyExchangeData.get_or_set_rate(c1, c2))


class TradeDataView(View):
    """
    View used for feeding the /buy and /sell pages with
    """

    def get(self, request, operation):
        if operation not in ('buy', 'sell'):
            return HttpResponseBadRequest('Invalid operation. Valid operations: buy, sell')
        if not request.GET:
            trades = models.Trade.objects.filter(trade_type=operation).values()
            results_status = True
        elif request.GET.get('crypto', ) and not (request.GET.get('fiat', ) and request.GET.get('amount', ) and
                                                  request.GET.get('payment_method', )):
            trades = models.Trade.objects.filter(trade_type=operation).filter(crypto_currency=request.GET['crypto'].
                                                                              upper()).values()
            results_status = True
        else:
            parameters = {
                'crypto': request.GET.get('crypto', ),
                'fiat': request.GET.get('fiat', ),
                'amount': request.GET.get('amount', ),
                'payment_method': request.GET.get('payment_method', ),
            }
            valid_parameters = {
                'crypto': ['btc', 'eth', 'xrp'],
                'fiat': ['usd', 'eur', 'gbp', 'jpy'],
            }
            for parameter, value in parameters.items():
                if valid_parameters.get(parameter) and value not in valid_parameters.get(parameter):
                    return HttpResponseBadRequest('Invalid value for {}'.format(parameter))
            trades = models.Trade.search(**parameters)
            results_status = True
            if not trades:
                trades = models.Trade.search_alternatives(**parameters)
                results_status = False
        page = request.GET.get('page', )
        paginator = Paginator(trades, 20)
        current_posts = paginator.get_page(page)
        return JsonResponse({
            'status': results_status,
            'current_page': page,
            'total_pages': paginator.num_pages,
            'values': list(current_posts)
        })
