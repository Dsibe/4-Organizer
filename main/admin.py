from django.contrib import admin
# from .models import *
from sellapp.models import License
from users.models import *
from blog.models import Post

admin.site.register(License)
admin.site.register(Post)
