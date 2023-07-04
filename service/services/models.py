from django.core.validators import MaxValueValidator
from django.db import models

from clients.models import Client


class Service(models.Model):
    name = models.CharField('Name', max_length=50)
    full_price = models.PositiveIntegerField('Full_price')


class Plan(models.Model):
    PLAN_TYPES = (
        ('full', 'Full'),
        ('student', 'Student'),
        ('discount', 'Discount')
    )

    plan_type = models.CharField('PLan types', choices=PLAN_TYPES,
                                 max_length=10)
    discount_percent = models.PositiveSmallIntegerField('Discount_percent', default=0,
                                                        validators=[
                                                            MaxValueValidator(100)])


class Subscription(models.Model):
    client = models.ForeignKey(Client, related_name='subscriptions',
                               on_delete=models.PROTECT, verbose_name='client')
    service = models.ForeignKey(Service, related_name='subscriptions',
                                on_delete=models.PROTECT, verbose_name='Service')
    plan = models.ForeignKey(Plan, related_name='subscriptions',
                             on_delete=models.PROTECT, verbose_name='subscriptions')
