from django.db import models
from users.models import *


class Key(models.Model):
    key = models.CharField(max_length=300, null=True, blank=True)
    date = models.CharField(max_length=100, null=True, blank=True)
    period = models.CharField(max_length=50, null=True, blank=True)
    profile = models.OneToOneField(Profile,
                                   null=True,
                                   blank=True,
                                   on_delete=models.CASCADE)

    def __str__(self):
        return str(self.key)


class Email(models.Model):
    email = models.CharField(max_length=400, null=True, blank=True)

    def __str__(self):
        return str(self.email)

    def save(self, *args, **kwargs):
        if self.email:
            self.email = self.email.lower()

        # print(self.email)
        super(Email, self).save(*args, **kwargs)
