from django.core.validators import MaxValueValidator
from django.db import models

from clients.models import Client
from .tasks import *


class Service(models.Model):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__full_price = self.full_price

    name = models.CharField('Name', max_length=50)
    full_price = models.PositiveIntegerField('Full_price', validators=[
        MaxValueValidator(10**9)
    ])

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.__full_price != self.full_price:
            set_full_price_with_discount_with_service_id.delay(self.pk)
            self.__full_price = self.full_price


class Plan(models.Model):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__discount_percent = self.discount_percent

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

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.__discount_percent != self.discount_percent:
            set_full_price_with_discount_with_plan_id.delay(self.pk)
            self.__old_discount_percent = self.discount_percent


class Subscription(models.Model):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__plan = None
        self.__service = None

    client = models.ForeignKey(Client, related_name='subscriptions',
                               on_delete=models.PROTECT, verbose_name='client')
    service = models.ForeignKey(Service, related_name='subscriptions',
                                on_delete=models.PROTECT, verbose_name='Service')
    plan = models.ForeignKey(Plan, related_name='subscriptions',
                             on_delete=models.PROTECT, verbose_name='subscriptions')
    full_price_with_discount = models.DecimalField('Full_price_with_discount', max_digits=9,
                                                   decimal_places=2, default=0)

    def save(self, *args, **kwargs):
        creating = not self.pk
        super().save(*args, **kwargs)
        if creating or self.__plan != self.plan or self.__service != self.service:
            set_price_with_discount.delay(self.pk)
            self.__plan = self.plan
            self.__service = self.service
