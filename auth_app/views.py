from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from register_app.models import School, Period, YearGroup
from auth_app.models import UserProfile
from datetime import date
from choices import YearGroupSystem, YearGroupLevel

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')  # Change to your desired view
        else:
            messages.error(request, 'Invalid username or password')
    return render(request, 'auth_app/login.html')

@login_required
def user_logout(request):
    logout(request)
    return redirect('login')


def user_signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        password_confirm = request.POST['password_confirm']
        
        if password == password_confirm:
            if User.objects.filter(username=username).exists():
                messages.error(request, 'Username already exists')
            else:
                user = User.objects.create_user(username=username, password=password)
                user.save()

                school = School.objects.create(
                    name=f"{username}'s School",
                    yeargroup_system= YearGroupSystem.CUSTOM)
                for level, label in YearGroupLevel.choices:
                    YearGroup.objects.create(
                        school=school,
                        level=level,
                        custom_name=label,
                    )

                Period.objects.create(
                    name=f"{date.today().year}", 
                    start_date = date(date.today().year, 1, 1),
                    end_date =  date(date.today().year, 12, 31),
                    current = True,
                    school = school,
                    )

                UserProfile.objects.create(user=user, school=school)
                login(request, user)
                return redirect('home')  # Change to your desired view
        else:
            messages.error(request, 'Passwords do not match')
    
    return render(request, 'auth_app/signup.html')

@login_required
def home(request):
    return render(request, 'auth_app/home.html', {'user': request.user})

