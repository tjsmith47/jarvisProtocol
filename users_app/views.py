#from typing import NewType
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import User, Machine
import bcrypt


def index(request):
    context = {
        'all_users':User.objects.all(),
    }
    return render(request, 'index.html', context)

def login(request):
    errors = User.objects.login_validator(request.POST)
    if len(errors) > 0:
        for value in errors.values():
            messages.error(request, value)
        return redirect(f'/')
    else:
        logged_user = User.objects.get(id=request.session['user_id'])
        request.session['user_id']=logged_user.id
        return redirect('/')

def register(request):
    print(f'CREATE: {request.POST}')
    if request.method == "GET":
        return redirect('/')
    errors = User.objects.update_validator(request.POST)
    if len(errors) > 0:
        for value in errors.values():
            messages.error(request, value)
        return redirect(f'/')
    else:
        password = request.POST['password']
        pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
        logged_user = User.objects.create(email=request.POST['email'], password=pw_hash)
        if bcrypt.checkpw(request.POST['password'].encode(), logged_user.password.encode()):
            request.session['user_id'] = logged_user.id
            return redirect('/dashboard')
        new_user = User.objects.create(
            first_name = request.POST['first_name'],
            last_name = request.POST['last_name'],
            email = request.POST['email'],
            password = request.POST['password'],
            admin = request.POST['admin'],
        )
        request.session['user_id']=new_user.id
    return render(request, 'dashboard.html', new_user)

def authenticate(request):
    User.objects.create(
        first_name=request.POST['first_name'],
        last_name=request.POST['last_name'],
        email=request.POST['email'],
        password=request.POST['password']
        )
    return redirect('/')

def dashboard(request, logged_user):
    context = {
        'all_machines': Machine.objects.all(),
    }
    logged_user = User.objects.get(id=request.session['user_id'])
    request.session['user_id']='new_user.id'
    return render(request, 'dashboard.html', context, logged_user)

def register(request):
    if request.method == "GET":
        #POST ---
        pass

def update(request, logged_user):
    logged_user = User.objects.get(id=request.session['user_id'])
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
        logged_user = User.objects.get(id = id)
        logged_user.first_name = request.POST['first_name'],
        logged_user.last_name = request.POST['last_name'],
        logged_user.email = request.POST['email'],
        logged_user.password = request.POST['password'],
        logged_user.admin = request.POST['admin'],
        logged_user.save()
        return render(request, 'dashboard.html', logged_user)

def logout(request):
    request.session.flush()
    return redirect('/')

''' def login(request):
    user = User.objects.filter(email=request.POST['email'])
    if user:
    validate_
        logged_user = user[0]
        password = request.POST['password']
        pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
        User.objects.create(email=request.POST['email'], password=pw_hash)
        if bcrypt.checkpw(request.POST['password'].encode(), logged_user.password.encode()):
            request.session['user_id'] = logged_user.id
            return redirect('/dashboard')
    return redirect('/') 
    

logged_user = Users.objects.get(id=request.session['user_id'])

<input type="text" name="first_name" value="{{user.id}}" aria-label="user_first_name"> 

    email = User.object.filter(email=request.POST['email'])
    if email:
        #ensure that email exists in DB
        logged_user = email[0]
        #ensure that the password provided belongs to the user
        if bcrypt.checkpw(request.POST['password'].encode(), logged_user.password.encode()):
            #log user in
            request.session['user_id']=user.id
            #if bcrypt.checkpw(request.POST['password'].encode(). logged_user.password.encode())
            return redirect('/dashboard')
    return redirect('/')


index
validate_login

create
update
register
login
logout
edit
update
destroy

'''