# Create your views here.
import json

from django.core import serializers
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from TakeOutSystem.forms import ComplainForm
from TakeOutSystem.models import Employee, Menu, order_menu, Complaint


def object_to_json(obj):
    return dict([(kk, obj.__dict__[kk]) for kk in obj.__dict__.keys() if kk != "_state"])


# R_MANAGER
@require_http_methods(['GET'])
def show_r_staff(request):
    response = {}
    try:
        employees = Employee.objects.filter(position='r_staff')
        response['list'] = json.loads(serializers.serialize('json', employees))
        response['msg'] = 'successfully'
        response['error_num'] = 0
    except Exception as e:
        response['msg'] = str(e)
        response['error_num'] = 1

    return JsonResponse(response)


@require_http_methods(['GET'])
def show_r_staff_dishes(request):
    response = {}
    try:
        r_staff_id = request.GET.get('employee_id')
        dish_names = Menu.objects.filter(r_staff_id=r_staff_id)
        response['list'] = json.loads(serializers.serialize('json', dish_names))
        response['msg'] = 'successfully'
        response['error_num'] = 0
    except Exception as e:
        response['msg'] = str(e)
        response['error_num'] = 1

    return JsonResponse(response)


@require_http_methods(['GET'])
def show_sales(request):
    response = {}
    try:
        sales = order_menu.objects.filter(dish_name=request.GET.get('dish_name'))
        response['list'] = json.loads(serializers.serialize('json', sales))
        response['msg'] = 'successfully'
        response['error_num'] = 0
    except Exception as e:
        response['msg'] = str(e)
        response['error_num'] = 1
    return JsonResponse(response)


@require_http_methods("GET")
def show_complaints(request):
    response = {}
    try:
        complaints = Complaint.objects.all()
        response['list'] = json.loads(serializers.serialize('json', complaints))
        response['msg'] = 'success'
        response['error_num'] = 0
    except Exception as e:
        response['msg'] = str(e)
        response['error_num'] = 1
    return JsonResponse(response)


@csrf_exempt
@require_http_methods("POST")
def change_one_complaint(request):
    response = {}
    try:
        complain_form = ComplainForm(request.POST)
        response['msg'] = 'check'
        response['error_num'] = 0
        if complain_form.is_valid():
            order_id = complain_form.cleaned_data['order_id']
            type = complain_form.cleaned_data['type']
            feed_back = complain_form.cleaned_data['feedback']
            complaint = Complaint.objects.get(order_id=order_id)
            complaint.feedback = feed_back
            complaint.save()
            response['msg'] = 'successfully'
            response['error_num'] = 1
        else:
            response['msg'] = 'form is not valid'
            response['error_num'] = 2
    except Exception as e:
        response['msg'] = str(e)
        response['error_num'] = 3
    return JsonResponse(response)