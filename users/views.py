from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.template import Context, Template
from django.contrib.auth.models import User
from random import randint
import calendar
from .models import *
import datetime
from django.urls import reverse
from django.contrib.auth import views as auth_views
from .forms import *
from paypal.standard.models import ST_PP_COMPLETED
from paypal.standard.ipn.signals import valid_ipn_received, invalid_ipn_received
from django.core.mail import send_mail
from django.conf import settings
from decimal import Decimal
from main.models import *
from paypal.standard.forms import PayPalPaymentsForm


def int_from_date(date):
    current_date_edit = ''
    for i in date:
        if i != '-':
            current_date_edit += i
    date = current_date_edit
    return int(date)



def add_months(sourcedate, months):
    month = sourcedate.month - 1 + months
    year = sourcedate.year + month // 12
    month = month % 12 + 1
    day = min(sourcedate.day, calendar.monthrange(year,month)[1])
    return datetime.date(year, month, day)


@login_required
def profile(request):
    if request.method == "GET":
        user = request.user
        user_profile = Profile.objects.get(user=user)
        key_obj = user_profile.key
        if key_obj.key == None:
            period = key_obj.period
            print(period)
            host = request.get_host()

            if period == '1':
                price = '4.99'
            elif period == '3':
                price = '12.99'
            elif period == '6':
                price = '19.99'
            elif period == '12':
                price = '24.99'
            elif period == '0':
                price = '499.99'

            print(period, price)
            if period == '0':
                period_paypal = 'forever'
            else:
                period_paypal = period + ' months'
            paypal_dict = {
                "business": 'abt.company@aol.com',
                "amount": price,
                "item_name": f"4-Organizer {period_paypal}",
                "currency_code": "USD",
                "invoice": f"{randint(1, 9999999)}",
                "notify_url": "http://{}{}".format(host, reverse("paypal-ipn")),
                "return_url": "http://{}{}".format(host, reverse("payment_done")),
                "cancel_return": "http://{}{}".format(host, reverse("payment_cancelled")),
                "custom": f"{period}, {user.username}",
            }

            # Create the instance.
            form = PayPalPaymentsForm(initial=paypal_dict)
            context = {"form": form}
            return render(request, "main/payment.html", context)
        user = request.user
        key_obj = user.profile.key

        current_date = int_from_date(str(datetime.datetime.now().date()))
        if key_obj.key:
            period = key_obj.period
            if key_obj.date:
                date = datetime.datetime.strptime(key_obj.date, '%Y-%m-%d')
                date = add_months(date, int(period))
                date = int_from_date(str(date))
        date = f"{str(date)[:4]}-{str(date)[4:6]}-{str(date)[6:]}"
        return render(request, 'main/profile.html', context={'user': user, 'key_obj': key_obj, 'end_of_license': date})


def register(request, period_selected):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            user = User.objects.all().last()
            # p = Profile.objects.create(user=user
            # p.save()
            key = Key.objects.create(profile=user.profile, period=form.cleaned_data['period'])
            key.save()
            return redirect("login")
    else:
        print(period_selected)
        form = UserRegisterForm(initial={'period': period_selected})

    return render(request, "main/register.html", context={"form": form})
