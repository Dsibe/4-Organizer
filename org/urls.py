from django.urls import path, include
from django.contrib import admin
from django.urls import path
from django.urls import reverse
from main.views import *
from django.contrib.auth import views as auth_views
from users.models import *
from users.views import *

urlpatterns = [
    path(r'', start, name="start"),
    path('key/<str:id>/<str:id2>/<str:license>/<str:username>/',
         key,
         name="key"),
    path('install/', install, name="install"),
    path('select-scan/', select_scan, name="select-scan"),
    path('paypal/', include('paypal.standard.ipn.urls')),
    path('register/<str:period_selected>/', register, name='register'),
    path('terms/', terms, name='terms'),
    path('mail/', mail),
    path('payment-done/', payment_done, name='payment_done'),
    path('payment-cancelled/', payment_canceled, name='payment_cancelled'),
    path('contact-us/', contact_us, name="contact-us"),
    path('pricing/', pricing, name="pricing"),
    path('main/', main, name="main"),
    path('support', support, name="support"),
    path('admin/', admin.site.urls),
    path('login/',
         auth_views.LoginView.as_view(template_name='main/login.html'),
         name='login'),
    path('logout/',
         auth_views.LogoutView.as_view(template_name='main/logout.html'),
         name='logout'),
    path('profile/', profile, name='profile'),
]
