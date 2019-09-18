from django.shortcuts import render, redirect, HttpResponse
import datetime
from django.db.models import Q
from uuid import uuid4
import base64
from django.core.mail import send_mail
from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from random import randint
from .models import *
from .forms import *
from django.views.decorators.csrf import csrf_exempt
from paypal.standard.models import ST_PP_COMPLETED
from paypal.standard.ipn.signals import valid_ipn_received, invalid_ipn_received
from django.shortcuts import render
from paypal.standard.forms import PayPalPaymentsForm
from django.urls import reverse
from paypal.standard.models import ST_PP_COMPLETED
from .models import Key
import smtplib
import ssl

def buy(request):
    if request.method == 'GET':
        form = PayForm
        return render(request, "main/payment.html", context={'payform': form})
    else:
        form = PayForm(request.POST)
        if form.is_valid():
            data = form.data
            email = data['email']
            key = Key(email=email)
            key.save()
            host = request.get_host()

            period = data['period']

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

            # print(period, price)

            paypal_dict = {
                "business": 'abt.company-facilitator@aol.com',
                "amount": price,
                "item_name": f"4-Organizer {period}",
                "currency_code": "USD",
                "invoice": f"{randint(1, 9999999)}",
                "notify_url": "http://{}{}".format(host, reverse("paypal-ipn")),
                "return_url": "http://{}{}".format(host, reverse("payment_done")),
                "cancel_return": "http://{}{}".format(host, reverse("payment_cancelled")),
                "custom": f"{period}, {email}",  # Custom command to correlate to some function later (optional)
            }

            # Create the instance.
            form = PayPalPaymentsForm(initial=paypal_dict)
            context = {"form": form}
            return render(request, "main/payment.html", context)




@csrf_exempt
def payment_done(request):
    return render(request, "main/payment_done.html")



@csrf_exempt
def payment_canceled(request):
    return HttpResponse("Payment Cancelled")


def show_me_the_money(sender, **kwargs):
    ipn_obj = sender
    print(ipn_obj.payment_status)
    print(dir(ipn_obj))
    if ipn_obj.payment_status == ST_PP_COMPLETED:
        print("Received payment")
        date = str(datetime.datetime.now().date())
        key = uuid4()

        period, email = ipn_obj.custom, ipn_obj.custom
        period = period[:period.find(',')]
        email = email[email.find(' ')+1:]
        key_obj = Key.objects.get(email=email)
        key_obj.key = key
        key_obj.date = date
        key_obj.period = period
        key_obj.save()

        send_mail('You have succesfully bought 4-Organizer', f'Now you can proceed to installation instruction (4-Organizer.com/install). Your key, keep it in secret: {key}', 'Darik.pc@gmail.com', [email])

        if key_obj.period != '0' or key_obj.period != 0:
            chance = randint(1, 100)
            if chance == 1:
                prize = 'Extra 1 Month'
                send_mail('You have won extra month for you license!', f'We have added 1 month you your current license. Now your license period is: {int(key_obj.period) + 1} months', 'Darik.pc@gmail.com', [email])
                key_obj.period = str(int(key_obj.period) + 1)
                key_obj.save()
            else:
                prize = 'nothing, bad luck!'
            return render(request, 'main/lottery.html', context={'prize': prize})
        return render(request, 'main/payment_done.html', context={'key_obj': key_obj})

    else:
        print("Failed")


valid_ipn_received.connect(show_me_the_money)

invalid_ipn_received.connect(show_me_the_money)

def int_from_date(date):
    current_date_edit = ''
    for i in date:
        if i != '-':
            current_date_edit += i
    date = current_date_edit
    return int(date)

import datetime
import calendar

def add_months(sourcedate, months):
    month = sourcedate.month - 1 + months
    year = sourcedate.year + month // 12
    month = month % 12 + 1
    day = min(sourcedate.day, calendar.monthrange(year,month)[1])
    return datetime.date(year, month, day)


def main(request):
    keys = Key.objects.all()
    current_date = int_from_date(str(datetime.datetime.now().date()))

    for key in keys:
        if key.key:
            period = key.period
            if key.date:
                date = datetime.datetime.strptime(key.date, '%Y-%m-%d')
                date = add_months(date, int(period))
                date = int_from_date(str(date))
                if period == '0' or period == 0:
                    pass
                elif current_date >= date:
                    send_mail(subject='Your 4-Organizer license', message=f'Hello, {key.email}. Your 4-Organizer license has expired. Please renew it at 4-Organizer.com/main', from_email='Mail.4_organizer@yahoo.com', recipient_list=[key.email], fail_silently=False)
                    key.delete()

    return render(request, 'main/description.html')

def start(request):
    return render(request, 'main/start.html')


def contact_us(request):
    if request.method == 'GET':
        form = ContactUsForm()
    else:
        form = ContactUsForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']

            send_mail(f'From {name}, email: {email}', f'{message}', 'Mail.4_organizer@yahoo.com', ['dariyshereta@aol.com'])
            return HttpResponse('You message has been sended succesfully')

    return render(request, r'main/contact_us.html', context={'form': form})

def description(request):
    return render(request, 'main/main.html')

def support(request):
    return render(request, 'main/support.html')

def lottery(request):
    return render(request, 'main/lottery.html')

def lottery_prize(request, prize):
    return render(request, 'main/lottery_prize.html', context={'prize': prize})

def terms(request):
    return render(request, 'main/terms.html')

def select_scan(request):
    return render(request, 'main/select_scan.html')

def install(request):
    return render(request, 'main/install.html')

def decode_str(string, key):
    f = Fernet(key)
    return f.decrypt(string).decode()

def key(request, id, id2, license, email):
    to_return = f'{id} {id2} {license} {email}'
    id = id.encode()
    salt = id2.encode()
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend()
    )
    key = base64.urlsafe_b64encode(kdf.derive(id))
    license = decode_str(license.encode(), key).lower()
    email = decode_str(email.encode(), key).lower()
    license_key = Key.objects.all().filter(Q(key=license) & Q(email=email))
    if len(license_key) >= 1:
        license_key = license_key[0]
    else:
        to_return = 'error'
    return HttpResponse(to_return)
