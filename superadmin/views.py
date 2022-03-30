from itertools import count
from django.shortcuts import render,redirect
from django.contrib.auth.models import User, auth
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import connection
from django.contrib.auth import get_user_model
from .choices import *
from .email import *

from django import template

from superadmin.models import Customer, Goal, SocialIcon
User = get_user_model()

def tables():
    table = []
    tables = connection.introspection.table_names()
    seen_models = connection.introspection.installed_models(tables)
    for i in seen_models:
        table.append(i)
    return table


@login_required
def homepage(request):
    template_name = 'index.html'
    table = ['User', 'Goal']
    goal = Goal.objects.filter().count()
    user = User.objects.filter(user_type='USER').count()
    vendor = User.objects.filter(user_type='VENDOR').count()
    return render(request, template_name, {'table':table, 'goal':goal, 'user':user, 'vendor':vendor})


def loginSuperAdmin(request):
    template_name = 'login.html'
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        admin = auth.authenticate(email=email,  password=password)
        if admin.is_superuser == True:
            auth.login(request, admin)
            messages.success(request, "You have Successfully Registerd!")
            return redirect('dashboard')
        elif admin is None:
            messages.error(request, "Invalid username or password ")
            return redirect('login')
    return render(request, template_name)


def tables(request):
    template_name = 'users.html'
    user = User.objects.filter(user_type='USER')
    return render(request, template_name, {'user': user})

def addUser(request):
    template_name = 'add-user.html'
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        mobile = request.POST.get('mobile')
        user_type = request.POST.get('user_type')
        data = User.objects.filter(email = request.POST.get('email'))
        if not data:
            user, created = User.objects.get_or_create(email=email, password=password, first_name=first_name, last_name=last_name, mobile=mobile, user_type=user_type)
            user.set_password(user.password)
            user.save()
            messages.success(request, "You have Successfully Registerd!")
            return redirect('tables')
        else:
            messages.error(request, "This email address is already exists!")
    return render(request, template_name,{'roll':USER_TYPE })

def userView(request, id):
    template_name = 'user-view.html'
    user = User.objects.get(id=id)
    return render(request, template_name, {'user': user})

def userUpdate(request, id):
    template_name = 'user-edit.html'
    if request.method=="POST":
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        mobile = request.POST.get('mobile')
        user = User.objects.filter(id=id, user_type='USER')
        if user:
            user.update(first_name=first_name, last_name=last_name, mobile=mobile)
            messages.success(request, "User updated!")
            return redirect('tables')
        else:
            messages.error(request, "Something went wrong!")
            return redirect('user_edit')
    else:
        user = User.objects.get(id=id)
        return render(request, template_name, {'user': user})

def userDelete(request, id):
    user = User.objects.get(id=id)
    user.delete()
    messages.success(request, "User is deleted!")
    return redirect('tables')

def vendor(request):
    template_name = 'vendors.html'
    vendor = User.objects.filter(user_type='VENDOR')
    return render(request, template_name, {'vendor': vendor})

def vendorView(request, id):
    template_name = 'vendor-view.html'
    vendor = User.objects.get(id=id)
    return render(request, template_name, {'vendor': vendor})

def addVendor(request):
    template_name = 'add-vendor.html'
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        mobile = request.POST.get('mobile')
        user_type = request.POST.get('user_type')
        data = User.objects.filter(email = request.POST.get('email'))
        if not data:
            user, created = User.objects.get_or_create(email=email, password=password, first_name=first_name, last_name=last_name, mobile=mobile, user_type=user_type)
            user.set_password(user.password)
            user.save()
            messages.success(request, "You have Successfully Registerd!")
            return redirect('vendors')
        else:
            messages.error(request, "This email address is already exists!")
    return render(request, template_name,{'roll':USER_TYPE })


def vendorUpdate(request, id):
    template_name = 'vendor-edit.html'
    if request.method=="POST":
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        mobile = request.POST.get('mobile')
        vendor = User.objects.filter(id=id, user_type='VENDOR')
        if vendor:
            vendor.update(first_name=first_name, last_name=last_name, mobile=mobile)
            messages.success(request, "User updated!")
            return redirect('vendors')
        else:
            messages.error(request, "Something went wrong!")
            return redirect('vendor_edit')
    else:
        vendor = User.objects.get(id=id)
        return render(request, template_name, {'vendor': vendor})


def vendorDelete(request, id):
    user = User.objects.get(id=id)
    user.delete()
    messages.success(request, "Vendor is deleted")
    return redirect('vendors')

def goalList(request):
    template_name = 'goal.html'
    goal = Goal.objects.all()
    return render(request, template_name, {'data': goal})

def goalView(request, id):
    template_name = 'goal-view.html'
    goal = Goal.objects.get(id=id)
    return render(request, template_name, {'data': goal})

def socialList(request):
    template_name = 'social.html'
    social = SocialIcon.objects.all()
    return render(request, template_name, {'social': social})

def addSocialLink(request):
    template_name = 'add-social.html'
    if request.method == 'POST':
        name = request.POST.get('name')
        icon = request.POST.get('icon')
        link = request.POST.get('link')
        social, created = SocialIcon.objects.get_or_create(name=name, icon=icon, link=link)
        social.save()
        messages.success(request, "You have Successfully Add Link!")
        return redirect('social')
    return render(request, template_name)


def register(request):
    template_name = 'register.html'
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        mobile = request.POST.get('mobile')
        data = Customer.objects.filter(email = request.POST.get('email'))
        if data:
            messages.error(request, "This email address is already exists!")
        else:
            user, created = Customer.objects.get_or_create(email=email, password=password, first_name=first_name, last_name=last_name, mobile=mobile)
            user.save()
            messages.success(request, "You have Successfully Registerd!")
    return render(request, template_name)

def logout(request):
    auth.logout(request)
    return redirect('/admin/login/')

def registerUser(request):
    template_name = 'user-register.html'
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        mobile = request.POST.get('mobile')
        user_type = request.POST.get('user_type')
        data = User.objects.filter(email = request.POST.get('email'))
        if not data:
            user, created = User.objects.get_or_create(email=email, password=password, first_name=first_name, last_name=last_name, mobile=mobile, user_type=user_type)
            user.set_password(user.password)
            user.save()
            sendOTP(user)
            print(user.slug, 'ssssssssdfffffffffffffffff')
            messages.success(request, "You have Successfully Registerd!")
            return redirect('/admin/verify/'+str(user.slug)+'/')
        else:
            messages.error(request, "This email address is already exists!")
    return render(request, template_name,{'roll':USER_TYPE})



def verifyUser(request, slug):
    template_name = 'verify-otp.html'
    if request.method == 'POST':
        otp = request.POST.get('otp')
        user = User.objects.get(slug=slug)
        if user.otp == otp:
            print(user.otp, 'pppppppppp')
            user.is_verified = True
            user.save()
            messages.success(request, 'Email Verification Complete.')
            return redirect('dashboard')
        else:
            messages.error(request, 'OTP does not match!')
    else:
        messages.error(request, 'Something Went wrong!')
    return render(request, template_name)

def pendingUser(request):
    template_name = 'pending-users.html'
    pending = User.objects.filter(is_active=False)
    return render(request, template_name, {'pending': pending})

def approveUser(request):
    template_name = 'approve-users.html'
    approve = User.objects.filter(is_active=True, is_verified=True)
    return render(request, template_name, {'approve': approve})


