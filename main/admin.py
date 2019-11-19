from django.contrib import admin
from .models import *
from users.models import *

admin.site.register(Key)
admin.site.register(Profile)
