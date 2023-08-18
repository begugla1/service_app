from django.db.models import Prefetch, Sum
from rest_framework.viewsets import ReadOnlyModelViewSet
from django.core.cache import cache

from clients.models import Client
from django.conf import settings
from services.models import Subscription
from services.serializers import SubscriptionSerializer


class SubscriptionView(ReadOnlyModelViewSet):
    queryset = Subscription.objects.all().prefetch_related(
        "plan",
        "service",
        Prefetch(
            queryset=Client.objects.all()
            .select_related("user")
            .only("user__email", "user__username", "company_name"),
            lookup="client",
        ),
    )
    serializer_class = SubscriptionSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        response = super().list(request, *args, **kwargs)

        total_amount_cache = cache.get(settings.TOTAL_AMOUNT_CACHE_NAME)

        if total_amount_cache:
            total_amount = total_amount_cache
        else:
            total_amount = queryset.aggregate(
                total_amount=Sum("full_price_with_discount")
            ).get("total_amount")
            cache.set(settings.TOTAL_AMOUNT_CACHE_NAME, total_amount, 60**2)

        response_data = {"result": response.data, "total_amount": total_amount}
        response.data = response_data
        return response
