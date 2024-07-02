from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views import View
from django.contrib import messages
from todo_app.models import *

class UsernameValidation(View):
    def post(self, request):
        res = { 'status' : 'invalid' }
        username = request.POST.get('username', None)
        if username:
            if User.objects.filter(username=username).exists():
                res['message'] = 'Username is aleady taken.'
                return JsonResponse(res)
            
            res['status'] = 'valid'
            res['message'] = 'Username is available.'
            return JsonResponse(res)
        
        res['message'] = 'Username is required.'
        return JsonResponse(res)
    

class EmailValidation(View):
    def post(seelf, request):
        res = { 'status' : 'invalid' }
        email = request.POST.get('email')
        if email:
            if User.objects.filter(email=email).exists():
                res['message'] = 'email is aleady taken.'
                return JsonResponse(res)
            
            res['status'] = 'valid'
            res['message'] = 'email is available.'
            return JsonResponse(res)
        
        res['message'] = 'Email address is required.'    
        return JsonResponse(res)

def signup_user(request):
    if request.method == 'POST':
        username = request.POST.get('username', None)
        email = request.POST.get('email', None)
        password = request.POST.get('password', None)
        profile_img = request.FILES.get('profile-img')
        if username and email and password:
            user = User.objects.create(username=username)
            user.email = email
            user.profile_img = profile_img if profile_img else 'profile_images/default_user.png'
            user.set_password(password)
            user.save()
            return redirect('login')
        
    # Reutrn response to signup.html
    return render(request, 'todo_app/signup.html')


def login_user(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        if request.method == 'POST':
            username = request.POST.get('username', None)
            password = request.POST.get('password', None)

            if username and password:
                user = authenticate(request, username=username, password=password)
                if user:
                    login(request, user)
                    messages.success(request, f'Welcome {user}, you are successfully Loged In.')
                    return redirect('home')
                else:
                    messages.error(request, 'Invaild Username and Password.')
                    return render(request, 'todo_app/login.html')
            
            messages.error(request,'Please enter the fields.')
            return render(request, 'todo_app/login.html')

        return render(request, 'todo_app/login.html')


@login_required(login_url = 'login')
def logout_user(request):
    logout(request)
    messages.success(request, 'Successfully!!! you are logout.')
    return redirect('login')


@login_required(login_url='login')
def home(request):
    username = request.user
    items_obj = TodoList.objects.filter(username=username)
    items_count = TodoList.objects.filter(username=username,is_completed=1).count()
    return render(request, 'todo_app/home.html', { 'items' : items_obj, 'items_count' : items_count  })
    

@login_required(login_url='login')
def add_item(request):
    if request.method == "POST":
        title = request.POST.get('title', None)
        description = request.POST.get('desc', None)
        is_completed = request.POST.get('is_completed', None)
        if title:
            item = TodoList.objects.create(username=request.user, title=title,  description=description, is_completed=True if is_completed == 'on' else False)
            item.save()
        return redirect('home')
    return render(request, 'todo_app/add_items.html')


@login_required(login_url='login')
def edit_item(request, id=None):
    if id:
        if request.method == "POST":
            title = request.POST.get('title', None)
            description = request.POST.get('desc', None)
            is_completed = request.POST.get('is_completed', None)
            if title:
                context = {
                    'title' : title,
                    'description' : description,
                    'is_completed' : True if is_completed == 'on' else False
                }
                item, created = TodoList.objects.update_or_create(id=id, defaults=context)
                item.save()
            return redirect('home')
        
        item_obj = TodoList.objects.get(id=id)
        return render(request, 'todo_app/edit_item.html', { 'item' : item_obj })


@login_required(login_url='login')
def delete_item(request, id=None):
    if request.method == "POST":
        if id:
            obj = TodoList.objects.get(id=id)
            obj.delete()
    return redirect('home')

@login_required(login_url='login')
def edit_profile(request):
    user_obj = User.objects.get(id=request.user.id)
    if request.method == 'POST':
        fullname = request.POST.get('fullname', None)
        username = request.POST.get('username', None)
        email = request.POST.get('email', None)
        profile_img = request.FILES.get('profile-img')
        if username and email:
            user_obj.username = username
            user_obj.email = email
            if profile_img:
                user_obj.profile_img = profile_img
            if fullname:
                user_obj.first_name = fullname
            user_obj.save()
        return redirect('home')

    return render(request, 'todo_app/edit_profile.html', { 'user' : user_obj })
