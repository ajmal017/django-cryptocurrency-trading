from wallet.models import ProofTransactionSlip
from django.contrib.auth.mixins import UserPassesTestMixin


class TransactionSlipRequiredMixin(UserPassesTestMixin):
    """
    A mixin used for redirecting the user to the Transaction Slip Upload page in case he doesn't have it
    """

    def test_func(self):
        """
        :return: True is user is authenticated and already has a ProofTransactionSlip, False otherwise
        """

        if self.request.user.is_authenticated:
            self.login_url = '/upload_proof_transaction_slip'
            try:
                ProofTransactionSlip.objects.get(User=self.request.user)
                return True
            except ProofTransactionSlip.DoesNotExist:
                return False
        self.login_url = '/index'
        return False
