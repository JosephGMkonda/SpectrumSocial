from urllib import request
from django.shortcuts import render, redirect
from django.views import View
from .models import User
import json
from django.http import JsonResponse
from validate_email import validate_email
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib import auth


# Create your views here.

class EmailValidation(View):
    def post(self,request):
        data = json.loads(request.body)
        email = data['email']

        if not validate_email(email):
            return JsonResponse({"email_error":"Email is not valid"},status=400)
        if User.objects.filter(email=email).exists():
            return JsonResponse({"email_error":"sorry email in use, choose another one"}, status=409)
        return JsonResponse({"email_valid":True})




class usernameValidationView(View):
    def post(self, request):
        data = json.loads(request.body)
        username = data["username"]

        if not str(username).isalnum():
            return JsonResponse({"username_error":"username should only contain alphanumeric characters"},status=400)
        if User.objects.filter(username=username).exists():
            return JsonResponse({"username_error":"sorry username in use, choose another one"}, status=409)
        return JsonResponse({"username":True})



class registrationView(View):
    def get(self, request):
        return render(request, 'authentication/registration.html')

    def post(self, request):

        email = request.POST['email']
        username = request.POST['username']
        password = request.POST['password']

        context = {
            'fieldValues': request.POST
        }

        if not User.objects.filter(username=username).exists():
            if not User.objects.filter(email=email).exists():
                if len(password) < 6:
                    messages.error(request,"The password is too short, atleast should have more than six character")
                    return render(request, 'authentication/registration.html',context)
                user = User.objects.create_user(email=email,username=username)
                user.set_password(password)
                user.save()
                messages.success(request,"Account created successfully")
                return render(request, 'authentication/registration.html')




        
        return render(request, 'authentication/registration.html')

class loginView(View):
    def get(self, request):
        return render(request,"authentication/login.html")

    def post(self,request):

        username = request.POST["username"]
        password = request.POST["password"]

        if username and password:
            user = auth.authenticate(username=username, password=password)

            if user:
                if user.is_active:
                    auth.login(request,user)
                    messages.success(request,"Welcome " + user.username+ " your now logged in")
                    return redirect("feeds")

            messages.success(request,"Invalid credentials, try again")
            return render(request,'authentication/login.html')

        messages.success(request,"please all fields")
        return render(request,"authentication/login.html")

class LogoutView(View):
    def post (self,request):
        auth.logout(request)
        messages.success(request,"you have been logged out")
        return redirect('login')
        



