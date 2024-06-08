from django.shortcuts import render
from django.http import HttpResponse
from django import forms
from .tools import hash_data, hash_data_md5, rc_encrypt, rc_decrypt, generate_key

class newForm(forms.Form):
    username = forms.CharField(label='Username', max_length=100)
    password = forms.CharField(
        label='Password', 
        max_length=100, 
        widget=forms.PasswordInput
    )


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
    return render(request, 'digets/login.html')