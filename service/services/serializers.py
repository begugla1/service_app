from rest_framework import serializers

from services.models import Subscription, Plan


class PlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plan
        fields = '__all__'


class SubscriptionSerializer(serializers.ModelSerializer):
    client_username = serializers.CharField(source='client.user.username',
                                            max_length=255)
    client_company_name = serializers.CharField(source='client.company_name',
                                                max_length=111)
    client_email = serializers.CharField(source='client.user.email',
                                         max_length=255)
    plan = PlanSerializer()
    # service_name = serializers.CharField(source='service.name',
    #                                      max_length=50)
    # service_full_price = serializers.IntegerField(source='service.full_price')

    class Meta:
        model = Subscription
        fields = ('id', 'plan', 'client_username',
                  'client_company_name', 'client_email',
                  # 'service_name', 'service_full_price',
                  'full_price_with_discount')
