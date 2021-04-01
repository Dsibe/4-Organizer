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
from sellapp.models import License


def int_from_date(date):
    str_date = str(date)
    str_date = str_date.replace('-', '')

    return int(str_date)


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
        key_obj = user.license_set.first()

        if not key_obj.key:
            period = key_obj.additional_info
            host = request.get_host()

            if key_obj.is_custom:
                months_amount = int(period)

                print('months_amount', months_amount)
                machines_amount = key_obj.max_machines_limit

                print('machines_amount', machines_amount)

                if months_amount > 3:
                    discount_percent = 0.15
                elif months_amount > 6:
                    discount_percent = 0.30
                elif months_amount > 12:
                    discount_percent = 0.60
                else:
                    discount_percent = 0

                print('discount_percent', discount_percent)

                months_total_sum = (months_amount * 3)
                print('months_total_sum', months_total_sum)
                months_total_sum = months_total_sum * (1 - discount_percent)
                print('months_total_sum', months_total_sum)

                machines_amount = machines_amount * (1 - discount_percent)
                print('machines_amount', machines_amount)
                machines_total_sum = months_total_sum * machines_amount
                print('machines_total_sum', machines_total_sum)

                price = round(machines_total_sum, 2)
                print('price', price)
                price = str(price)
            else:
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
                'abt.company-facilitator@aol.com',
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
            context = {
                "form": form,
                'price': price,
                'period': period_paypal,
                'max_machines_limit': key_obj.max_machines_limit,
            }
            return render(request, "main/payment.html", context)
        user = request.user
        key_obj = user.license_set.first()

        current_date = int_from_date(str(datetime.datetime.now().date()))
        date = 'UNDEFINED'

        if key_obj.key:
            period = key_obj.additional_info
            if key_obj.creation_date:
                date = key_obj.creation_date
                date = add_months(date, int(period))

                if int(period) == 0:
                    date = 'Infinite'

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
            user = User.objects.get(username=form.cleaned_data['username'])
            additional_info = form.cleaned_data['period']

            license = License(user=user,
                              additional_info=additional_info,
                              creation_date=datetime.date.today())
            license.save()
            return redirect("login")

    form = UserRegisterForm(initial={'period': period_selected})
    return render(request, "main/register.html", context={"form": form})


def register_unique_profile(request, months_amount, machines_amount):
    if request.method == "POST":
        form = UniquePlanUserRegisterForm(request.POST)
        print(form.errors)

        if form.is_valid():
            form.save()
            user = User.objects.get(username=form.cleaned_data['username'])

            months_amount = form.cleaned_data['months_amount']
            machines_amount = form.cleaned_data['machines_amount']

            license = License(user=user,
                              is_custom=True,
                              additional_info=str(months_amount),
                              max_machines_limit=machines_amount,
                              creation_date=datetime.date.today())
            license.save()
            return redirect("login")

    form = UniquePlanUserRegisterForm(initial={
        'months_amount': months_amount,
        'machines_amount': machines_amount,
    })
    return render(request, "main/register.html", context={"form": form})


def update_profile(request):
    if request.method == "POST":
        form = UserUpdateForm(request.POST)

        if form.is_valid():
            user = request.user
            user.username = form.cleaned_data['new_username']
            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
            user.save()

            return redirect("profile")
    else:
        user = request.user
        form = UserUpdateForm(instance=user,
                              initial={'new_username': user.username})

    return render(request, "main/update_profile.html", context={"form": form})
