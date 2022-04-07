
from django.shortcuts import render,HttpResponse,redirect
from django import forms
from django.forms import widgets
from django.urls import reverse

from app01.models import UserInfo,DateInfo

from django.core.exceptions import ValidationError

from Crypto.Hash import MD5
from Crypto.Cipher import AES


N = b'\x94\x87\x90\xcd"\xaa\x04\xe9\xf1\xe3\xd2\x81\xe7J%\x1c'



wid_01 = widgets.TextInput(attrs={"class":"form-control"})
wid_02 = widgets.PasswordInput(attrs={"class":"form-control"})
wid_03 = widgets.URLInput(attrs={"class":"form-control", "value":"http://www.baidu.com"})

class UserForm(forms.Form):
    name=forms.CharField(max_length=32,
                         widget=wid_01,
                         label='姓名'
                         )
    pwd=forms.CharField(max_length=32,widget=wid_02,label='密码')
    key= forms.CharField(max_length=8,widget=wid_02, label='密钥')
    # r_pwd=forms.CharField(max_length=32,widget=wid_02)
    # email=forms.EmailField(widget=wid_01)
    # tel=forms.CharField(max_length=32,widget=wid_01)

class LoginForm(forms.Form):
    name=forms.CharField(max_length=32,
                         widget=wid_01,
                         label='姓名'
                         )
    pwd=forms.CharField(max_length=32,widget=wid_02,label='密码')

class DataForm(forms.Form):
    site = forms.URLField(max_length=32, widget=wid_03,label='网站')
    account =  forms.CharField(max_length=32,widget=wid_01,label='账户')
    password = forms.CharField(max_length=32,widget=wid_02,label='密码')


def show(request):
    all =  UserInfo.objects.all()
   
    return render(request,'show.html',{'all':all})


###############

def index(request):
    return render(request,'index.html')

def register(request):
    form = UserForm()

    if request.method == 'POST':
        user = request.POST.get('name')
        pwd = request.POST.get('pwd')
        key = request.POST.get('key')

        while len(key) < 16:
            key += '0'

        h = MD5.new()
        h.update(key.encode('utf8'))

        if UserInfo.objects.filter(name=user):
            message = '用户名已存在'
        else:
            UserInfo.objects.create(name=user, pwd=pwd, key=h.hexdigest())
            message = '注册成功'
    return render(request, 'register.html', locals())

def login(request):
    form = LoginForm()
    if request.method == 'POST':
        user = request.POST.get('name')
        pwd = request.POST.get('pwd')
        if UserInfo.objects.filter(name = user):
            if UserInfo.objects.get(name = user).pwd == pwd:
                id = UserInfo.objects.get(name = user).id
                return redirect(reverse('id_index',args=(id,)))
            else:
                message = '密码错误'
        else:
            message = '用户不存在'

    return render(request, 'login.html', locals())

def id_index(request,id):
    
    userinfo = UserInfo.objects.get(id=id) 
    objects = userinfo.dateinfo_set.all()

    url_add = reverse('id_add',args=(id,))
    url_secret = reverse('id_secret',args=(id,))


    return render(request, 'id_index.html', locals())

def id_info(request,id):
    userinfo = UserInfo.objects.get(id=id) 
    return render(request, 'id_info.html', locals())

def id_add(request, id):
    form = DataForm()
    if request.method == 'POST':
        userinfo = UserInfo.objects.filter(id=id).first()
        form=DataForm(request.POST)
        key = request.POST.get('key')
        while len(key) < 16:
            key += '0'

        h = MD5.new()
        h.update(key.encode('utf8'))
        if h.hexdigest()==userinfo.key:
            if form.is_valid():

                pwd = form.cleaned_data['password']
                print(pwd)
                print(key)
                
                e_cipher = AES.new(key.encode('utf8'), AES.MODE_EAX, N)
                e_data = e_cipher.encrypt(pwd.encode('utf8'))

                e_cipher = AES.new(key.encode('utf8'), AES.MODE_EAX, N)
                S = e_cipher.decrypt(e_data)

                form.cleaned_data['password'] = e_data
                pwd = form.cleaned_data['password']
                print(pwd)
                print(S.decode('utf-8'))
                if DateInfo.objects.filter(site=form.cleaned_data['site'], userinfo=userinfo, account=form.cleaned_data['account']):
                    DateInfo.objects.filter(account=form.cleaned_data['account']).update(**form.cleaned_data, userinfo=userinfo)
                    request.session['m'] = '更新了旧数据'
                else:
                    DateInfo.objects.create(**form.cleaned_data, userinfo=userinfo)
                    request.session['m'] = '创建了新数据'
        else:
            request.session['m'] = '密钥错误！添加失败'


        return redirect(reverse('id_index',args=(id,)))
    else:
        title = '添加'
        return render(request, 'id_add.html', locals())

def id_delete(request,id,data_id):
    DateInfo.objects.filter(id=data_id).delete()
    return redirect(reverse('id_index',args=(id,)))

def id_edit(request,id,data_id):
    obj = DateInfo.objects.filter(id=data_id).first()
    class DataEditForm(forms.Form):
        site = forms.URLField(max_length=32, widget=wid_03,label='网站')
        account =  forms.CharField(max_length=32,widget=wid_01,label='账户')
        key = forms.CharField(max_length=16,widget=wid_02,label='密钥') 
        password_new = forms.CharField(max_length=32,widget=wid_02,label='新密码') 

        def __init__(self,):
            super().__init__()
            self.fields['site'].initial = obj.site
            self.fields['account'].initial = obj.account
    if request.method == 'POST':
        site = request.POST.get('site')
        account = request.POST.get('account')
        key = request.POST.get('key')
        password_new = request.POST.get('password_new')

        while len(key) < 16:
            key += '0'

        print(key)
        h = MD5.new()
        h.update(key.encode('utf8'))

        e_cipher = AES.new(key.encode('utf8'), AES.MODE_EAX)
        e_data = e_cipher.encrypt(password_new.encode('utf8'))


        if h.hexdigest() == UserInfo.objects.filter(id=id).first().key:
            print('密钥正确')
            DateInfo.objects.filter(id=data_id).update(site= site, account=account, password=e_data)
            request.session['m'] = '密钥正确！更新成功'
        else:
            print('密钥错误')
            request.session['m'] = '密钥错误！更新失败'

        return redirect(reverse('id_index',args=(id,)))
    else:
        
        form = DataEditForm()
        title = '更新'
        return render(request, 'id_edit.html', locals())

def id_secret(request,id):
    if request.method == 'POST':
        userinfo = UserInfo.objects.get(id=id) 
        key = request.POST.get('key')

        while len(key) < 16:
            key += '0'

        h = MD5.new()
        h.update(key.encode('utf8'))
        if h.hexdigest() != userinfo.key:
            print('no')
            request.session['m'] = '密钥错误!'
            userinfo = UserInfo.objects.get(id=id) 
            objects = userinfo.dateinfo_set.all()
            
            url_add = reverse('id_add',args=(id,))
            url_secret = reverse('id_secret',args=(id,))
            return render(request, 'id_index.html',locals())
        else:
            request.session['m'] = '密钥正确，解密成功!'

            objects = userinfo.dateinfo_set.all()
            key = '1000000000000000'
            for obj in objects:
                e_cipher = AES.new(key.encode('utf-8'), AES.MODE_EAX, N)
                obj.password = e_cipher.decrypt(obj.password).decode('utf-8')
            secret = True
            
            return render(request, 'id_index.html',locals())
    else:
        return render(request, 'index.html')