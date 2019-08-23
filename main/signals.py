from paypal.standard.models import ST_PP_COMPLETED
from paypal.standard.ipn.signals import valid_ipn_received, invalid_ipn_received

# def show_me_the_money(sender, **kwargs):
#     ipn_obj = sender
#
#     # ipn_obj = sender
#     if ipn_obj.payment_status == ST_PP_COMPLETED:
#         print("Received payment")
#         print("save")
#         print('Recieved payment')
#     else:
#         print("Failed")
#

# valid_ipn_received.connect(show_me_the_money)
#
# invalid_ipn_received.connect(show_me_the_money)
