from django.shortcuts import render, redirect
from django.http.response import HttpResponse, HttpResponseNotFound,Http404,HttpResponseRedirect
from django.urls import reverse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth import logout

from .forms import NewUserForm
from django.contrib.auth import login, authenticate

# Create your views here.

@csrf_protect
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        print(username)
        if user is not None:
            login(request, user)
            print("login success")
            return HttpResponseRedirect(reverse('base:main'))  # Redirect to a success page.
        else:
            print("login fail")
            return render(request, 'login/login.html', context={'error': 'Invalid username or password'})
    else:
        return render(request, 'login/login.html')

def register_request(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            # login(request, user)

            return redirect("login:account_succeed")
    else:
        form = NewUserForm()
    return render (request=request, template_name="login/register.html", context={"register_form":form})

def account_succeed(request):
    return render(request, 'login/account_succeed.html')

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('login:login'))  # Redirect to a success page