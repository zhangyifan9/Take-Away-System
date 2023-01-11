from django.conf.urls import url

from TakeOutSystem.views.administer import *
from TakeOutSystem.views.employee import *
from TakeOutSystem.views.r_delivery import *
from TakeOutSystem.views.r_manager import *
from TakeOutSystem.views.r_staff import *
from TakeOutSystem.views.user import *

urlpatterns = [

    # views
    url(r'user_login$', user_login),
    url(r'user_logout$', user_logout),
    url(r'user_register$', user_register),

    # administer
    url(r'add_one_employee$', add_one_employee, ),
    url(r'show_one_employee$', show_one_employee,),
    url(r'change_one_employee$', change_one_employee,),
    url(r'add_one_account$', add_one_account),
    url(r'show_account$', show_account),
    url(r'change_one_account$', change_one_account),
    url(r'add_one_location$', add_one_location),
    url(r'show_location$', show_location),
    url(r'change_one_location$', change_one_location),

    # r_staff
    url(r'add_one_dish$', add_one_dish),
    url(r'show_dish$', show_dish),
    url(r'change_one_dish$', change_one_dish),
    url(r'accept_dish_order$', accept_dish_order),
    url(r'request_delivery$', request_delivery),

    # Employee
    url(r'order_dish$', order_dish),
    url(r'pay$', pay),
    url(r'show_order$', show_order),
    url(r'show_turnovers$', show_turnovers),
    url(r'complain$', complain),

    # r_delivery
    url(r'accept_delivery_order$', accept_delivery_order),
    url(r'delivered$', delivered),

    # r_manager
    url(r'show_complaints$', show_complaints),
    url(r'change_one_complaint$', change_one_complaint),
    url(r'show_r_staff$', show_r_staff),
    url(r'show_sales$', show_sales),
    url(r'show_r_staff_dishes$', show_r_staff_dishes),



]