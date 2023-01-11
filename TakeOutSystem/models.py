from django.db import models


# Create your models here.


class Employee(models.Model):
    POSITION_CHOICES = (
        (u'A', u'admin'),
        (u'E', u'employee'),
        (u'S', u'r_staff'),
        (u'M', u'r_manager'),
        (u'D', u'r_delivery')
    )
    employee_id = models.IntegerField(primary_key=True, null=False, unique=True)
    name = models.CharField(max_length=255, null=False)
    password = models.CharField(max_length=255, default='123456')
    department = models.CharField(max_length=255)
    position = models.CharField(max_length=255, choices=POSITION_CHOICES, null=False, default='employee')


class employee_phone(models.Model):
    employee_id = models.ForeignKey('Employee', on_delete=models.CASCADE, null=False)
    phone_number = models.CharField(max_length=15, primary_key=True, null=False)


class Balance_account(models.Model):
    employee_id = models.ForeignKey('Employee', on_delete=models.CASCADE)
    account_id = models.IntegerField(primary_key=True, null=False)
    open_time = models.DateTimeField(auto_now_add=True, null=False)
    balance = models.FloatField(null=False, default=0.0)
    report_loss = models.IntegerField(null=False, default=0)


class turnover(models.Model):
    TYPE_CHOICES = (
        (u'Z', u'支付'),
        (u'C', u'充值')
    )
    turn_id = models.AutoField(primary_key=True, null=False)
    account_id = models.ForeignKey('Balance_account', on_delete=models.CASCADE, null=False)
    time = models.DateTimeField(auto_now_add=True, null=False)
    business_type = models.CharField(choices=TYPE_CHOICES, max_length=20, null=False)
    amount = models.FloatField(default=0, null=False)


class Menu(models.Model):
    dish_name = models.CharField(max_length=255, primary_key=True, null=False)
    r_staff_id = models.ForeignKey("Employee", on_delete=models.CASCADE, null=False)
    price = models.FloatField(null=True, default=0.0)
    picture = models.ImageField()
    stock = models.IntegerField(default=0, null=False)
    special_offer = models.IntegerField(default=10, null=True)

class Location(models.Model):
    loc_id = models.IntegerField(primary_key=True, null=False)
    building = models.CharField(max_length=255, null=False)
    floor = models.IntegerField(null=False, default=1)
    room = models.CharField(max_length=255, null=False, default=0)
    time = models.DateTimeField(null=True)


class Order(models.Model):
    STATUS_CHOICES = (
        (u'0', u'预定状态'),
        (u'1', u'订单开始'),
        (u'2', u'完成支付'),
        (u'3', u'商家已接单'),
        (u'4', u'完成备餐'),
        (u'5', u'骑手已接单'),
        (u'6', u'完成送达')
    )
    METHOD_CHOICES = (
        (u'W', u'微信支付'),
        (u'Z', u'支付宝'),
        (u'Y', u'余额支付')
    )
    EAT_CHOICES = (
        (u'T', u'堂食'),
        (u'W', u'外送')
    )
    order_id = models.IntegerField(primary_key=True, unique=True, null=False)
    dish_name = models.CharField(max_length=20, null=True)
    date = models.DateTimeField(null=True)
    order_status = models.CharField(choices=STATUS_CHOICES, max_length=20, null=False, default='预定状态')
    build_time = models.DateTimeField(null=True)
    payment_time = models.DateTimeField(null=True)
    meal_complete_time = models.DateTimeField(null=True)
    accept_order_time = models.DateTimeField(null=True)
    delivery_time = models.DateTimeField(null=True)
    remark = models.CharField(max_length=256)
    eat_in_store = models.CharField(choices=EAT_CHOICES, max_length=20, null=False)
    specify_delivery_time = models.DateTimeField(null=True)
    location = models.ForeignKey('Location', on_delete=models.CASCADE, null=False)
    payment_method = models.CharField(choices=METHOD_CHOICES, max_length=20, null=False)
    payment_amount = models.FloatField(null=False)
    payment_account_id = models.ForeignKey('Balance_account', on_delete=models.CASCADE)
    payment_id = models.ForeignKey('turnover', null=True, on_delete=models.CASCADE)
    cus_id = models.ForeignKey('Employee', on_delete=models.CASCADE, null=False, related_name='employee1')
    r_staff_id = models.ForeignKey('Employee', on_delete=models.CASCADE, null=False, related_name='employee2')
    r_delivery_id = models.ForeignKey('Employee', on_delete=models.CASCADE, null=True, related_name='employee3')


class order_menu(models.Model):
    order_id = models.ForeignKey('Order', on_delete=models.CASCADE, primary_key=True, null=False)
    dish_name = models.ForeignKey('Menu', on_delete=models.CASCADE, null=False)
    amount = models.IntegerField(null=False, default=1)


class Complaint(models.Model):
    order_id = models.ForeignKey('Order', on_delete=models.CASCADE, primary_key=True, null=False)
    time = models.DateTimeField(null=False)
    type = models.CharField(max_length=255, null=False)
    content = models.TextField(null=False, max_length=255)
    feedback = models.CharField(max_length=255)
