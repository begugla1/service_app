from django.db.models import Prefetch
from rest_framework.viewsets import ReadOnlyModelViewSet

from clients.models import Client
from services.models import Subscription
from services.serializers import SubscriptionSerializer


class SubscriptionView(ReadOnlyModelViewSet):
    queryset = Subscription.objects.all() \
        .select_related('service', 'plan') \
        .prefetch_related(Prefetch(
            queryset=Client.objects.all().select_related('user') \
            .only('user__email', 'user__username', 'company_name'),
            lookup='client'
        ))
    serializer_class = SubscriptionSerializer
