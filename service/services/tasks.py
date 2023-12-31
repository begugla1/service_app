import datetime
from celery import shared_task

from django.db import transaction
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


@shared_task(base=Singleton)
def set_price_with_discount(subscription_id):
    from services.models import Subscription

    with transaction.atomic():

        subscription = Subscription.objects.select_for_update().filter(id=subscription_id) \
            .annotate(annotated_price=(F('service__full_price') -
                                       F('service__full_price') * F('plan__discount_percent') / 100))[0]

        subscription.full_price_with_discount = subscription.annotated_price
        subscription.save()


@shared_task(base=Singleton)
def set_comment(subscription_id):
    from services.models import Subscription

    with transaction.atomic():

        subscription = Subscription.objects.select_for_update() \
            .get(id=subscription_id)

        subscription.comment = str(datetime.datetime.now())
        subscription.save()
