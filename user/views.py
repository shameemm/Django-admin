from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse

# Create your views here.
# @login_required(login_url='login')
def login(request):
    if 'username' in request.session:
        print(request.session)
        return redirect(to='home')
    
    if request.method == 'POST':
        username=request.POST['uname']
        password=request.POST['pswd']
        if len(username) == 0 or len(password) == 0:
            messages.info(request, 'Please enter all fields')
            return redirect(to='login')
        else:
            user = auth.authenticate(username=username, password=password)
            
            if user is not None and user.is_superuser==False:
                auth.login(request, user)
                request.session['username'] = username
                return redirect(to='home')
            else:
                messages.info(request, 'Invalid credentials')
                return redirect(to='login')
        user = auth.authenticate(username=username,password=password)
        
            
    else:
        return render(request, 'login.html')

def signup(request):
    if request.method == 'POST':
        first_name = request.POST['fname']
        last_name = request.POST['lname']
        email = request.POST['email']
        username = request.POST['uname']
        password = request.POST['pswd']
        if len(username) == 0 or len(password) == 0 or len(email)==0 or len(first_name)==0 or len(last_name)==0:
            messages.info(request, 'Please enter all fields')
            return redirect(to='signup')
        if User.objects.filter(username=username).exists():
            messages.info(request, 'Username Taken')
            return redirect('signup')
        elif User.objects.filter(email=email).exists():
            messages.info(request, 'Email Exists')
            return redirect('signup')
        else:
            print(password)
            user = User.objects.create_user(username=username, password=password, first_name=first_name, last_name=last_name, email=email, )
            user.save()
            print('success')
            return redirect(to='login')
    else:
        return render(request, 'signup.html')
@login_required(login_url='login')
def home(request):
    return render(request, 'index.html')
@login_required(login_url='login')
def logout(request):
    auth.logout(request)
    return redirect(to='login')


