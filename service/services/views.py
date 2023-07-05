from django.db.models import Prefetch, F, Sum
from rest_framework.viewsets import ReadOnlyModelViewSet

from clients.models import Client
from services.models import Subscription
from services.serializers import SubscriptionSerializer


class SubscriptionView(ReadOnlyModelViewSet):
    queryset = Subscription.objects.all() \
        .prefetch_related('plan', 'service',
                          Prefetch(queryset=Client.objects.all().select_related('user')
                                   .only('user__email', 'user__username', 'company_name'), lookup='client'))
    serializer_class = SubscriptionSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        response = super().list(request, *args, **kwargs)

        response_data = dict()
        response_data['result'] = response.data
        response_data['total_amount'] = queryset.aggregate(total_amount=Sum('full_price_with_discount')) \
            .get('total_amount')
        response.data = response_data
        return response
