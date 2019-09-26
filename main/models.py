from django.db import models


class Key(models.Model):
    key = models.CharField(max_length=300, null=True, blank=True)
    date = models.CharField(max_length=100, null=True, blank=True)
    period = models.CharField(max_length=50, null=True, blank=True)
    email = models.CharField(max_length=300, null=True, blank=True)
    fullname = models.CharField(max_length=500, null=True, blank=True)

    def __str__(self):
        return str(self.key)

    def save(self, *args, **kwargs):
        if self.email:
            self.email = self.email.lower()
        if self.fullname:
            self.fullname = self.fullname.lower()
        # print(self.email, self.period, self.key, self.date)
        super(Key, self).save(*args, **kwargs)


class Email(models.Model):
    email = models.CharField(max_length=400, null=True, blank=True)

    def __str__(self):
        return str(self.email)

    def save(self, *args, **kwargs):
        if self.email:
            self.email = self.email.lower()

        # print(self.email)
        super(Email, self).save(*args, **kwargs)
