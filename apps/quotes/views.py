from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from .models import User, Quote
from django.db.models import Count
import bcrypt

#New User Registration Logic
def register(request):

    first_name = request.POST['first_name']
    last_name = request.POST['last_name']
    email = request.POST['email']
    birthday = request.POST['birthday']
    password = request.POST['password']
    confirm_password = request.POST['confirm_password']
    data = {
    "first_name": first_name,
    "last_name": last_name,
    "email": email,
    "birthday": birthday,
    "password": password,
    "confirm_password": confirm_password
    }
    user = User.objects.register(data)

    if user:
        for i in range(0,len(user)):
            messages.error(request, user[i])
            return redirect('/')
    else:
        hashed = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
        create = User.objects.create(first_name=first_name, last_name=last_name, birthday=birthday, email=email, password=hashed)
        current_user = User.objects.get(first_name=request.POST['first_name'])
        request.session['id'] = current_user.id
        return redirect('/quotes')

#Returning user login
def login(request):
    email = request.POST['email']
    password = request.POST['password'].encode()
    data = {"email": email, "password": password}

    user = User.objects.login(data)
    if user:
        for i in range(0,len(user)):
            messages.error(request, user[i])
            return redirect('/')

    else:
        current_user = User.objects.get(email=email)
        print current_user.first_name
        print current_user.id

        request.session['id'] = current_user.id
        return redirect('/quotes')

def index(request):
    return render(request, 'quotes/index.html')

def quotes(request):
    thisuser = User.objects.get(id=request.session['id'])
    quotes = Quote.objects.all().exclude(favorite__id=request.session['id'])
    favs = Quote.objects.filter(favorite__id=request.session['id'])
    context = {
    "thisuser": thisuser,
    "quotes": quotes,
    "favs": favs,
    }
    return render(request,'quotes/quotes.html', context)

def add_quote(request):
    thisuser = User.objects.get(id=request.session['id'])
    name = request.POST['name']
    content = request.POST['content']
    if len(name) < 3:
        messages.error(request, "Quoted by must be more than 3 characters")

    if len(content) < 10:
        messages.error(request, "Quote must be more than 10 characters")
    else:
        Quote.objects.create(name = name, content=content, user = thisuser)
    return redirect('/quotes')

def fav(request, id):
    thisuser = User.objects.get(id=request.session['id'])
    quote = Quote.objects.get(id=id)
    quote.favorite.add(thisuser)
    return redirect('/quotes')

def remove(request, id):
    thisuser = User.objects.get(id=request.session['id'])
    quotes = Quote.objects.get(id=id)
    quotes.favorite.remove(thisuser)
    return redirect('/quotes')

def user(request, id):
    thisuser = User.objects.get(id=id)
    user_quotes = Quote.objects.filter(user__id=id)
    context = {
    "thisuser": thisuser,
    "user_quotes": user_quotes,
    }
    return render(request, 'quotes/users.html', context)

def logout(request):
    request.session['id'] = ''
    return redirect('/')
