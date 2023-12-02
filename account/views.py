from django.shortcuts import render,get_object_or_404
from django.contrib import messages
from django.http import HttpResponse
from .forms import loginform,UserCreationForm
from .models import CustomUser
from django.contrib.auth import authenticate,login,logout

def user_login(request):
    if request.method=='POST':
        form=loginform(request.POST)
        
        if form.is_valid():
            cd=form.cleaned_data
            user=authenticate(request,email=cd['Email'],password=cd['Password'])
            if user is not None:
                login(request,user)
                messages.success(request,'Login  successful')
                context={ "action":True ,"type":"showlogin","value":"false"}
                res=render(request,'login-out-register.html',context)
                res['HX-Target']='#msgs'
                return res
                
            else:
                return HttpResponse('<p class="text-red-600"> Invalid Email or Password </p>')

           
        else:
            return HttpResponse(form)    

def user_logout(request):
    logout(request)
    messages.success(request,'Logout  successful')
    return render(request,'login-out-register.html')
    
def register(request):
    if request.method=="POST":
        form=UserCreationForm(request.POST)
        if form.is_valid():
            new_user=form.save()
            messages.success(request,'Login  successful')
            context={"action":True ,"type":"showregister","value":"false"}
            res=render(request,'login-out-register.html' ,context)
            res['HX-Target']='#msgs'
            return res     
             
        else:
            
            return render(request,'formerrors.html',{'form':form})   


def myaccount(request):

    return render(request,'account/account.html')

def editprofile(request):

    return render(request,'account/partials/editprofile.html')
    