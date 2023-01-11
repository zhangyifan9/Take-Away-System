# Create your views here.
import json
from datetime import datetime

from django.core import serializers
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from TakeOutSystem.forms import EmployeeForm, AccountForm, LocationForm
from TakeOutSystem.models import Employee, Balance_account, Location, turnover


def object_to_json(obj):
    return dict([(kk, obj.__dict__[kk]) for kk in obj.__dict__.keys() if kk != "_state"])



# ADMINISTER


@csrf_exempt
@require_http_methods(["POST"])
def add_one_employee(request):
    response = {}
    try:
        employee_form = EmployeeForm(request.POST)
        if employee_form.is_valid():
            employee_id = employee_form.cleaned_data['employee_id']
            try:
                Employee.objects.get(employee_id=employee_id)
                response['msg'] = 'employee_id exsited'
                response['error_num'] = 1
            except:

                employee = Employee(employee_id=employee_id,
                                    name=employee_form.cleaned_data['name'],
                                    password=employee_form.cleaned_data['password'],
                                    department=employee_form.cleaned_data['department'],
                                    position=employee_form.cleaned_data['position']
                                    )
                employee.save()
                response['msg'] = 'successfully'
                response['error_num'] = 0
        else:
            response['msg'] = 'form is not valid'
            response['error_num'] = 1
    except  Exception as e:
        response['msg'] = str(e)
        response['error_num'] = 2
    return JsonResponse(response)


@require_http_methods(["GET"])
def show_one_employee(request):
    response = {}
    try:
        employee = {}
        if request.GET.get('employee_id') is not None:
            print(( request.GET.get('employee_id')))
            employee = Employee.objects.get(employee_id=request.GET.get('employee_id'))
            response['list'] = object_to_json(employee)
            total = 1
            response['error_num'] = -1
        else:
            # 返回值增加了分页，把数据分成每页pagesize个数据
            employee = Employee.objects.all()
            listall =  json.loads(serializers.serialize("json", employee))
            total = int(len(listall))
            pagesize = int(request.GET.get('pagesize'))
            pagenum = int(request.GET.get('pagenum'))
            # print(pagesize, pagenum)
            if pagesize>total:
                pagesize = total
            sort_ls = [listall[i:i + pagesize] for i in range(0, len(listall), pagesize)]
            response['list'] = sort_ls[pagenum-1]
            response['error_num'] = 0
        response['msg'] = 'success'
        response['total'] = total
    except  Exception as e:
        response['msg'] = str(e)
        print(str(e))
        response['error_num'] = 1
    return JsonResponse(response)


@csrf_exempt
@require_http_methods(['POST'])
def change_one_employee(request):
    response = {}
    try:
        employee_form = EmployeeForm(request.POST)
        if employee_form.is_valid():
            employee_id = employee_form.cleaned_data['employee_id']
            try:
                employee = Employee.objects.get(employee_id=employee_id)
                employee.name = employee_form.cleaned_data['name']
                employee.password = employee_form.cleaned_data['password']
                employee.department = employee_form.cleaned_data['department']
                employee.position = employee_form.cleaned_data['position']
                employee.save()
                response['msg'] = 'successfully'
                response['error_num'] = 0
            except Exception as e:
                response['msg'] = 'employee does not exsited'
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
def add_one_account(request):
    response = {}
    try:
        account_form = AccountForm(request.POST)
        if account_form.is_valid():
            account_id = account_form.cleaned_data['account_id']
            try:
                Balance_account.objects.get(account_id=account_id)
                response['msg'] = 'account existed'
                response['error_num'] = 0
            except:
                account = Balance_account(
                    employee_id=Employee.objects.get(employee_id=account_form.cleaned_data['employee_id']),
                    account_id=account_id,
                    open_time=datetime.now(),
                    balance=account_form.cleaned_data['balance'],
                    report_loss=account_form.cleaned_data['report_loss']
                )
                account.save()
                response['msg'] = 'success'
                response['error_num'] = 1
        else:
            response['msg'] = 'form is not valid'
            response['error_num'] = 2
    except Exception as e:
        response['msg'] = str(e)
        response['error_num'] = 3
    return JsonResponse(response)


@require_http_methods(['GET'])
def show_account(request):
    response = {}
    try:
        account = Balance_account.objects.all()
        # response['list'] = json.loads(serializers.serialize("json", account))
        listall= json.loads(serializers.serialize("json", account))
        response['list'] = listall
        total = int(len(listall))

        pagesize = int(request.GET.get('pagesize'))
        pagenum = int(request.GET.get('pagenum'))
        print(pagesize, pagenum,total)
        if pagesize > total:
            pagesize = total
        sort_ls = [listall[i:i + pagesize] for i in range(0, len(listall), pagesize)]
        response['list'] = sort_ls[pagenum - 1]

        response['total'] = total
        response['msg'] = 'success'
        response['error_num'] = 0
    except Exception as e:
        if str(e)=="range() arg 3 must not be zero":
            response['error_num'] = 0
            response['msg'] = 'success'
        else:
            response['msg'] = str(e)
            response['error_num'] = 1
    return JsonResponse(response)


@csrf_exempt
@require_http_methods(['POST'])
def change_one_account(request):
    response = {}
    try:
        account_form = AccountForm(request.POST)
        if account_form.is_valid():
            account_id = account_form.cleaned_data['account_id']
            try:
                account = Balance_account.objects.get(account_id=account_id)
                account.balance += account_form.cleaned_data['balance']
                account.report_loss = account_form.cleaned_data['report_loss']
                account.save()
                t = turnover(
                    account_id=account,
                    business_type='充值',
                    time=datetime.now(),
                    amount=account_form.cleaned_data['balance']
                )
                t.save()
                response['msg'] = 'successfully'
                response['error_num'] = 0
            except Exception as e:
                response['msg'] = str(e)
                response['error_num'] = 0
        else:
            response['msg'] = 'form is not valid'
            response['error_num'] = 0

    except Exception as e:
        response['msg'] = str(e)
        response['error_num'] = 1
    return JsonResponse(response)


@csrf_exempt
@require_http_methods(['POST'])
def add_one_location(request):
    response = {}
    try:
        location_form = LocationForm(request.POST)
        if location_form.is_valid():
            loc_id = location_form.cleaned_data['loc_id']
            try:
                Location.objects.get(loc_id=loc_id)
                response['msg'] = 'loc_id existed'
                response['error_num'] = 0
            except:
                location = Location(
                    loc_id=int(loc_id),
                    building=location_form.cleaned_data['building'],
                    floor=location_form.cleaned_data['floor'],
                    room=location_form.cleaned_data['room'],
                    time=datetime.now()
                )
                location.save()
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
def show_location(request):
    response = {}
    try:
        location = Location.objects.all()
        response['list'] = json.loads((serializers.serialize("json", location)))
        listall = json.loads((serializers.serialize("json", location)))
        response['list'] = listall
        print(listall)
        response['msg'] = 'success'
        response['error_num'] = 0
    except Exception as e:
        if str(e)=="range() arg 3 must not be zero":
            response['error_num'] = 0
            response['msg'] = 'success'
        else:
            response['msg'] = str(e)
            response['error_num'] = 1
    return JsonResponse(response)


@csrf_exempt
@require_http_methods(['POST'])
def change_one_location(request):
    response = {}
    try:
        location_form = LocationForm(request.POST)
        if location_form.is_valid():
            try:
                location = Location.objects.get(loc_id=location_form.cleaned_data['loc_id'])
                location.building = location_form.cleaned_data['building']
                location.floor = location_form.cleaned_data['floor']
                location.room = location_form.cleaned_data['room']
                location.save()
                response['msg'] = 'successfully'
                response['error_num'] = 0
            except Exception as e:
                response['msg'] = str(e)
                response['error_num'] = 0
        else:
            response['msg'] = 'form is not valid'
            response['error_num'] = 0

    except Exception as e:
        response['msg'] = str(e)
        response['error_num'] = 1
    return JsonResponse(response)
