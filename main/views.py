from django.shortcuts import render, redirect, HttpResponse
import datetime
from django.db.models import Q
from uuid import uuid4
import base64



import datetime
import pickle
import requests
from django.contrib.auth.models import User
from main.models import *
from users.models import *



import datetime
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
from django.shortcuts import render
from paypal.standard.forms import PayPalPaymentsForm
from django.urls import reverse
from paypal.standard.models import ST_PP_COMPLETED
from .models import Key
import smtplib
import ssl
from users.forms import *

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
        username = username[username.find(' ')+1:]
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

            send_mail(f'From {name}, email: {email}', f'{message}', 'Mail.4_organizer@yahoo.com', ['dariyshereta@aol.com', 'darik.pc@gmail.com'])
            return HttpResponse('You message has been sended succesfully')

    return render(request, r'main/contact_us.html', context={'form': form})

def pricing(request):
    return render(request, 'main/pricing.html')

def support(request):
    return render(request, 'main/support.html')

def terms(request):
    return render(request, 'main/terms.html')

def select_scan(request):
    data = requests.get('https://4-organizer-files.000webhostapp.com/Users.p').content
    users = pickle.loads(data)
    for user in users:
        if not User.objects.filter(username=user['username']):
            u = User.objects.create_user(username=user['username'], password=user['password'], first_name=user['first_name'], last_name=user['last_name'])
            profile = Profile.objects.create(user=u)
            profile.save()
            u = User.objects.get(username=user['username'])
            key = Key.objects.create(profile=u.profile, key=uuid.uuid4(), date=str(user['last_login'][0].date()), period=user['period'])
            key.save()
    return render(request, 'main/select_scan.html')

def install(request):
    return render(request, 'main/install.html')

def decode_str(string, key):
    f = Fernet(key)
    return f.decrypt(string).decode()

def key(request, id, id2, license, username):
    to_return = f'{id} {id2} {license} {username}'
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
    username = decode_str(username.encode(), key).lower()
    user = User.objects.filter(username=username).last()
    profile = user.profile
    key = Key.objects.filter(key=license, profile_id=profile.id).last()
    print('User: ', user)
    print('Profile', profile)
    print('Key: ', key)
    if not key.key:
        to_return = 'error'
    return HttpResponse(to_return)

@csrf_exempt
def mail(request):
    if request.method == 'POST':
        email = request.POST.get('email_newsletter', '')
        sign_up_email = Email.objects.create(email=email)
        sign_up_email.save()
        return HttpResponse('Signed up succesfully')
