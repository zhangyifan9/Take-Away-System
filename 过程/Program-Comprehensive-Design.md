---
Author: Alex Ma
title: Program Comprehensive Design
---

[详细全面的postman接口测试实战教程](https://zhuanlan.zhihu.com/p/141948716)

[参考 Django](https://cloud.tencent.com/developer/article/1576599))

# 



# 1 创建 models

* 更换 Mysql ，创建数据库表TakeOutSystem

  * ```Mysql
    CREATE DATABASE TakeOutSystem;
    ```

  * ```python
    pip install mysqlclient
    ```

  * settings.py:

    ```python
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': 'django_vue_db',
            'USER': 'root',
            'PASSWORD': 'xxxxxxx',
            'HOST': '127.0.0.1',
        }
    }
    ```

* 同步数据库：

  * ```python
    py manage.py migrate
    ```

## 1.1 创建model Employee

```python
```



# 2 编写视图

```python
from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from django.core import serializers
from django.http import JsonResponse
import json
```

## 2.0 路由

* 编写好的视图都需要添加入 .urls.py 文件中

```python
from django.conf.urls import url, include
from .views import *

urlpatterns = [
    url(r'add_book$', add_book, ),
    url(r'show_books$', show_books, ),
]
```

* urls添加到项目django_vue下的urls中

```python
from django.contrib import admin
from django.urls import path
from django.conf.urls import url, include
from django.contrib import admin
from django.views.generic import TemplateView
import api_test.urls

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^api/', include(api_test.urls)),
]
```



# 2.1 Employee views

```python
@require_http_methods(["GET"])
def add_employee(request):
    response = {}
    try:
        employee = Employee(employee_id=request.GET.get('employee_id'))
        employee.save()
        response['msg'] = 'success'
        response['error_num'] = 0
    except  Exception as e:
        response['msg'] = str(e)
        response['error_num'] = 1
    return JsonResponse(response)


@require_http_methods(["GET"])
def show_employee(request):
    response = {}
    try:
        employees = Employee.objects.filter()
        response['list'] = json.loads(serializers.serialize("json", employees))
        response['msg'] = 'success'
        response['error_num'] = 0
    except  Exception as e:
        response['msg'] = str(e)
        response['error_num'] = 1
    return JsonResponse(response)
```

