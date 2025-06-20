from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import SignUpForm, AddRecordForm
from .models import Record

def home(request: HttpRequest) -> HttpResponse:
    records = Record.objects.all()

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username = username, password = password)
        if user is not None:
            login(request, user)
            messages.success(request, 'You Have Been Logged In!')
            return redirect('home')
        else:
            messages.success(request,
                             'There Was An Error Logging In, Please Try Again...')
            return redirect('home')

    # GETTING
    else: return render(request, 'home.html', {'records': records})

def logout_user(request: HttpRequest) -> HttpResponse:
    logout(request)
    messages.success(request, 'You have been Logged Out...')
    return redirect('home')

def register_user(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            # authenticate and login
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username = username, password = password)
            login(request, user)
            return redirect('home')
    else: 
        form = SignUpForm()
        return render(request, 'register.html', {'form': form})
    return render(request, 'register.html', {'form': form})

def customer_record(request: HttpRequest, pk: int) -> HttpResponse:
    if request.user.is_authenticated:
        # look up record
        customer_record = Record.objects.get(id = pk)
        return render(request, 'record.html',
                      {'customer_record': customer_record})
    else:
        messages.success(request, 'You Must Be Logged In to View That Page.')
        return redirect('home')

def delete_record(request: HttpRequest, pk: int) -> HttpResponse:
    if request.user.is_authenticated:
        deleted = Record.objects.get(id = pk)
        deleted.delete()
        messages.success(request, 'Record Got Deleted!')
        return redirect('home')
    else:
        messages.success(request,
                         'You Must Be Logged In to Delete Records. Also Fuck you.')
        return redirect('home')

def add_record(request: HttpRequest) -> HttpResponse:
    form = AddRecordForm(request.POST or None)
    if request.user.is_authenticated:
        if request.method == 'POST':
            if form.is_valid():
                add_record = form.save()
                messages.success(request, 'Record Added.')
                return redirect('home')
        return render(request, 'add_record.html', {'form': form})
    else:
        messages.success(request, 'You Must Be Logged In to Add Record.')
        return redirect('home')

def update_record(request: HttpRequest, pk: int) -> HttpResponse:
    if request.user.is_authenticated:
        current_record = Record.objects.get(id = pk)
        form = AddRecordForm(request.POST or None, instance = current_record)
        if form.is_valid():
            form.save()
            messages.success(request, 'Record Has Been Updated.')
            return redirect('home')
        return render(request, 'update_record.html', {'form': form})
    else:
        messages.success(request, 'You Must Be Logged In to Add Record.')
        return redirect('home')
