from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from .models  import *
# Create your views here.
def StudentReg (request):
    if request.method == 'POST':

        obj = app1_Student()
        obj1 = Logindata()

        a = request.POST['T1']
        b = request.POST['T2']
        c = request.POST['T3']
        d = request.POST['T4']
        e = 'student'

        obj.name = a
        obj.branch = b
        obj.email = c

        obj1.email = c
        obj1.password = d
        obj1.usertype = e

        obj.save()
        obj1.save()
        return render(request, 'StudentReg.html', {'data': "success"})
    else:
        return render(request, 'StudentReg.html')

def showstudent(request):
    students = app1_Student.objects.all()
    return render(request, 'showstudent.html', {'students': students})

def deletestudent(request, id):
    student = app1_Student.objects.get(id=id)
    student.delete()
    return redirect('showstudent')

def updatestudent(request, id):
    student = app1_Student.objects.get(id=id)
    if request.method == 'POST':
        student.name = request.POST['T1']
        student.branch = request.POST['T2']
        student.email = request.POST['T3']
        student.save()
        return redirect('showstudent')
    return render(request, 'updatestudent.html', {'student': student})

def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            user = Logindata.objects.get(email=email, password=password)
            # Store user info in session
            request.session['user_email'] = user.email
            request.session['user_type'] = user.usertype
            request.session['user_id'] = user.id

            messages.success(request, f'Welcome {user.email}!')
            return redirect('dashboard')
        except Logindata.DoesNotExist:
            messages.error(request, 'Invalid email or password')
            return render(request, 'login.html')

    return render(request, 'login.html')

def logout(request):
    # Clear session
    request.session.flush()
    messages.success(request, 'You have been logged out successfully')
    return redirect('login')

@login_required(login_url='login')
def dashboard(request):
    user_email = request.session.get('user_email')
    user_type = request.session.get('user_type')

    if not user_email:
        return redirect('login')

    # Get user data
    user = Logindata.objects.get(email=user_email)

    # Get dashboard data based on user type
    context = {
        'user': user,
        'user_type': user_type,
    }

    if user_type == 'student':
        # For students, show their own data
        try:
            student = app1_Student.objects.get(email=user_email)
            context['student'] = student
        except app1_Student.DoesNotExist:
            context['student'] = None
        return render(request, 'dashboard.html', context)
    else:
        # For admin, show all students
        students = app1_Student.objects.all()
        context['students'] = students
        context['total_students'] = students.count()
        return render(request, 'dashboard.html', context)
