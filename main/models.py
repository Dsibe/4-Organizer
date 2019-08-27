from django.db import models

# Create your models here.

class Key(models.Model):
    key = models.CharField(max_length=300, null=True, blank=True)
    date = models.CharField(max_length=100, null=True, blank=True)
    period = models.CharField(max_length=50, null=True, blank=True)
    email = models.CharField(max_length=300, null=True, blank=True)

    def __str__(self):
        return str(self.key)

    def save(self, *args, **kwargs):
        self.key = self.key.lower()
        self.email = self.email.lower()
        super(Key, self).save(*args, **kwargs)
