from django.urls import path, include
from django.contrib import admin
from django.urls import reverse
from main.views import *
from django.contrib.auth import views as auth_views
from users.models import *
from users.views import *
import sellapp.views as sell_views
import blog.views as blog_views

urlpatterns = [
    path('blog/', include('blog.urls')),
    path('register-unique-profile/<int:months_amount>/<int:machines_amount>/',
         register_unique_profile),
    path('custom-plan/', custom_plan, name='custom-plan'),
    path('update-profile/', update_profile, name='update_profile'),
    path('unban-machine/<int:machine_id>/', sell_views.unban_machine),
    path('ban-machine/<int:machine_id>/', sell_views.ban_machine),
    path('view-machines/', sell_views.view_machines, name='view_machines'),
    path('decrypt-code-with-license/<path:args>',
         sell_views.decrypt_code_with_license,
         name='decrypt-code-with-license'),
    path('license-check/<path:args>',
         sell_views.license_check,
         name='license-check'),
    path(r'', start, name="start"),
    path('changelog/', changelog, name="changelog"),
    path('paypal/', include('paypal.standard.ipn.urls')),
    path('register/<int:period_selected>/', register, name='register'),
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
