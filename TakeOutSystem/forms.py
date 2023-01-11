from django import forms


class UserForm(forms.Form):
    employee_id = forms.IntegerField(label="employee_id")
    password = forms.CharField(label="password", max_length=256, widget=forms.PasswordInput)


class RegisterForm(forms.Form):
    name = forms.CharField(label="name", max_length=256, widget=forms.TextInput(attrs={'class': 'form-control'}))
    employee_id = forms.IntegerField(label="employee_id", widget=forms.TextInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(label="password", max_length=256, widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label="ensure password", max_length=256, widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    department = forms.CharField(label="department", max_length=256, widget=forms.TextInput(attrs={'class': 'form-control'}))
    # position = forms.ChoiceField(label="position", choices=POSITION_CHOICES)
    position = forms.CharField(label="position", max_length=256, widget=forms.TextInput(attrs={'class': 'form-control'}))
    # email = forms.EmailField(label="e-mail", widget=forms.EmailInput(attrs={'class': 'form-control'}))
    # sex = forms.ChoiceField(label='gender', choices=gender)


class ComplainForm(forms.Form):
    TYPE_CHOICES = (
        (u'r_staff', u'餐厅员工'),
        (u'r_delivery', u'餐厅外卖员')
    )
    order_id = forms.IntegerField(label='order_id')
    type = forms.CharField(label='type', max_length=255, widget=forms.TextInput(attrs={'class': 'form-control'}))
    content = forms.CharField(label='content', max_length=255, widget=forms.TextInput(attrs={'class': 'form-control'}))
    feedback = forms.CharField(label='feedback', max_length=255, widget=forms.TextInput(attrs={'class': 'form-control'}))


class EmployeeForm(forms.Form):
    employee_id = forms.IntegerField(label='employee_id', widget=forms.TextInput(attrs={'class': 'form-control'}))
    name = forms.CharField(label='name', max_length=255, widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label='password', max_length=255, widget=forms.TextInput(attrs={'class': 'form-control'}))
    department = forms.CharField(label='department', max_length=255, widget=forms.TextInput(attrs={'class': 'form-control'}))
    position = forms.CharField(label='position', max_length=255, widget=forms.TextInput(attrs={'class': 'form-control'}))


class AccountForm(forms.Form):
    employee_id = forms.IntegerField(label='employee_id', widget=forms.TextInput(attrs={'class': 'form-control'}))
    account_id = forms.IntegerField(label='account_id', widget=forms.TextInput(attrs={'class': 'form-control'}))
    balance = forms.IntegerField(label='balance', widget=forms.TextInput(attrs={'class': 'form-control'}))
    report_loss = forms.IntegerField(label='report_loss', widget=forms.TextInput(attrs={'class': 'form-control'}))


class MenuForm(forms.Form):
    dish_name = forms.CharField(label='dish_name', max_length=255, widget=forms.TextInput(attrs={'class': 'form-control'}))
    r_staff_id = forms.IntegerField(label='r_staff_id', widget=forms.TextInput(attrs={'class': 'form-control'}))
    price = forms.IntegerField(label='price')
    # picture = forms.ImageField(label='picture', widget=forms.TextInput(attrs={'class': 'form-control'}))
    stock = forms.IntegerField(label='stock', widget=forms.TextInput(attrs={'class': 'form-control'}))
    special_offer = forms.IntegerField(label='special_offer')

class LocationForm(forms.Form):
    loc_id = forms.IntegerField(label='loc_id', widget=forms.TextInput(attrs={'class': 'form-control'}))
    building = forms.CharField(label='building', max_length=255, widget=forms.TextInput(attrs={'class': 'form-control'}))
    floor = forms.IntegerField(label='floor', widget=forms.TextInput(attrs={'class': 'form-control'}))
    room = forms.CharField(label='room', max_length=255, widget=forms.TextInput(attrs={'class': 'form-control'}))


class OrderForm(forms.Form):
    STATUS_CHOICES = (
        (u'0', u'预定状态'),
        (u'1', u'订单开始'),
        (u'2', u'完成支付'),
        (u'3', u'完成备餐'),
        (u'4', u'完成接单'),
        (u'5', u'完成送达')
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
    order_id = forms.IntegerField(label='order_id', widget=forms.TextInput(attrs={'class': 'form-control'}))
    dish_name = forms.CharField(label='dish_name', max_length=255, widget=forms.TextInput(attrs={'class': 'form-control'}))
    order_status = forms.CharField(label='order_status', max_length=255, widget=forms.TextInput(attrs={'class': 'form-control'}))
    build_time = forms.DateTimeField(label='build_time', widget=forms.TextInput(attrs={'class': 'form-control'}))
    payment_time = forms.DateTimeField(label='payment_time', widget=forms.TextInput(attrs={'class': 'form-control'}))
    meal_complete_time = forms.DateTimeField(label='meal_complete_time', widget=forms.TextInput(attrs={'class': 'form-control'}))
    accept_order_time = forms.DateTimeField(label='accept_order_time', widget=forms.TextInput(attrs={'class': 'form-control'}))
    delivery_time = forms.DateTimeField(label='delivery_time', widget=forms.TextInput(attrs={'class': 'form-control'}))
    remark = forms.CharField(label='remark', max_length=255, widget=forms.TextInput(attrs={'class': 'form-control'}))
    eat_in_store = forms.CharField(label='eat_in_store', max_length=255, widget=forms.TextInput(attrs={'class': 'form-control'}))
    specify_delivery_time = forms.CharField(label='specify_delivery_time', widget=forms.TextInput(attrs={'class': 'form-control'}))
    location = forms.IntegerField(label='location', widget=forms.TextInput(attrs={'class': 'form-control'}))
    payment_method = forms.CharField(label='payment_method', max_length=255, widget=forms.TextInput(attrs={'class': 'form-control'}))
    payment_amount = forms.FloatField(label='payment_amount', widget=forms.TextInput(attrs={'class': 'form-control'}))
    payment_account_id = forms.IntegerField(label='payment_account_id', widget=forms.TextInput(attrs={'class': 'form-control'}))
    payment_id = forms.IntegerField(label='payment_id', widget=forms.TextInput(attrs={'class': 'form-control'}))
    cus_id = forms.IntegerField(label='cus_id', widget=forms.TextInput(attrs={'class': 'form-control'}))
    r_staff_id = forms.IntegerField(label='r_staff_id', widget=forms.TextInput(attrs={'class': 'form-control'}))
    r_delivery_id = forms.IntegerField(label='r_delivery_id', widget=forms.TextInput(attrs={'class': 'form-control'}))