from django.shortcuts import render
from basic_app.forms import UserForm, UserProfileInfoForm
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required

# Create your views here.

def index(request):
    return render(request, 'basic_app/index.html')

@login_required
def user_logout(request):
    logout(request)
    #return HttpResponseRedirect(reverse('logout'))
    return render(request, 'basic_app/logout.html')

@login_required
def special(request):
    return HttpResponse("You are logged in . Nice!!")

def user_login(request):

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        print(f"username {username} and password {password}")
        user = authenticate(username=username, password=password)

        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('index'))
            else:
                print('User is inactive')
                return HttpResponse('Account Not Active')

        else:
            print(f"{username} tried to login using password {password} and failed")
            return HttpResponse('Invalid login credentials supplied!!')

    else:
        return render(request, 'basic_app/login.html',{'showlogin':True})


def register(request):

    registered = False

    if request.method == 'POST':
        user_form = UserForm(request.POST)
        userprofile_form = UserProfileInfoForm(request.POST)

        if user_form.is_valid() and userprofile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()

            user_profile = userprofile_form.save(commit=False)
            user_profile.user = user

            if 'profile_pic' in request.FILES:
                user_profile.profile_pic = request.FILES['profile_pic']
            user_profile.save()

            registered = True
        else:
            print(user_form.errors, userprofile_form.errors)
    else:
        user_form = UserForm()
        userprofile_form = UserProfileInfoForm()

    return render(request, 'basic_app/register.html', {'user_form':user_form, 'profile_form':userprofile_form, 'registered':registered})
