# Create your views here.
from datetime import datetime

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from TakeOutSystem.forms import OrderForm
from TakeOutSystem.models import Employee, Order


def object_to_json(obj):
    return dict([(kk, obj.__dict__[kk]) for kk in obj.__dict__.keys() if kk != "_state"])


# R_DELIVERY


@csrf_exempt
@require_http_methods(['POST'])
def accept_delivery_order(request):
    response = {}
    try:
        if request.session.get('is_login'):  # and request.session.get('position') == 'r_delivery':
            order_form = OrderForm(request.POST)
            if order_form.is_valid():
                order_id = order_form.cleaned_data['order_id']
                order = Order.objects.get(order_id=order_id)
                if order.order_status == '完成备餐':
                    order.r_delivery_id = Employee.objects.get(employee_id=request.session.get('employee_id'))
                    order.accept_order_time = datetime.now()
                    order.order_status = '骑手已接单'
                    order.save()

                    response['msg'] = 'accept_delivery_order successfully'
                    response['error_num'] = 0
                else:
                    response['msg'] = '商家未完成配餐'
                    response['error_num'] = 1
            else:
                response['msg'] = ' form is not valid'
                response['error_num'] = 2
        else:
            response['msg'] = 'not login or not r_delivery'
            response['error_num'] = 3
    except Exception as e:
        response['msg'] = str(e)
        response['error_num'] = 4
    return JsonResponse(response)


@csrf_exempt
@require_http_methods(['POST'])
def delivered(request):
    response = {}
    try:
        if request.session.get('is_login'):  # and request.session.get('position') == 'r_delivery':
            order_form = OrderForm(request.POST)
            if order_form.is_valid():

                order_id = order_form.cleaned_data['order_id']
                order = Order.objects.get(order_id=order_id)
                if order.order_status == '骑手已接单':
                    order.delivery_time = datetime.now()
                    order.order_status = '完成送达'
                    order.save()

                    response['msg'] = 'delivered successfully'
                    response['error_num'] = 0
                else:
                    response['msg'] = 'r_delivery 未完成接单'
                    response['error_num'] = 1
            else:
                response['msg'] = 'form is not valid'
                response['error_num'] = 2
        else:
            response['msg'] = 'not login or not r_delivery'
            response['error_num'] = 3
    except Exception as e:
        response['msg'] = str(e)
        response['error_num'] = 4
    return JsonResponse(response)