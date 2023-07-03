from django.contrib.auth.models import User
from django.db import models


class Client(models.Model):
    user = models.OneToOneField(User, on_delete=models.PROTECT,
                                verbose_name='User')
    company_name = models.CharField('Company name', max_length=111)
    full_address = models.CharField('Address', max_length=255)

    def __str__(self):
        return f'{self.user} in company {self.company_name}'
