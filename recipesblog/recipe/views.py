from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Recipes  # Import the Recipes model
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate , login , logout
from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required(login_url='/login/')
def recipes(request):
    if request.method == "POST":
        data = request.POST 
        recipe_name = data.get('recipe_name')
        recipe_desc= data.get('recipe_desc')
        recipe_image = request.FILES.get('recipe_image')
        
        Recipes.objects.create(
            recipe_name=recipe_name,
            recipe_desc=recipe_desc,
            recipe_image=recipe_image,
        )
        return redirect('/recipes/')
        
    queryset= Recipes.objects.all()

    if request.GET.get('search'):
        queryset = queryset.filter(recipe_name__icontains = request.GET.get('search'))
        
    context= {'recipes':queryset}
    return render(request, 'pages/recipes.html',context)

def update_recipes(request,id):
    queryset = Recipes.objects.get(id=id)

    if request.method == "POST":
        data = request.POST 
        recipe_name = data.get('recipe_name')
        recipe_desc= data.get('recipe_desc')
        recipe_image = request.FILES.get('recipe_image')

        queryset.recipe_name = recipe_name
        queryset.recipe_desc = recipe_desc

        if recipe_image:
            queryset.recipe_image = recipe_image

        queryset.save()    
        return redirect('/recipes/')

    context= {'recipe':queryset}
    return render(request, 'pages/update_recipes.html',context)    

def delete_recipes(request,id):
    queryset = Recipes.objects.get(id=id)
    queryset.delete()
    return redirect('/recipes/')

def login_page(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        if not User.objects.filter(username = username). exists():
            messages.error(request,'Invalid username')
            return redirect('/login/')

        user = authenticate(username = username, password = password)

        if user is None:
            messages.error(request,'Invalid Password')
            return redirect('/login/')
        else:
            login(request,user)
            return redirect('/recipes/')
    return render(request,'pages/login.html')            
        
        
def logout_page(request):
    logout(request)
    return redirect('/login/') 
    
def register_page(request):
     if request.method == "POST":
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = User.objects.filter(username=username)

        if user.exists():
            messages.info(request,'Username already taken')
            return redirect('/register/')
      

        user=User.objects.create(
            first_name = first_name,
            last_name = last_name,
            username=username
        )
        user.set_password(password )
        user.save()
        
        messages.info(request,'Account created succesfully')
        return redirect('/login/')

     return render(request, 'pages/register.html')
