from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import SignUpForm  
from django.contrib.auth import authenticate, login, logout


# Create your views here.
def home(request):
    return render(request, 'home.html')


def room(request):
    return HttpResponse('room.html')




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