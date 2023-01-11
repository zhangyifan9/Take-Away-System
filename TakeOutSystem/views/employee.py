# Create your views here.
import json
from datetime import datetime,date

from django.core import serializers
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from TakeOutSystem.forms import ComplainForm, OrderForm
from TakeOutSystem.models import Employee, Balance_account, Location, Menu, Order, turnover, order_menu, Complaint
from django.db.models import Q

def object_to_json(obj):
    return dict([(kk, obj.__dict__[kk]) for kk in obj.__dict__.keys() if kk != "_state"])


# EMPLOYEE


@csrf_exempt
@require_http_methods(['POST'])
def order_dish(request):
    response = {}
    if not request.session.get('is_login', None):
        response['msg'] = 'you must login'
        response['error_num'] = -1
        return JsonResponse(response)
    try:
        order_form = OrderForm(request.POST)
        if order_form.is_valid():
            order_id = order_form.cleaned_data['order_id']
            try:
                Order.objects.get(order_id=order_id)
                response['msg'] = 'order_id existed'
                response['error_num'] = 0
            except:
                menu = Menu.objects.get(dish_name=order_form.cleaned_data['dish_name'])
                # amount = menu.price
                today = date.today()
                specify__delivery_time = str(today)+str(order_form.cleaned_data['specify_delivery_time'])[10:]
                order = Order(
                    order_id=order_id,
                    order_status='预定状态',
                    build_time=datetime.now(),
                    remark=order_form.cleaned_data['remark'],
                    eat_in_store=order_form.cleaned_data['eat_in_store'],
                    specify_delivery_time=specify__delivery_time,
                    location=Location.objects.get(loc_id=order_form.cleaned_data['location']),
                    payment_method=order_form.cleaned_data['payment_method'],
                    payment_amount=order_form.cleaned_data['payment_amount'],
                    payment_account_id=Balance_account.objects.get(
                    account_id=order_form.cleaned_data['payment_account_id']),
                    cus_id=Employee.objects.get(employee_id=request.session.get('employee_id')),
                    r_staff_id=menu.r_staff_id,
                    dish_name = order_form.cleaned_data['dish_name'],
                )
                order.save()
                request.session['order_id'] = order_id

                order_m = order_menu(
                    order_id=order,
                    dish_name=Menu.objects.get(dish_name=menu.dish_name),
                    amount=order_form.cleaned_data['payment_amount']
                )
                order_m.save()

                response['msg'] = 'order_dish successfully'
                response['error_num'] = 1
        else:
            response['msg'] = 'form is not valid'
            response['error_num'] = 2

    except Exception as e:
        response['msg'] = str(e)
        response['error_num'] = 3
    return JsonResponse(response)


@require_http_methods("GET")
def show_order(request):
    response = {}
    try:
        if request.session.get('position') == 'employee':
            orders = Order.objects.filter(cus_id=request.session.get('employee_id'))
        elif request.session.get('position') == 'r_staff':
            orders = Order.objects.filter(r_staff_id=request.session.get('employee_id'))
        elif request.session.get('position') == 'r_delivery':
            orders = Order.objects.filter(Q(Q(order_status='完成备餐') | Q(order_status='骑手已接单')))
        elif request.session.get('position') == 'admin' or request.session.get('position') == 'r_manager':
            orders = Order.objects.all()
        else:
            orders = Order.objects.all()

        listall = json.loads(serializers.serialize("json", orders))
        total = int(len(listall))
        pagesize = int(request.GET.get('pagesize'))
        pagenum = int(request.GET.get('pagenum'))
        if pagesize > total:
            pagesize = total
        sort_ls = [listall[i:i + pagesize] for i in range(0, len(listall), pagesize)]
        response['list'] = sort_ls[pagenum - 1]
        response['msg'] = 'successfully'
        response['total'] = total
        response['error_num'] = 0

    except Exception as e:
        # print(str(e) == "range() arg 3 must not be zero")
        if str(e) == "range() arg 3 must not be zero":
            response['error_num'] = 0
            response['msg'] = 'successfully'
        else:
            response['msg'] = str(e)
            response['error_num'] = 1
    return JsonResponse(response)


@csrf_exempt
@require_http_methods(['POST'])
def pay(request):
    response = {}
    if not request.session.get('is_login'):
        response['msg'] = 'you must login'
        response['error_num'] = 0
        return JsonResponse(response)
    try:
        order_form = OrderForm(request.POST)
        if order_form.is_valid():
            order_id = order_form.cleaned_data['order_id']
            # print(order_id)
            order = Order.objects.get(order_id=order_id)

            if order_form.cleaned_data['payment_method'] == '余额支付':
                # 支付方式为余额
                Balance = Balance_account.objects.get(account_id=order.payment_account_id_id)
                Balance.balance -= order_menu.objects.get(order_id=order_id).amount
                Balance.save()
                t = turnover(
                    account_id=Balance_account.objects.get(account_id=order.payment_account_id_id),
                    business_type='支付',
                    amount=order_menu.objects.get(order_id=order_id).amount
                )
                t.save()
            order.payment_method = order_form.cleaned_data['payment_method']
            order.payment_time = datetime.now()
            order.payment_id = t
            order.order_status = '完成支付'
            order.save()
            response['msg'] = 'pay successfully'
            response['error_num'] = 1
        else:
            response['msg'] = 'form is not valid'
            response['error_num'] = 2

    except Exception as e:
        response['msg'] = str(e)
        response['error_num'] = 3
    return JsonResponse(response)


@require_http_methods("GET")
def show_turnovers(request):
    response = {}
    try:
        account_id = Balance_account.objects.get(employee_id=request.session.get('employee_id')).account_id
        turns = turnover.objects.filter(account_id=account_id)

        listall = json.loads(serializers.serialize("json", turns))
        total = len(listall)
        pagesize = int(request.GET.get('pagesize'))
        pagenum = int(request.GET.get('pagenum'))
        if pagesize > total:
            pagesize = total
        sort_ls = [listall[i:i + pagesize] for i in range(0, len(listall), pagesize)]
        response['total'] = total
        response['list'] = sort_ls[pagenum - 1]
        response['error_num'] = 1
        response['msg'] = 'successfully'
    except Exception as e:
        if str(e) == "range() arg 3 must not be zero":
            response['error_num'] = 1
            response['msg'] = 'successfully'
        else:
            response['msg'] = str(e)
            response['error_num'] = 2
    return JsonResponse(response)


@csrf_exempt
@require_http_methods("POST")
def complain(request):
    response = {}
    try:
        if request.session.get('is_login', None):
            response['msg'] = 'check content'
            response['error_num'] = 0
            if request.method == 'POST':
                complain_form = ComplainForm(request.POST)
                response['msg'] = 'check'
                response['error_num'] = 1

                if complain_form.is_valid():
                    order_id = complain_form.cleaned_data['order_id']
                    time = datetime.now()
                    type = complain_form.cleaned_data['type']
                    content = complain_form.cleaned_data['content']
                    feedback = complain_form.cleaned_data['feedback']
                    complaint = Complaint(
                        order_id=Order.objects.get(order_id=order_id),
                        time=time,
                        type=type,
                        content=content,
                        feedback=feedback
                    )
                    complaint.save()
                    response['msg'] = 'complain successfully!'
                    response['error_num'] = 2

                else:
                    response['msg'] = 'form is not valid'
                    response['error_num'] = 3
            else:
                response['msg'] = 'GET'
                response['error_num'] = 4

            return JsonResponse(response)
        else:
            response['msg'] = 'you must login!'
            response['error_num'] = 5
    except Exception as e:
        response['msg'] = str(e)
        response['error_num'] = 6
    return JsonResponse(response)