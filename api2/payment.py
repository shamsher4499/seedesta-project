import stripe
from django.conf import settings
from django.http import JsonResponse
from django.views import View
from .models import Goal

stripe.api_key = settings.STRIPE_SECRET_KEY

class PaymentView(View):
    def post(self, request, *args, **kwargs):
        amount = Goal.objects.get(id=self.kwargs["pk"])
        YOUR_DOMAIN = "http://127.0.0.1:8000"  # change in production
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[
                {
                    'amount': amount.stripe_price_id,
                    'quantity': 1,
                },
            ],
            mode='payment',
            success_url=YOUR_DOMAIN + '/success/',
            cancel_url=YOUR_DOMAIN + '/cancel/',
        )
        return redirect(checkout_session.url)