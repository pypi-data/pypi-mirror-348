from django.db import models


class MercadoPagoAccount(models.Model):
    mercado_pago_user_id = models.CharField(max_length=255, null=True, blank=True)
    access_token = models.CharField(max_length=255, null=True, blank=True)
    refresh_token = models.CharField(max_length=255, null=True, blank=True)
    expires_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f'MercadoPagoAccount for {self.mercado_pago_user_id}'
