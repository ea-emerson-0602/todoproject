from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import todo
# Create your views here.

@login_required
def home(request):
    if request.method=="POST":
        task=request.POST.get("task")
        new_todo=todo(user=request.user, todo_name=task)
        new_todo.save()
        
    all_todos=todo.objects.filter(user=request.user)
    context={
        'todos':all_todos,
    }
    return render(request, "todoapp/todo.html",context)

def register(request):
    if request.user.is_authenticated:
        return redirect('homepage')
    if request.method=="POST":
        username=request.POST.get("username")
        email=request.POST.get("email")
        password=request.POST.get("password")
        passwordconfirm=request.POST.get("passwordconfirm")
        print(passwordconfirm!=password)
        if len(password)<5:
            messages.error(request, "Password must be at least 5 characters")
            return redirect("register")
        if passwordconfirm!=password:
            messages.error(request, "Passwords do not match")
            return redirect('register')
        
        username_exists=User.objects.filter(username=username).order_by("username")
        if username_exists:
            messages.error(request, "Error, username already exists!")
            return redirect("register")
        
        email_exists=User.objects.filter(email=email,)
        if email_exists:
            messages.error(request, "Email already exists! Login in instead")
            return redirect("register")
        new_user = User.objects.create_user(username=username, email=email, password=password)
        new_user.save()
        messages.success(request, "User has been successfully created, login now")
        return redirect("login")
    return render(request, "todoapp/register.html", {})

def loginpage(request):
    
    if request.user.is_authenticated:
        return redirect('homepage')
    if request.method=="POST":
        username=request.POST.get("uname")
        password=request.POST.get("pass")
        
        validate_user=authenticate(username=username,password=password)
        
        if validate_user is not None:
            login(request, validate_user)
            return redirect("homepage")
        else:
            messages.error(request, "Wrong credentials, or user does not exist")
            return redirect("login")
        
    return render(request, "todoapp/login.html", {})

def logoutuser(request):
    logout(request)
    messages.success(request, "Logged out successfully")
    return redirect("login")

@login_required
def delete_task(request, name):
    get_todo=todo.objects.get(user=request.user, todo_name=name)
    get_todo.delete()
    return redirect("homepage")

@login_required
def update_task(request, name):
    get_todo=todo.objects.get(user=request.user, todo_name=name)
    get_todo.status=True
    get_todo.save()
    return redirect('homepage')