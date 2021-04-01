from django.db import models
from users.models import *


class Email(models.Model):
    email = models.CharField(max_length=400, null=True, blank=True)

    def __str__(self):
        return str(self.email)

    def save(self, *args, **kwargs):
        if self.email:
            self.email = self.email.lower()

        super(Email, self).save(*args, **kwargs)
