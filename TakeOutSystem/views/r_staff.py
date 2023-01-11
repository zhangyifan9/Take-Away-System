# Create your views here.
import json
from datetime import datetime

from django.core import serializers
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from TakeOutSystem.forms import MenuForm, OrderForm
from TakeOutSystem.models import Employee, Menu, Order, order_menu


def object_to_json(obj):
    return dict([(kk, obj.__dict__[kk]) for kk in obj.__dict__.keys() if kk != "_state"])


# R_STAFF


@csrf_exempt
@require_http_methods(['POST'])
def add_one_dish(request):
    response = {}
    try:
        menu_form = MenuForm(request.POST)
        if menu_form.is_valid():
            dish_name = menu_form.cleaned_data['dish_name']
            try:
                menu = Menu.objects.get(dish_name=dish_name)
                response['msg'] = 'dish_name existed'
                response['error_num'] = 0
            except:
                menu = Menu(
                    dish_name=dish_name,
                    r_staff_id=Employee.objects.get(employee_id=request.session.get('employee_id')),
                    price=menu_form.cleaned_data['price'],
                    # picture = menu_form.cleaned_data['picture'],
                    stock=menu_form.cleaned_data['stock'],
                    special_offer = menu_form.cleaned_data['special_offer']
                )
                menu.save()
                response['msg'] = 'successfully'
                response['error_num'] = 1
        else:
            response['msg'] = 'form is not valid'
            response['error_num'] = 2
    except Exception as e:
        response['msg'] = str(e)
        response['error_num'] = 3
    return JsonResponse(response)


@require_http_methods(['GET'])
def show_dish(request):
    response = {}
    if not request.session.get('is_login'):
        response['msg'] = 'you must login'
        response['error_num'] = 0
        return JsonResponse(response)
    try:
        if request.GET.get('dish_name') is None:
            dish = Menu.objects.all()
            orders_total = Order.objects.all()

            listall = json.loads(serializers.serialize("json", dish))
            total = len(listall)
            pagesize = int(request.GET.get('pagesize'))
            pagenum = int(request.GET.get('pagenum'))
            if pagesize > total:
                pagesize = total
            sort_ls = [listall[i:i + pagesize] for i in range(0, len(listall), pagesize)]
            response['total_dish'] = total
            response['total'] = len(orders_total) + 20001
            response['list'] = sort_ls[pagenum-1]
            response['msg'] = 'success'
            response['error_num'] = 0
        else:
            dish = Menu.objects.get(dish_name=request.GET.get('dish_name'))
            request.session['dish_name'] = dish.dish_name
            orders_total = Order.objects.all()
            response['total_dish'] = 1
            response['total'] = len(orders_total) + 20001
            response['list'] = object_to_json(dish)
            response['msg'] = 'show success'
            response['error_num'] = 0
    except Exception as e:

        if str(e)=="range() arg 3 must not be zero":
            response['error_num'] = 0
            response['msg'] = 'show success'
        else:
            response['error_num'] = 1
            response['msg'] = str(e)
    return JsonResponse(response)



@csrf_exempt
@require_http_methods(['POST'])
def change_one_dish(request):
    response = {}
    try:
        menu_form = MenuForm(request.POST)
        if menu_form.is_valid():
            dish_name = menu_form.cleaned_data['dish_name']
            try:
                menu = Menu.objects.get(dish_name=dish_name)
                menu.price = menu_form.cleaned_data['price']
                # menu.picture = menu_form.cleaned_data['picture']
                menu.stock = menu_form.cleaned_data['stock']
                menu.special_offer = menu_form.cleaned_data['special_offer']
                menu.save()
                response['msg'] = 'successfully'
                response['error_num'] = 0
            except:
                response['mas'] = 'dish_name not exsited'
                response['error_num'] = 1
        else:
            response['msg'] = 'form is not valid'
            response['error_num'] = 2

    except Exception as e:
        response['msg'] = str(e)
        response['error_num'] = 3
    return JsonResponse(response)


@csrf_exempt
@require_http_methods(['POST'])
def accept_dish_order(request):
    response = {}
    try:
        if request.session.get('is_login'):  # and request.session.get('position') == 'r_staff':
            order_form = OrderForm(request.POST)
            if order_form.is_valid():
                order_id = order_form.cleaned_data['order_id']
                order = Order.objects.get(order_id=order_id)
                if order.order_status == '完成支付':
                    order_m = order_menu.objects.get(order_id=order_id)
                    dish = Menu.objects.get(dish_name=order_m.dish_name.dish_name)
                    dish.stock -= 1
                    dish.save()

                    order.meal_complete_time = datetime.now()
                    order.order_status = '商家已接单'
                    order.save()

                    response['msg'] = 'accept_dish_order successfully'

                    response['error_num'] = 0
                else:
                    response['msg'] = '对方还未完成支付'
                    response['error_num'] = 0
            else:
                response['msg'] = 'form is not valid'
                response['error_num'] = 1
        else:
            response['msg'] = 'you are not r_staff or not login'
            response['error_num'] = 0
    except Exception as e:
        response['msg'] = str(e)
        response['error_num'] = 2
    return JsonResponse(response)


@csrf_exempt
@require_http_methods(['POST'])
def request_delivery(request):
    response = {}
    try:
        if request.session.get('is_login'):  # and request.session.get('position')=='r_staff':
            order_form = OrderForm(request.POST)
            if order_form.is_valid():

                order_id = order_form.cleaned_data['order_id']
                order = Order.objects.get(order_id=order_id)
                if order.order_status == '商家已接单':
                    order.order_status = '完成备餐'

                    if order.eat_in_store == '堂食':
                        order.order_status = '完成送达'

                    order.save()

                    response['msg'] = 'request_delivery successfully'
                    response['error_num'] = 0
                else:
                    response['msg'] = '对方未完成支付'
                    response['error_num'] = 0
            else:
                response['msg'] = 'form is not valid'
                response['error_num'] = 0
        else:
            response['msg'] = 'not login or not r_staff'
            response['error_num'] = 0
    except Exception as e:
        response['msg'] = str(e)
        response['error_num'] = 1
    return JsonResponse(response)