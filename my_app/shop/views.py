from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import SignUpForm, ItemsForm  
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import Item, Topic, Message
from django.conf import settings
from django.contrib.auth import authenticate, login


from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate, login



# views.py
from django.shortcuts import render, redirect
from .models import Item, Topic, Message

def home(request):
    q = request.GET.get('q', '')
    items = Item.objects.all()

    if q:
        items = items.filter(topic__name__icontains=q)

    topics = Topic.objects.all()
    context = {'items': items, 'topics': topics}
    return render(request, 'shop/home.html', context)

# def item(request, pk):
#     item = Item.objects.get(id=pk)
#     item_messages = item.message_set.all()
#     participants = item.participants.all()

#     if request.method == 'POST':
#         message = Message.objects.create(
#             user=request.user,
#             item=item,
#             body=request.POST.get('body')
#         )
#         item.participants.add(request.user)
#         return redirect('view-item', pk=item.id)

#     context = {'item': item, 'item_messages': item_messages, 'participants': participants}
#     return render(request, 'shop/view_item.html', context)


def item(request, pk):
    item = Item.objects.get(id=pk)
    item_messages = item.message_set.all()

    if request.method == 'POST':
        message = Message.objects.create(
            user=request.user,
            item=item,
            body=request.POST.get('body')
        )
        item.participants.add(request.user)
        # Chuyển hướng người dùng về trang chi tiết của item
        return redirect('item', pk=item.id)

    context = {'item': item, 'item_messages': item_messages}
    return render(request, 'shop/view_item.html', context)




@login_required(login_url='login')
def createItems(request):
    form = ItemsForm()

    if request.method == 'POST':
        form = ItemsForm(request.POST)
        if form.is_valid():
            item = form.save(commit=False)
            item.host = request.user
            item.save()
            return redirect('home')
        
    context = {'form':form}
    return render(request, 'shop/item.html', context)


@login_required(login_url='login')
def update_item(request, pk):
    item = Item.objects.get(id=pk)
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
    item = Item.objects.get(id=pk) 

    # Kiểm tra xem người dùng có phải là người tạo mục không
    if request.user != item.host:
        return HttpResponse('you are not allow here!!')

    if request.method == 'POST':
        # Xác nhận xóa mục
        item.delete()
        return redirect('home')
    return render(request, 'shop/delete_item.html', {'obj':item})


def view_item(request, pk):
    item = Item.objects.get(id=pk)
    item_messages = item.message_set.all()

    context = {'item': item, 'item_messages': item_messages}
    return render(request, 'shop/view_item.html', context)


@login_required(login_url='login')
def deleteMessage(request, pk):
    message = Message.objects.get(id=pk)

    if request.user != message.user:
        return HttpResponse('You are not allowed here!')

    if request.method == 'POST':
        item_id = message.item.id  # Lấy ID của item trước khi xóa message
        message.delete()
        # Chuyển hướng trang về view_item của item đã xóa message
        return redirect('view-item', pk=item_id)
    
    return render(request, 'shop/delete.html', {'obj':message})


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
    

@api_view(['POST'])
def api_register(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            return Response({"message": "Registration successful"}, status=status.HTTP_201_CREATED)
        return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def api_login(request):
    if request.method == 'POST':
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return Response({"message": "Login successful"}, status=status.HTTP_200_OK)
        return Response({"message": "Invalid username or password"}, status=status.HTTP_401_UNAUTHORIZED)
def logoutUser(request):
    logout(request)
    return redirect('login')  # Chuyển hướng người dùng đến trang chính sau khi đăng xuất