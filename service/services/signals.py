from django.conf import settings
from django.core.cache import cache
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from services.models import Subscription, Plan, Service


@receiver(post_save, sender=Service)
@receiver(post_save, sender=Plan)
@receiver(post_save, sender=Subscription)
@receiver(post_delete, sender=Service)
@receiver(post_delete, sender=Plan)
@receiver(post_delete, sender=Subscription)
def reset_total_amount_cache(sender, instance, **kwargs):
    """
    Clear total_amount cache if any Subscription,
    PLan or Service object was deleted
    """
    cache.delete(settings.TOTAL_AMOUNT_CACHE_NAME)
