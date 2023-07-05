from celery import shared_task
from django.db.models import F, Subquery, OuterRef
from celery_singleton import Singleton


@shared_task(base=Singleton)
def set_full_price_with_discount_with_plan_id(plan_id):
    from services.models import Subscription

    Subscription.objects.filter(plan_id=plan_id).update(
        full_price_with_discount=Subquery(
            Subscription.objects.filter(
                id=OuterRef('id')
            ).annotate(
                annotated_price=(F('service__full_price') -
                                 F('service__full_price') * F('plan__discount_percent') / 100)
            ).values('annotated_price')[0:1]
        )
    )


@shared_task(base=Singleton)
def set_full_price_with_discount_with_service_id(service_id):
    from services.models import Subscription

    Subscription.objects.filter(service_id=service_id).update(
        full_price_with_discount=Subquery(
            Subscription.objects.filter(
                id=OuterRef('id')
            ).annotate(
                annotated_price=(F('service__full_price') -
                                 F('service__full_price') * F('plan__discount_percent') / 100)
            ).values('annotated_price')[0:1]
        )
    )
