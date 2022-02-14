from distutils.log import error
from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import logout
from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.urls import reverse
from django.http import HttpResponseRedirect
from register.models import Company
from register.models import Project
from register.models import UserProfile
from projects.models import Task
import psutil, os
from django.contrib import messages
from django.contrib.auth.hashers import make_password

# Create your views here.
def index(request):
    return render(request, 'core/index.html')

def dashboard(request):
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
    logout(request)
    return HttpResponseRedirect(reverse('home:index'))


def forget_password_view(request):
    
    username = request.POST.get('username')
    user_name = User.objects.filter(username = username).exists()
    user = authenticate(request, username = user_name)
    user = User.objects.get(username = request.user.username)
    print('uuuuuuuuuuuuuuuuuuuuuuuuuuuuuu',user)
    error_message = None
    if user:
        if username == user.username:
            u_id = request.session['username'] = user.id
            print('iiiiiiiiiiiiiiiiiiiiiiii',u_id)
            return redirect('home:new-password')
        else:
            error_message = 'Username not exist. Please try again !!!'
    else:
        error_message = 'Username not exist. Please try again !!!'
    return render(request, 'register/forget_password.html',{'error':error_message})



def new_password_view(request):
    # # # get_session_id = request.session['username']
    # # # data = User.objects.get(id = get_session_id)
    
    # password = request.POST.get('password')
    # c_pass = request.POST.get('con_pass')
    # # error_message = None
    # # user = User(password = password)
    # if password == c_pass:
    #     # data.set_password(password)
    #     # data.save()
    #     return redirect('home:index')
    # else:
    #     error_message = 'Something went Wrong !!!'
    # return render(request, 'register/new_password.html')
    error_message = None
    if request.POST:
        password = request.POST.get('password')
        c_pass = request.POST.get('con_pass')
        if password == c_pass:
            return redirect('home:index')
        else:
            messages.info(request,'Password not matching...')
    else:
        return render(request, 'register/new_password.html',{'error':error_message})


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

