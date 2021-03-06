import logging

from oscar.core.loading import get_model
from oscar.apps.checkout.views import PaymentDetailsView as OscarPaymentDetailsView

from apps.core.facade import PaymentFacade
from apps.core.util import crypto_to_fiat


Order = get_model('order', 'Order')
Source = get_model('payment', 'Source')
SourceType = get_model('payment', 'SourceType')


logger = logging.getLogger('ccstore')


class PaymentDetailsView(OscarPaymentDetailsView):
    def submit(self, **kwargs):
        try:
            payment = kwargs.pop('payment')
        except KeyError:
            payment = None
        if payment:
            logger.info('Payment #{} order submitted.'.format(payment.id))
        return super().submit(**kwargs)

    def handle_place_order_submission(self, request):
        submission = self.build_submission()
        payment = self.get_context_data()['payment']
        logger.info('Payment #{} order submission.'.format(payment.id))
        payment.check_payment(save=False)
        if payment.status == 'expired':
            logger.info('Payment #{} order expired.'.format(payment.id))
            payment.save()
        return self.submit(**submission)

    def handle_payment(self, order_number, total, **kwargs):
        payment = PaymentFacade().check_order_payment(order_number, self.request.user)
        source_type, created = SourceType.objects.get_or_create(name='ccstore')
        currency = self.request.basket.currency
        source = Source(
            source_type=source_type,
            currency=currency,
            amount_allocated=crypto_to_fiat(payment.amount),
            amount_debited=total.incl_tax,
            reference=payment.id
        )
        self.add_payment_source(source)
        self.add_payment_event('purchase', total.incl_tax)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        basket = self.request.basket
        order_number = self.get_order_number(basket)
        ctx['payment'] = self.get_payment_object(basket, order_number, user=self.request.user)
        return ctx
