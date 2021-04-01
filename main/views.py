from django.shortcuts import render, redirect, HttpResponse
import datetime
from uuid import uuid4
import base64

from django.contrib.auth.models import *
from django.core.mail import send_mail
from random import randint
from .models import *
from .forms import *
from django.views.decorators.csrf import csrf_exempt
from paypal.standard.models import ST_PP_COMPLETED
from paypal.standard.ipn.signals import valid_ipn_received, invalid_ipn_received
from paypal.standard.forms import PayPalPaymentsForm
from django.urls import reverse
from sellapp.models import License
import smtplib
import ssl
from users.forms import *
import telebot
import os


def debug_env_var(name):
    with open(rf'D:\libraries\Desktop\Dj\env\Scripts\app\organizer\{name}.txt'
              ) as file:
        return file.read()


ADMIN_ID = int(os.environ.get('admin_id', debug_env_var('admin_id')))
TOKEN = os.environ.get('tg_token', debug_env_var('tg_token'))
bot = telebot.TeleBot(TOKEN)


@csrf_exempt
def payment_done(request):
    return render(request, "main/payment_done.html")


def custom_plan(request):
    return render(request, "main/custom_plan.html")


@csrf_exempt
def payment_canceled(request):
    return render(request, 'main/payment_cancelled.html')


def show_me_the_money(sender, **kwargs):
    ipn_obj = sender

    print(ipn_obj.payment_status)
    # for i in dir(ipn_obj):
    #     try:
    #         exec(f"""print('{i}', ipn_obj.{i})""")
    #     except:
    #         pass

    if ipn_obj.payment_status == ST_PP_COMPLETED and ipn_obj.business == 'abt.company@aol.com':
        print("Received payment")
        date = str(datetime.datetime.now().date())

        period, username = ipn_obj.custom, ipn_obj.custom
        period = period[:period.find(',')]
        username = username[username.find(' ') + 1:]
        try:
            user = User.objects.filter(username=username)[0]
            key_obj = user.license_set.first()
            key_obj.create_key()
            key_obj.save()

            client_data = str(ipn_obj.posted_data_dict)
            bot.send_message(ADMIN_ID, client_data)
            # send_mail('You have succesfully bought 4-Organizer', f'Now you can proceed to installation instruction (4-Organizer.com/install). Your key, keep it in secret: {key}', 'Mail.4_organizer@yahoo.com', [email])
        except IndexError:
            pass
    else:
        print("Failed")


valid_ipn_received.connect(show_me_the_money)
invalid_ipn_received.connect(show_me_the_money)


def main(request):
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
