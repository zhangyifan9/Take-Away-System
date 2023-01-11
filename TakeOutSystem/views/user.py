# Create your views here.
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from TakeOutSystem.forms import UserForm, RegisterForm
from TakeOutSystem.models import Employee


def object_to_json(obj):
    return dict([(kk, obj.__dict__[kk]) for kk in obj.__dict__.keys() if kk != "_state"])


# USER
def login(request):
    return render(request, 'index.html')

@csrf_exempt
@require_http_methods("POST")
def user_login(request):
    response = {}
    if request.session.get('is_login', None):
        response['msg'] = 'this employee has logined'
        response['error_num'] = 0
        response['position'] = request.session.get('position')
        return JsonResponse(response)

    if request.method == 'POST':
        login_form = UserForm(request.POST)
        response['msg'] = 'please check '

        if login_form.is_valid():
            employee_id = login_form.cleaned_data['employee_id']
            password = login_form.cleaned_data['password']
            try:
                user = Employee.objects.get(employee_id=employee_id)
                if user.password == password:
                    request.session['is_login'] = True
                    request.session['employee_id'] = user.employee_id
                    request.session['name'] = user.name
                    request.session['position'] = user.position
                    response['msg'] = 'login successfully'
                    response['error_num'] = 0
                    response['position'] = user.position
                    return JsonResponse(response)
                else:
                    response['msg'] = 'login failed: wrong password'
                    response['error_num'] = 2
            except Exception as e:
                response['msg'] = str(e)
                response['error_num'] = 3

        return JsonResponse(response)

    return JsonResponse(response)


@csrf_exempt
@require_http_methods("POST")
def user_logout(request):
    response = {}
    try:
        if not request.session.get('is_login'):
            response['msg'] = 'have not login'
            response['error_num'] = 0
            return JsonResponse(response)
        request.session.flush()
        response['msg'] = 'logout successfully'
        response['error_num'] = 1
    except Exception as e:
        response['msg'] = str(e)
        response['error_num'] = 2
    return JsonResponse(response)


@csrf_exempt
@require_http_methods("POST")
def user_register(request):
    response = {}

    if request.method == "POST":
        register_form = RegisterForm(request.POST)
        response['msg'] = 'please check content!'
        response['error_num'] = 1

        if register_form.is_valid():
            employee_id = register_form.cleaned_data['employee_id']
            password1 = register_form.cleaned_data['password1']
            password2 = register_form.cleaned_data['password2']
            name = register_form.cleaned_data['name']
            department = register_form.cleaned_data['department']
            position = register_form.cleaned_data['position']

            if password1 != password2:
                response['msg'] = 'password is not consistent！'
                return JsonResponse(response)
            else:
                same_employee = {}
                try:
                    same_employee = Employee.objects.get(employee_id=employee_id)
                    response['msg'] = 'this employee_id has existed！'
                    response['error_num'] = 2
                    return JsonResponse(response)

                except Exception as e:

                    new_employee = Employee(
                        employee_id=employee_id,
                        name=name,
                        password=password1,
                        department=department,
                        position=position
                    )
                    response['msg'] = 'register successfully!'
                    response['error_num'] = 3
                    new_employee.save()
                return JsonResponse(response)
        return JsonResponse(response)
    return JsonResponse(response)
