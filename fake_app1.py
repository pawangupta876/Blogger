import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'jarvis.settings')


import django
django.setup()

import random
from App1.models import User
from faker import Faker

fake = Faker()

def fun(n=5):

    for i in range(n):
        first_name = fake.first_name()
        last_name = fake.last_name()
        email= fake.email()
        t =User.objects.get_or_create(first_name=first_name, last_name=last_name, email=email)[0]
        t.save()

if __name__ == '__main__':
    fun(10)
