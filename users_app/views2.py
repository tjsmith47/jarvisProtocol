from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
from .models import User, Machine

def index(request):
    context = {
        'all_users':User.objects.all(),
    }
    return render(request, 'index.html', context)

def new(request):
    return render(request, 'login.html')

def create(request):
    request.session['first_name'] = request.POST['first_name'],
    request.session['last_name'] = request.POST['last_name'],
    request.session['email'] = request.POST['email'],
    request.session['age'] = request.POST['age'],
    request.session['admin'] = request.POST['admin'],
    print(f'CREATE: {request.POST}')
    if request.method == "GET":
        return redirect('/')
    errors = User.objects.update_validator(request.POST)
    if len(errors) > 0:
        for value in errors.values():
            messages.error(request, value)
        return redirect(f'/')
    else:
        new_user = User.objects.create(
            first_name = request.POST['first_name'],
            last_name = request.POST['last_name'],
            email = request.POST['email'],
            age = request.POST['age'],
            admin = request.POST['admin'],
        )
        new_user.save()
    return render(request, 'dashboard.html', new_user)

def authenticate(request):
    User.objects.create(
        first_name=request.POST['first_name'],
        last_name=request.POST['last_name'],
        email=request.POST['email'],
        age=request.POST['age']
        )
    return redirect('/')

# logged_user = Users.objects.get(id=request.session['user_id'])
# 
# <input type="text" name="first_name" value="{{user.id}}" aria-label="user_first_name">

def update(request, user):
    user = User.objects.get(id=request.session['user_id'])
    if request.method == "POST":
        return redirect('/edit')
    # create object
    if 'user_id' not in request.session:
        return redirect('/landing')
    #instance = get instance
    errors = User.objects.update_validator(request.POST)
    # if errors are present:
    if len(errors) > 0:
        for value in errors.values():
            messages.error(request, value)
        return redirect('/')
    # if errors not present.
    else:
        user = User.objects.get(id = id)
        user.first_name = request.POST['first_name'],
        user.last_name = request.POST['last_name'],
        user.email = request.POST['email'],
        user.age = request.POST['age'],
        user.admin = request.POST['admin'],
        user.save()
        return render(request, 'dashboard.html', user)

def dashboard(request, logged_user):
    context = {
        'all_machines': Machine.objects.all(),
    }
    logged_user = User.objects.get(id=request.session['user_id'])
    request.session['user_id']='new_user.id'
    return render(request, 'dashboard.html', context, logged_user)

def logout(request):
    request.session.flush()
    return redirect('/')

''' def login(request):
    user = User.objects.filter(email=request.POST['email'])
    if user:
    
        logged_user = user[0]
        password = request.POST['password']
        pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
        User.objects.create(email=request.POST['email'], password=pw_hash)
        if bcrypt.checkpw(request.POST['password'].encode(), logged_user.password.encode()):
            request.session['user_id'] = logged_user.id
            return redirect('/success')
    return redirect('/') '''