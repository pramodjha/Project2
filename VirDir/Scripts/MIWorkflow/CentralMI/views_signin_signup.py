from django.shortcuts import render, render_to_response, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import Group

from .forms import  UserRegistrationForm, UsersigninForm, UserForm, UsersigninasotherForm
from django.urls import reverse
import datetime
import getpass


def Sign_Up_View_Version1(request):
    activetab = 'signup'
    system_username = getpass.getuser()
    system_username = system_username.replace('$','')

    #system_username = system_username.replace(" ", "")
    form = UserRegistrationForm(initial={'username':system_username})
    Authusercount = User.objects.filter(username__in=[system_username]).count()
    if Authusercount >= 1:
        msg = "Username already Exists, you can't register with same username again"
    else:
        msg = ""
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            userObj = form.cleaned_data
            username =  userObj['username']
            email =  userObj['email']
            password =  userObj['password']
            passwordagain =  userObj['passwordagain']
            firstname =  userObj['firstname']
            lastname =  userObj['lastname']
            if password == passwordagain:
                if not (User.objects.filter(username=username).exists() ):
                    new_user = User.objects.create_user(username, email, password)
                    new_user.is_active = True
                    new_user.first_name = firstname
                    new_user.last_name = lastname
                    new_user.save()
                    my_group = Group.objects.get(name='others')
                    new_user.groups.add(my_group)
                    try:
                        user = authenticate(username = username, password = password)
                        login(request, user)
                        return HttpResponseRedirect(reverse('home'))
                    except:
                        form =  UserRegistrationForm()
                        return render(request,'CentralMI/15a_ErrorPage.html')
    context = {'form' : form,'activetab':activetab,'msg':msg,'system_username':system_username}
    return render(request, 'CentralMI/1a_signup_view.html', context)


def Sign_Up_View_Version2(request):
    activetab = 'signup'
    system_username = request.META['REMOTE_USER']
    system_username = system_username.replace('$','')

    #system_username = system_username.lower()
    #system_username = system_username[4:]
    form = UserRegistrationForm(initial={'username':system_username})
    Authusercount = User.objects.filter(username__in=[system_username]).count()
    if Authusercount >= 1:
        msg = "Username already Exists, you can't register with same username again"
    else:
        msg = ""
    form = UserRegistrationForm(initial={'username':system_username})
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            userObj = form.cleaned_data
            username =  userObj['username']
            email =  userObj['email']
            password =  userObj['password']
            passwordagain =  userObj['passwordagain']
            firstname =  userObj['firstname']
            lastname =  userObj['lastname']
            if password == passwordagain:
                if not (User.objects.filter(username=username).exists() ):
                    new_user = User.objects.create_user(username, email, password)
                    new_user.is_active = True
                    new_user.first_name = firstname
                    new_user.last_name = lastname
                    new_user.save()
                    my_group = Group.objects.get(name='others')
                    new_user.groups.add(my_group)
                    try:
                        user = authenticate(username = username, password = password)
                        login(request, user)
                        return HttpResponseRedirect(reverse('checkdetail'))
                    except:
                        form =  UserRegistrationForm()
                        return render(request,'CentralMI/15a_ErrorPage.html')
    context = {'form' : form,'activetab':activetab,'msg':msg,'system_username':system_username}
    return render(request, 'CentralMI/1a_signup_view.html', context)


def Sign_In_View_Version1(request):
    try:
        activetab, activetab1, username, info, sd = create_session(request, header='signin',footer='')
    except:
        activetab = 'signin'
    tab = request.session.get('tabname')
    system_username = getpass.getuser()
    system_username = system_username.replace('$','')
    #system_username = system_username.replace(" ", "")
    form = UsersigninForm(initial={'username':system_username})
    if request.method == 'POST':
        form =  UsersigninForm(request.POST)
        if form.is_valid():
            userObj = form.cleaned_data
            username =  userObj['username']
            if (User.objects.filter(username=username).exists()):
                user = User.objects.get(username = system_username)
                user.backend = 'django.contrib.auth.backends.ModelBackend'
                login(request, user)
                return HttpResponseRedirect(reverse('checkdetail'))
    context = {'form' : form,'activetab':activetab,'system_username':system_username}
    return render(request, 'CentralMI/1b_signin_view.html', context)

def Sign_In_View_Version2(request):
    try:
        activetab, activetab1, username, info, sd = create_session(request, header='signin',footer='')
    except:
        activetab = 'signin'
    tab = request.session.get('tabname')
    system_username = request.META['REMOTE_USER']
    system_username = system_username.replace('$','')

    #system_username = system_username.lower()
    #system_username = system_username[4:]
    form = UsersigninForm(initial={'username':system_username})
    if request.method == 'POST':
        form =  UsersigninForm(request.POST)
        if form.is_valid():
            userObj = form.cleaned_data
            username =  userObj['username']
            if (User.objects.filter(username=username).exists()):
                user = User.objects.get(username = system_username)
                user.backend = 'django.contrib.auth.backends.ModelBackend'
                login(request, user)
                return HttpResponseRedirect(reverse('checkdetail'))
    context = {'form' : form,'activetab':activetab,'system_username':system_username}
    return render(request, 'CentralMI/1b_signin_view.html', context)

def Sign_In_As_Other_View_Version1(request):
    try:
        activetab, activetab1, username, info, sd = create_session(request, header='signin',footer='')
    except:
        activetab = 'signin'
    tab = request.session.get('tabname')
    form = UsersigninasotherForm()
    if request.method == 'POST':
        form =  UsersigninasotherForm(request.POST)
        if form.is_valid():
            userObj = form.cleaned_data
            username =  userObj['username']
            password =  userObj['password']
            if (User.objects.filter(username=username).exists()):
                user = authenticate(username = username, password = password)
                if user is not None:
                    login(request, user)
                    return HttpResponseRedirect(reverse('home'))
    context = {'form' : form,'activetab':activetab}
    return render(request, 'CentralMI/1b_signin_other_view.html',context)
