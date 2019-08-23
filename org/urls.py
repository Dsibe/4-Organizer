from django.urls import path, include
from django.contrib import admin
from django.urls import path
from django.urls import reverse
from main.views import *

urlpatterns = [
    path(r'', start, name="start"),
    path('key/<str:id>/<str:id2>/<str:license>/<str:email>/', key, name="key"),
    path('install/', install, name="install"),
    path('lottery/', lottery, name="lottery"),
    path('lottery-prize/<str:prize>/', lottery_prize, name="lottery-prize"),
    path('select-scan/', select_scan, name="select-scan"),
    path('paypal/', include('paypal.standard.ipn.urls')),
    path('buy/', buy, name='buy'),
    path('terms/', terms, name='terms'),
    path('payment-done/', payment_done, name='payment_done'),
    path('payment-cancelled/', payment_canceled, name='payment_cancelled'),
    path('contact-us/', contact_us, name="contact-us"),
    path('description/', description, name="description"),
    path('main/', main, name="main"),
    path(r'main/', main, name="main"),
    path('support', support, name="support"),
    path('admin/', admin.site.urls),
]
