from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import SignUpForm, AddRecordForm
from .models import Record


def home(request):
    records = Record.objects.all()
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "Добро пожаловать!")
            return redirect('home')
        else:
            messages.success(request, "Что то пошло не так!")
            return redirect('home')
    else:
        return render(request, 'home.html', {'records': records})


def logout_user(request):
    logout(request)
    messages.success(request, "До свидания!")
    return redirect('home')


def register_user(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(request, username=username, password=password)
            login(request, user)
            messages.success(request, "Вы успешно зарегистрировались!")
            return redirect('home')
    else:
        form = SignUpForm()
        return render(request, 'register.html', {'form': form})

    return render(request, 'register.html', {'form': form})


def customer_record(request, pk):
    if request.user.is_authenticated:
        customer_rec = Record.objects.get(id=pk)
        return render(request, 'record.html', {'customer_rec': customer_rec})
    else:
        messages.success(request, "Вы должны войти в систему!")
        return redirect('home')


def delete_record(request, pk):
    if request.user.is_authenticated:
        customer_rec = Record.objects.get(id=pk)
        customer_rec.delete()
        messages.success(request, "Запись удалена!")
        return redirect('home')
    else:
        messages.success(request, "Вы должны войти в систему!")
        return redirect('home')


def add_record(request):
    form = AddRecordForm(request.POST or None)
    if request.user.is_authenticated:
        if request.method == "POST":
            if form.is_valid():
                add_record = form.save()
                messages.success(request, "Record Added!")
                return redirect("home")
        return render(request, 'add_record.html', {"form": form})
    else:
        messages.success(request, "Войдите в систему!")
        return redirect("home")


def update_record(request, pk):
    if request.user.is_authenticated:
        current_record = Record.objects.get(id=pk)
        form = AddRecordForm(request.POST or None, instance=current_record)
        if form.is_valid():
            form.save()
            messages.success(request, "Record updated!")
            return redirect("home")
        return render(request, 'update_record.html', {'form': form})
    else:
        messages.success(request, "Войдите в систему!")
        return redirect("home")