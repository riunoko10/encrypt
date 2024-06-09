from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django import forms
from django.urls import reverse
from .tools import hash_data, hash_data_md5, rc_encrypt, generate_key, hash_data_sha512
from .models import DataUser, LoginUser


MY_KEY = b"\xa2X\x19?\xe6\x0cx\xca'\x19\xfe\xdd7\xc5To"

class newForm(forms.Form):
    username = forms.CharField(label='Username', max_length=100)
    password = forms.CharField(
        label='Password', 
        max_length=100, 
        widget=forms.PasswordInput
    )

class registerForm(forms.Form):
    username = forms.CharField(label='Username', max_length=100)
    password = forms.CharField(
        label='Password', 
        max_length=100, 
        widget=forms.PasswordInput
    )
    re_password = forms.CharField(
        label='Re-Password', 
        max_length=100, 
        widget=forms.PasswordInput
    )

class userInfoForm(forms.Form):
    name = forms.CharField(label='Name', max_length=100)
    email = forms.EmailField(label='Email')
    phone = forms.CharField(label='Phone', max_length=15)
    address = forms.CharField(label='Address', max_length=100)


def index(request):
    return render(request, 'digets/index.html')

def hash(request):
    if request.method == 'POST':
        form = newForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            hash_user = hash_data(username)
            hash_pass = hash_data(password)
            
            return render(request, 'digets/hash.html', {
                'form_hash': newForm(),
                'user': hash_user,
                'pass': hash_pass
                })
    return render(request, 'digets/hash.html', {
        'form_hash': newForm()
        })
    

def md5(request):
    if request.method == 'POST':
        form = newForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            hash_user = hash_data_md5(username)
            hash_pass = hash_data_md5(password)
            
            return render(request, 'digets/md5.html', {
                'form_md5': newForm(),
                'user': hash_user,
                'pass': hash_pass
                })
    return render(request, 'digets/md5.html', {
        'form_md5': newForm()
        })


def rc4(request):
    if request.method == 'POST':
        form = newForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            key = generate_key()
            enc_user = rc_encrypt(key, username)
            enc_pass = rc_encrypt(key, password)
            
            return render(request, 'digets/rc4.html', {
                'form_rc4': newForm(),
                'user': enc_user,
                'pass': enc_pass,
                'key': key
                })
    return render(request, 'digets/rc4.html', {
        'form_rc4': newForm()
        })


def login(request):
    if request.method == 'POST':
        form = newForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            encripted_user = hash_data_sha512(username)
            encripted_pass = hash_data_sha512(password)
            print(encripted_user)
            print(encripted_pass)
            try:
                user = LoginUser.objects.get(
                    username=encripted_user, 
                    password=encripted_pass
                )
                return HttpResponseRedirect(reverse("user", args=(username,)))
            except LoginUser.DoesNotExist:
                return render(request, 'digets/login.html', {
                    'form_login': newForm(),
                    'message': 'Login failed!'
                })
        
    return render(request, 'digets/login.html', {
        'form_login': newForm()
    })


def register(request):
    if request.method == 'POST':
        form = registerForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            re_password = form.cleaned_data['re_password']
            if password != re_password:
                return render(request, 'digets/register.html', {
                    'form_register': registerForm(),
                    'message': 'Password not match!'
                })
            else:
                encripted_user = hash_data_sha512(username)
                encripted_pass = hash_data_sha512(password)
                login = LoginUser(username=encripted_user, password=encripted_pass)
                login.save()
                return render(request, 'digets/register.html', {
                    'form_register': registerForm(),
                    'message': 'Register success! - to login.'
                })
    return render(request, 'digets/register.html', {
        'form_register': registerForm()
    })

def user(request, username):
    if request.method == 'POST':
        form = userInfoForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            phone = form.cleaned_data['phone']
            address = form.cleaned_data['address']
            user = DataUser(
                name=name, 
                email=email, 
                phone=phone, 
                address=address
            )
            user.save()
            userInfo = DataUser.objects.get(name=name)
            encripted_user = hash_data_sha512(username)
            user = LoginUser.objects.get(username=encripted_user)
            user.dataUser_id = userInfo.id
            user.save()
            return render(request, 'digets/user.html', {
                'user_info': userInfoForm(),
                'username': username,
                'message': 'Data saved!',
                "user_data": userInfo
            })
    encripted_user = hash_data_sha512(username)
    user = LoginUser.objects.get(username=encripted_user)
    userInfo = DataUser.objects.filter(id=user.dataUser_id).first()
    print(userInfo)
    return render(request, 'digets/user.html', {
        'user_info': userInfoForm(),
        'username': username, 
        'user_data': userInfo
    })