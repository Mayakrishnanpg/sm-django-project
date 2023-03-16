from django.shortcuts import render,redirect
from django .http import HttpResponse
from .forms import UserAddForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from .decorators import admin_only,unauthenticated_user,allowed_user
from product.models import ProductDetails

# Create your views here.
@admin_only
def Index(request):
    product=ProductDetails.objects.all()
    
    context = {
        "product":product
    }
    return render(request,"index.html",context)
@allowed_user
def AdminIndex(request):
    return render(request,"admin/adminhome.html")

@unauthenticated_user
    
def signin(request):
    if request.method =="POST":
        username = request.POST["uname"]
        password = request.POST["pswd"]
        user = authenticate(request,username=username,password = password)
        if user is not None:
            login(request,user)
            return redirect('Index')
        else:
            messages.info(request,"username or password is incorrect")
            return redirect('signin')  
    return render(request,"login.html")

@unauthenticated_user
def signup(request):
     form = UserAddForm()
     if request.method =="POST":
        form = UserAddForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("Username")
            email = form.cleaned_data.get("email")
            
            if User.objects.filter(username = username).exists():
                messages.info(request,"username already exists")
                return redirect('signup')
            
            if User.objects.filter(email = email).exists():
                messages.info(request,"email already exist")
                return redirect('signup')
            
            else:
                form.save()
                messages.success(request,"user created")
                return redirect('signin')
            
     context = {"form":form}
     return render(request,"register.html",context)
def SignOut(request):
    logout(request)
    return redirect('Index')

    
  