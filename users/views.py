import calendar
import datetime
from decimal import Decimal
from random import randint

from django.conf import settings
from django.contrib.auth import authenticate, login
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, redirect, render
from django.template import Context, Template
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from main.models import *
from paypal.standard.forms import PayPalPaymentsForm
from paypal.standard.ipn.signals import (invalid_ipn_received,
                                         valid_ipn_received)
from paypal.standard.models import ST_PP_COMPLETED

from .forms import *
from .models import *


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
    day = min(sourcedate.day, calendar.monthrange(year, month)[1])
    return datetime.date(year, month, day)


@login_required
def profile(request):
    if request.method == "GET":
        user = request.user
        user_profile = Profile.objects.get(user=user)
        key_obj = user_profile.key

        if key_obj.key == None:
            period = key_obj.period
            host = request.get_host()

            price = {
                '1': '4.99',
                '3': '12.99',
                '6': '19.99',
                '12': '24.99',
                '0': '499.99',
            }[period]

            if period == '0':
                period_paypal = 'forever'
            else:
                period_paypal = period + ' months'
            paypal_dict = {
                "business":
                'abt.company@aol.com',
                "amount":
                price,
                "item_name":
                f"4-Organizer {period_paypal}",
                "currency_code":
                "USD",
                "invoice":
                f"{randint(1, 9999999)}",
                "notify_url":
                "http://{}{}".format(host, reverse("paypal-ipn")),
                "return_url":
                "http://{}{}".format(host, reverse("payment_done")),
                "cancel_return":
                "http://{}{}".format(host, reverse("payment_cancelled")),
                "custom":
                f"{period}, {user.username}",
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
                date = datetime.datetime.strptime(key_obj.date,
                                                  '%Y-%m-%d %H:%M:%S.%f')
                date = add_months(date, int(period))
                date = int_from_date(str(date))
        date = f"{str(date)[:4]}-{str(date)[4:6]}-{str(date)[6:]}"
        return render(request,
                      'main/profile.html',
                      context={
                          'user': user,
                          'key_obj': key_obj,
                          'end_of_license': date
                      })


def register(request, period_selected):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            user = User.objects.all().last()
            key = Key.objects.create(profile=user.profile,
                                     period=form.cleaned_data['period'])
            key.save()
            return redirect("login")
    else:
        print(period_selected)
        form = UserRegisterForm(initial={'period': period_selected})

    return render(request, "main/register.html", context={"form": form})
