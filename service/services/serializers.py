from rest_framework import serializers

from services.models import Subscription


class SubscriptionSerializer(serializers.ModelSerializer):
    client_username = serializers.CharField(source='client.user.username',
                                            max_length=255)
    client_company_name = serializers.CharField(source='client.company_name',
                                                max_length=111)
    client_email = serializers.CharField(source='client.user.email',
                                         max_length=255)
    plan = serializers.CharField(source='plan.plan_type',
                                 max_length=10)
    service_name = serializers.CharField(source='service.name',
                                         max_length=50)
    service_full_price = serializers.IntegerField(source='service.full_price')

    class Meta:
        model = Subscription
        fields = ('id', 'plan_id', 'plan', 'client_username',
                  'client_company_name', 'client_email',
                  'service_name', 'service_full_price')
