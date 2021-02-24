from django.shortcuts import render, redirect, HttpResponse
import datetime
from django.db.models import Q
from uuid import uuid4
import base64

from django.contrib.auth.models import *
import calendar
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
from paypal.standard.forms import PayPalPaymentsForm
from django.urls import reverse
from .models import Key
import smtplib
import ssl
from users.forms import *
import telebot

ADMIN_ID = 489460463
TOKEN = '1442595220:AAEdSkO8wH-784vDjq95xu3XD06naeWXM00'
bot = telebot.TeleBot(TOKEN)


@csrf_exempt
def payment_done(request):
    return render(request, "main/payment_done.html")


@csrf_exempt
def payment_canceled(request):
    return render(request, 'main/payment_cancelled.html')


def show_me_the_money(sender, **kwargs):
    ipn_obj = sender
    print(ipn_obj.payment_status)
    if ipn_obj.payment_status == ST_PP_COMPLETED:
        print("Received payment")
        date = str(datetime.datetime.now().date())
        key = uuid4()

        period, username = ipn_obj.custom, ipn_obj.custom
        period = period[:period.find(',')]
        username = username[username.find(' ') + 1:]
        try:
            user = User.objects.filter(username=username)[0]
            user_profile = user.profile
            key_obj = user_profile.key
            key_obj.key = key
            key_obj.date = date
            key_obj.save()
            # send_mail('You have succesfully bought 4-Organizer', f'Now you can proceed to installation instruction (4-Organizer.com/install). Your key, keep it in secret: {key}', 'Mail.4_organizer@yahoo.com', [email])
        except IndexError:
            pass
    else:
        print("Failed")


valid_ipn_received.connect(show_me_the_money)
invalid_ipn_received.connect(show_me_the_money)


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


def main(request):
    keys = Key.objects.all()
    current_date = int_from_date(str(datetime.datetime.now().date()))

    for key in keys:
        if key.key:
            period = key.period
            if key.date:
                try:
                    date = datetime.datetime.strptime(key.date,
                                                      '%Y-%m-%d %H:%M:%S.%f')
                except:
                    date = datetime.datetime.strptime(key.date,
                                                      '%Y-%m-%d')
                                                                                           
                date = add_months(date, int(period))
                date = int_from_date(str(date))
                if period == '0' or period == 0:
                    pass
                elif current_date >= date:
                    key.delete()

    return render(request, 'main/main.html')


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

            bot.send_message(
                ADMIN_ID,
                f'Name: |{name}|\nEmail: |{email}|\nMessage: |{message}|'[:
                                                                          4000]
            )
            return HttpResponse("""
<body style="background-color: #282c34"> 

<div style="margin: 10%; border-radius: 15px; border: 5px #4989cc solid!important; padding: 10px">
<h1 style="color: #4989cc; text-align: center; margin-top: 30px; font-family: Segoe UI;">You message has been sended succesfully.</h1>
</div>

</body>
""")

    return render(request, r'main/contact_us.html', context={'form': form})


def pricing(request):
    return render(request, 'main/pricing.html')


def support(request):
    return render(request, 'main/support.html')


def terms(request):
    return render(request, 'main/terms.html')


def select_scan(request):
    return render(request, 'main/select_scan.html')


def install(request):
    return render(request, 'main/install.html')


def changelog(request):
    return render(request, 'main/changelog.html')

def decode_str(string, key):
    f = Fernet(key)
    return f.decrypt(string).decode()


def key(request, id, id2, license, username):
    to_return = f'{id} {id2} {license} {username}'
    id = id.encode()
    salt = id2.encode()
    kdf = PBKDF2HMAC(algorithm=hashes.SHA256(),
                     length=32,
                     salt=salt,
                     iterations=100000,
                     backend=default_backend())
    key = base64.urlsafe_b64encode(kdf.derive(id))

    license = decode_str(license.encode(), key).lower()
    username = decode_str(username.encode(), key).lower()
    user = User.objects.filter(username=username).last()
    profile = user.profile
    key = Key.objects.filter(key=license, profile_id=profile.id).last()

    if not key.key:
        to_return = 'error'
    return HttpResponse(to_return)


@csrf_exempt
def mail(request):
    if request.method == 'POST':
        email = request.POST.get('email_newsletter', '')
        sign_up_email = Email.objects.create(email=email)
        sign_up_email.save()
        return HttpResponse("""
<body style="background-color: #282c34"> 

<div style="margin: 10%; border-radius: 15px; border: 5px #4989cc solid!important; padding: 10px">
<h1 style="color: #4989cc; text-align: center; margin-top: 30px; font-family: Segoe UI;">Signed up succesfully.</h1>
</div>

</body>
""")
