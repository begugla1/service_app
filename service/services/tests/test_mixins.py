from django.contrib.auth.models import User
from django.urls import reverse_lazy

from clients.models import Client
from services.models import Service, Plan, Subscription


class MainApiTestMixin:

    def setUp(self):
        self.user1 = User.objects.create(username='test_username1',
                                         email="yokimokiadmin@gmail.com")
        self.client1 = Client.objects.create(user=self.user1, company_name='Amazon',
                                             full_address='Amazon shop')
        self.service1 = Service.objects.create(name='YouTube Premium', full_price=1000)
        self.plan1 = Plan.objects.create(plan_type='student', discount_percent=65)
        self.subscription1 = Subscription.objects.create(client=self.client1, plan=self.plan1,
                                                         service=self.service1)
        self.url = reverse_lazy('subscription-list')
