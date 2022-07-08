from urllib import request
from django.shortcuts import render, redirect,get_object_or_404
from django.views import View
from .models import Profile
import json
from django.http import JsonResponse,HttpResponse
from validate_email import validate_email
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib import auth
from django.urls import resolve
from PostFeed.models import Posts,Follow 
from django.template import loader



# Create your views here.

def UserProfile(request, username):
    user = get_object_or_404(User, username=username)
    profile = Profile.objects.get(user=user)
    url_name = resolve(request.path).url_name

    if url_name == 'profile':
        posts = Posts.objects.filter(user=user).order_by('-posted')
    else:
        posts = profile.favorites.all()

    post_count = Posts.objects.filter(user=user).count()
    following_count = Follow.objects.filter(follower=user).count()
    followers_count = Follow.objects.filter(following=user).count()


    template = loader.get_template('Feed/profile.html')

    context = {
        'posts': posts,
        'profile': profile,
        'post_count':post_count,
        'following_count':following_count,
        'followers_count':followers_count,
    }

    return HttpResponse(template.render(context,request))



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
        



