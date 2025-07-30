from rest_framework import serializers


class MercadoPagoCallbackSerializer(serializers.Serializer):
    code = serializers.CharField()
    state = serializers.CharField()


class SchedulePaymentSerializer(serializers.Serializer):
    email = serializers.EmailField()
    phone = serializers.CharField()
    name = serializers.CharField()
    schedule_id = serializers.IntegerField()
    back_urls = serializers.DictField(child=serializers.URLField())


class MercadoPagoAccountRegisterSerializer(serializers.Serializer):
    redirect_url = serializers.URLField()
