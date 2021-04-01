from django.utils import timezone
from django.db import models
from django.contrib.auth.models import User

import uuid
import datetime


class License(models.Model):
    key = models.CharField(max_length=40, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True)
    additional_info = models.CharField(max_length=1000, blank=True)

    expiration = models.IntegerField(default=0)
    is_custom = models.BooleanField(default=False)
    creation_date = models.DateField('Date created', blank=True)

    max_machines_limit = models.IntegerField(default=3)

    def create_key(self):
        self.key = str(uuid.uuid4())
        self.save()


class Machine(models.Model):
    hardware_id = models.CharField(max_length=1000, blank=True)
    info = models.CharField(max_length=1000, blank=True)
    model = models.CharField(max_length=1000, blank=True)
    last_login = models.DateTimeField('Last login time', blank=True)
    license = models.ForeignKey(License,
                                on_delete=models.CASCADE,
                                blank=True,
                                null=True)
    is_blacklisted = models.BooleanField(default=False)

    def update_last_login_time(self):
        self.last_login = timezone.now()
        self.save()

    def create_machine(self, hardware_id, info, model, is_blacklisted,
                       license):
        self.hardware_id = hardware_id
        self.info = info
        self.model = model
        self.last_login = timezone.now()
        self.is_blacklisted = is_blacklisted
        self.license = license
        self.save()
