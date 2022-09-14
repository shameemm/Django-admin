from django.shortcuts import render,redirect
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse

# Create your views here.

def adminlogin(request):
    if 'uname' in request.session:
        return redirect(to='adminhome')
    if request.method == 'POST':
        username = request.POST['uname']
        password = request.POST['pswd']
        if len(username) == 0 or len(password) == 0:
            messages.info(request, 'Please enter all fields')
            return redirect(to='login')
        
        user = auth.authenticate(username=username, password=password)
        if user is not None and user.is_superuser:
            auth.login(request, user)
            request.session['uname'] = username
            return redirect('adminhome')
            
        else:
            messages.info(request, 'Invalid credentials')
            return render(request, 'adlogin.html')
    else:
        return render(request, 'adlogin.html')
    
@login_required(login_url='adminlogin')
def edituser(request):
    id=request.GET['id']
    if request.method=='POST':
        fname=request.POST['firstname']
        lname=request.POST['lastname']
        email=request.POST['email']
        username=request.POST['uname']
        password=request.POST['password']
        
        user = User.objects.create_user(id=id,username=username, password=password, first_name=fname, last_name=lname, email=email)
        print(user.password)
        user.save_base()
        print('success')
        return redirect('adminhome')
    else:
        user=User.objects.filter(id=id)
        return render(request, 'edituser.html',{'user':user})

@login_required(login_url='adminlogin')
def deleteuser(request):
    id=request.GET['id']
    user=User.objects.filter(id=id)
    user.delete()
    return redirect('adminhome')



@login_required(login_url='adminlogin')
def adduser(request):
    if request.method=='POST':
        first_name = request.POST['firstname']
        last_name = request.POST['lastname']
        email = request.POST['email']
        username = request.POST['uname']
        password = request.POST['password']
        if len(username) == 0 or len(password) == 0 or len(first_name)==0 or len(last_name)==0 or len(email)==0:
            messages.info(request, 'Please enter all fields')
            return redirect(to='adduser')
        if User.objects.filter(username=username).exists():
            messages.info(request, 'Username Taken')
            return redirect('adduser')
        elif User.objects.filter(email=email).exists():
            messages.info(request, 'Email Exists')
            return redirect('adduser')
        else:
            user = User.objects.create_user(username=username, password=password, first_name=first_name, last_name=last_name, email=email)
            user.save()
            print(password)
            return redirect(to='adminhome')
    else:
        return render(request, 'adduser.html')

@login_required(login_url='adminlogin')    
def adminhome(request):
    if 'search' in request.POST:
        search = request.POST['search']
        users = User.objects.filter(username__contains=search)
        if len(users)!=0:
            return render(request, 'admin_home.html',{'users':users})
        else:
            messages.info(request, "No Matches found")
            return redirect('adminhome')
    else:
        users=User.objects.filter(is_superuser=False)
        return render(request, 'admin_home.html',{'users':users})

@login_required(login_url='adminlogin')
def adminout(request):
    auth.logout(request)
    return redirect('adminlogin')
    
