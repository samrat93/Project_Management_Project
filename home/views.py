from ast import Assign
from asyncio import tasks
from distutils.log import error
from tokenize import group
from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import logout
from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect
from register.models import Company
from register.models import Project
from register.models import UserProfile
from projects.models import Task
import psutil, os
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from django.contrib.auth.hashers import make_password





def index(request):
    """ Function to display index """

    projects = Project.objects.all()
    return render(request, 'core/index.html',{'projects':projects})


def dashboard(request):
    """ Function to display dashboard of the website """

    users = User.objects.all()
    active_users = User.objects.all().filter(is_active=True)
    companies = Company.objects.all()
    projects = Project.objects.all()
    tasks = Task.objects.all()
    cup_usage = psutil.cpu_percent(4)
    #print('jjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjj',cup_usage)
    context = {
        'users' : users,
        'active_users' : active_users,
        'companies' : companies,
        'projects' : projects,
        'tasks' : tasks,
        'cpu_usage':cup_usage,
    }
    return render(request, 'core/dashboard.html', context)


def login_view(request):
    """ Function to login user """

    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            authenticated_user = authenticate(username=request.POST['username'], password=request.POST['password'])
            login(request, authenticated_user)
            return redirect('home:index')
        else:
            return render(request, 'register/login.html', {'login_form':form})
    else:
        form = AuthenticationForm()
    return render(request, 'register/login.html', {'login_form':form})


def logout_view(request):
    """ Function to logout user """

    logout(request)
    return HttpResponseRedirect(reverse('home:index'))


def forget_password_view(request):
    """ Function to check username and redirect to password reset page """

    if request.method == "POST":
        username = request.POST.get('username')
        try:
            user = User.objects.get(username = username)
        except ObjectDoesNotExist:
            messages.warning(request, 'Please Create your account first !!!')
            return render(request, 'register/forget_password.html')
        if user:
            if username == user.username:
                request.session['user'] = user.id
                return redirect('home:new-password')
            else:
                messages.info(request, 'Username not found !!!')
                return render(request, 'register/forget_password.html')
        else:
            messages.info(request, 'Username not found !!!')
    return render(request, 'register/forget_password.html')


def new_password_view(request):
    """ Function to reset new password """

    u_id = request.session['user']
    user = User.objects.get(id = u_id)

    if request.method == "POST":
        pwd = request.POST.get('new_password')
        c_pwd = request.POST['con_pass']
        error_message = None
        if pwd == c_pwd:
            enccrypt_pwd = make_password(pwd)
            user.password = enccrypt_pwd
            user.save()
            messages.success(request, 'Password Reset Successfully.')
            return redirect('home:index')
        else:
            messages.warning(request, 'Password does not match')
            return redirect('home:new-password')
    return render(request, 'register/new_password.html')


def context(request): # send context to base.html
    # if not request.session.session_key:
    #     request.session.create()
    users = User.objects.all()
    users_prof = UserProfile.objects.all()
    if request.user.is_authenticated:
        try:
            users_prof = UserProfile.objects.exclude(
                id=request.user.userprofile_set.values_list()[0][0])  # exclude himself from invite list
            user_id = request.user.userprofile_set.values_list()[0][0]
            logged_user = UserProfile.objects.get(id=user_id)
            friends = logged_user.friends.all()
            context = {
                'users': users,
                'users_prof': users_prof,
                'logged_user': logged_user,
                'friends' : friends,
            }
            return context
        except:
            users_prof = UserProfile.objects.all()
            context = {
                'users':users,
                'users_prof':users_prof,
            }
            return context
    else:
        context = {
            'users': users,
            'users_prof': users_prof,
        }
        return context


@login_required
def change_password_view(request):
    """ Function to change password of logedin user """

    if request.user.is_authenticated:
        if request.method == 'POST':
            old_password = request.POST['old_password']
            new_password = request.POST['new_password']
            con_pass = request.POST['con_pass']
            if new_password == con_pass:
                user = authenticate(request, username= request.user, password = old_password)
                if user is not None:
                    user = User.objects.get(username = request.user.username)
                    user.set_password(new_password)
                    user.is_visit = True
                    user.save()
                    messages.success(request, "Password Has Been Changed")
                    return redirect('home:index')
                else:
                    messages.warning(request, "Old password not match !!!")
                    return redirect('home:change-password')
            else:
                messages.warning(request, "Password does not match")
                return redirect('home:change-password')
        else:
            # messages.success(request, "Something went wrong !!!")
            return render(request, 'register/change_password.html')
    else:
        return render(request, 'register/change_password.html')
    

def user_task_view(request):
    """ Function to show the assigned task of logged in user """
    
    u_id = request.user.id
    task_details = Task.objects.all()
    projects = Project.objects.all()
    user_task = Task.objects.filter(assign = u_id)
    context = {
        'projects' : projects,
        'user_task' : user_task,
    }

    print('current user id : ', u_id)
    print('Task assigned to user : ',user_task)
    if request.user.is_authenticated:
        return render(request, 'core/user_task.html',context)
    else:
        return render(request, 'core/index.html')