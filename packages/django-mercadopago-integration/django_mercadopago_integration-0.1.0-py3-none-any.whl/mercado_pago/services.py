import hashlib
import hmac
from abc import ABC
from datetime import timedelta
from urllib.parse import quote

import requests
from django.conf import settings
from django.core.cache import cache
from django.utils import timezone


class MercadoPagoBase(ABC):
    @staticmethod
    def get_setting(key, default=None):
        return getattr(settings, key, default)

    @classmethod
    def generate_token(cls, user):
        """
        Default token generator. Override this in a subclass or inject your own class if needed.
        """
        from django.utils.crypto import get_random_string
        from django.utils import timezone
        from datetime import timedelta

        token = get_random_string(30)
        expires_at = timezone.now() + timedelta(hours=4)

        # Example return structure. You can adapt it to your base system.
        return {
            "token": token,
            "expires_at": expires_at,
        }

    @classmethod
    def register_application_link(cls, user, front_redirect_url, company_id):
        token_data = cls.generate_token(user)
        token = token_data["token"]

        cache.set(token, {'company_id': company_id, 'front_redirect_url': front_redirect_url}, timeout=6000)
        encoded_callback_uri = quote(cls.get_setting("MERCADO_PAGO_REDIRECT_URI", ""), safe='')

        auth_url = (
            f"https://auth.mercadopago.com/authorization"
            f"?client_id={cls.get_setting('MERCADO_PAGO_CLIENT_ID')}"
            f"&response_type=code"
            f"&platform_id=mp"
            f"&redirect_uri={encoded_callback_uri}"
            f"&scope=offline_access"
            f"&state={token}"
        )
        return auth_url

    @staticmethod
    def register_application_callback(code, user):
        data = {
            'grant_type': 'authorization_code',
            'client_id': settings.MERCADO_PAGO_CLIENT_ID,
            'client_secret': settings.MERCADO_PAGO_CLIENT_SECRET,
            'code': code,
            'redirect_uri': settings.MERCADO_PAGO_REDIRECT_URI,
        }
        try:
            response = requests.post('https://api.mercadopago.com/oauth/token', data=data)
            response.raise_for_status()
            tokens = response.json()
            mp_account, created = MercadoPagoAccount.objects.get_or_create(mercado_pago_user_id=tokens.get('user_id'))
            mp_account.access_token = tokens.get('access_token')
            mp_account.refresh_token = tokens.get('refresh_token')
            mp_account.expires_at = timezone.now() + timedelta(seconds=tokens.get('expires_in', 0))
            mp_account.save()

            mp_account.users.add(user)
            return mp_account
        except requests.exceptions.RequestException as e:
            return {'error': str(e.response.json())}

    @staticmethod
    def create_split_payment(mp_account, payment_id, payment_title, amount, buyer_email, fee_percentage, metadata=None,
                             back_urls=None):
        """Create a new split payment on the specified account with the fee applied to the principal account"""
        payment_data = {
            "items": [
                {
                    "id": payment_id,
                    "title": payment_title,
                    "quantity": 1,
                    "currency_id": "UYU",
                    "unit_price": amount
                }
            ],
            "marketplace_fee": amount * (fee_percentage / 100),
            "payer": {
                "email": buyer_email
            },
            "notification_url": f"{settings.BASE_BACKEND_URL}/mercado_pago/notifications/",
            "auto_return": "approved"
        }
        if metadata:
            payment_data["metadata"] = metadata
        if back_urls:
            payment_data["back_urls"] = back_urls

        headers = {
            "Authorization": f"Bearer {mp_account.access_token}",
            "Content-Type": "application/json",
        }

        try:
            response = requests.post('https://api.mercadopago.com/checkout/preferences', headers=headers,
                                     json=payment_data)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {'error': str(e.response.json())}

    @staticmethod
    def check_mp_signature(request):
        try:
            x_signature = request.headers['x-signature']
            x_request_id = request.headers['x-request-id']
            data_id = request.query_params.get("data.id")
            if data_id is None:
                data_id = request.query_params.get("id")
            secret_key = settings.MERCADO_PAGO_WEBHOOKS_SECRET_KEY

            parts = dict(part.split('=') for part in x_signature.split(','))
            ts, received_signature = parts['ts'], parts['v1']

            msg = f"id:{data_id};request-id:{x_request_id};ts:{ts};"
            expected_signature = hmac.new(
                secret_key.encode(), msg.encode(), hashlib.sha256
            ).hexdigest()

            return hmac.compare_digest(expected_signature, received_signature)

        except (KeyError, ValueError):
            return False

    @staticmethod
    def create_main_app_payment(amount, buyer_email=None, back_urls=None):
        """Create a new payment for the principal account"""

        preference_data = {
            "items": [
                {
                    "title": "Monthly Subscription",
                    "quantity": 1,
                    "unit_price": amount,
                    "currency_id": "UYU"
                }
            ],
            "payer": {
                "email": buyer_email or "default@example.com"
            },
            "notification_url": f"{settings.BASE_BACKEND_URL}/mercado_pago/notifications/"
        }

        if back_urls:
            preference_data["back_urls"] = back_urls
            preference_data["auto_return"] = "approved"

        headers = {
            "Authorization": f"Bearer {settings.MERCADO_PAGO_ACCESS_TOKEN}",
            "Content-Type": "application/json",
        }

        try:
            response = requests.post(
                "https://api.mercadopago.com/checkout/preferences",
                headers=headers,
                json=preference_data
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {'error': str(e), 'details': e.response.json() if e.response else "No response"}


class MercadoPagoService(MercadoPagoBase):
    @staticmethod
    def generate_token(user):
        token = VerificationToken.generate_token_for_user(user, VerificationToken.Type.MERCADO_PAGO)
        return token.token
