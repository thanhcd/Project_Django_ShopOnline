from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import SignUpForm, ItemsForm  
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import Items
from django.conf import settings
from django.core.files.storage import FileSystemStorage
import os

# Create your views here.
def home(request):
    items = Items.objects.all()
    context = {'items' :items}
    return render(request, 'home.html', context)


@login_required(login_url='login')
def createItems(request):
    form = ItemsForm()

    if request.method == 'POST':
        form = ItemsForm(request.POST)
        if form.is_valid():
            item = form.save(commit=False)
            item.host = request.user
            item.save()
            return redirect('home')  # Đảm bảo rằng tên 'home' được sử dụng chính xác
    context = {'form': form}
    return render(request, 'shop/item.html', context)



@login_required(login_url='login')
def update_item(request, pk):
    item = Items.objects.get(id=pk)
    if request.user != item.host:
        return HttpResponse('you are not allow here!!')

    if request.method == 'POST':
        form = ItemsForm(request.POST, request.FILES, instance=item)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = ItemsForm(instance=item)
    return render(request, 'shop/update_item.html', {'form': form, 'item': item})


@login_required(login_url='login')
def delete_item(request, pk):
    item = Items.objects.get(id=pk) 

    # Kiểm tra xem người dùng có phải là người tạo mục không
    if request.user != item.host:
        return HttpResponse('you are not allow here!!')

    if request.method == 'POST':
        # Xác nhận xóa mục
        item.delete()
        return redirect('home')
    return render(request, 'shop/delete_item.html', {'obj':item})

def view_item(request, pk):
    item = Items.objects.get(id=pk)
    return render(request, 'shop/view_item.html', {'item': item})


def indexPage(request):
    return render(request, 'shop/index.html')

def shopPage(request):
    return render(request, 'shop/shop.html')


def registerPage(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login') # Chuyển hướng đến trang thông báo đăng ký thành công
    else:
        form = SignUpForm() 
    return render(request, 'shop/register.html', {'form': form})  # Truyền form vào template


def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # Đăng nhập thành công, chuyển hướng đến trang chính hoặc trang mà bạn muốn
            return redirect('home')
        else:
            # Đăng nhập không thành công, hiển thị lại trang đăng nhập với thông báo lỗi
            context = {'error_message': 'Invalid username or password'}
            return render(request, 'shop/login.html', context)
    else:
        # Nếu không phải là POST request, hiển thị trang đăng nhập
        return render(request, 'shop/login.html')
    

def logoutUser(request):
    logout(request)
    return redirect('login')  # Chuyển hướng người dùng đến trang chính sau khi đăng xuất