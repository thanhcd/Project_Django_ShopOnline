from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import SignUpForm, ItemsForm, UserProfileForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import Item, Topic, Message, Cart, CartItem , UserProfile
from django.conf import settings
from django.contrib.auth import authenticate, login 
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate, login
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator

# views.py
from django.shortcuts import render, redirect
from .models import Item, Topic, Message

def home(request):
    q = request.GET.get('q', '')

    if q:
        return redirect('shopPage') + f'?q={q}'

    items = Item.objects.all()
    topics = Topic.objects.all()
    context = {'items': items, 'topics': topics}
    return render(request, 'shop/home.html', context)

#view item
def item_details(request, pk):
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

def related_pro(request):
    items = Item.objects.all()

    context = {'items': items}
    return render(request, 'shop/related_pro.html', context)


@login_required(login_url='login')
def createItems(request):
    form = ItemsForm()

    if request.method == 'POST':
        form = ItemsForm(request.POST, request.FILES)
        if form.is_valid():
            item = form.save(commit=False)
            item.host = request.user
            item.save()
            return redirect('shop')
        else:
            print(form.errors)  # In lỗi form ra log để kiểm tra

    context = {'form': form}
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
            return redirect('shop')
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

    items = Item.objects.all().order_by('-created')[:4]

    context = {'item': item, 'item_messages': item_messages , 'items' :items}
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

def whyPage(request):
    return render(request, 'shop/why.html')

def testimonialPage(request):
    return render(request, 'shop/testimonial.html')

def contactPage(request):
    return render(request, 'shop/contact.html')


def shopPage(request):
    q = request.GET.get('q', '')
    items = Item.objects.all()

    if q:
        items = items.filter(topic__name__icontains=q)

    paginator = Paginator(items, 8)  # Chia danh sách sản phẩm thành các trang, mỗi trang có tối đa 8 sản phẩm
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)  # Lấy trang hiện tại từ query parameter 'page'

    topics = Topic.objects.all()
    context = {'page_obj': page_obj, 'topics': topics}
    return render(request, 'shop/shop.html', context)



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



def cc(request):
    return HttpResponse("co cai con cac")



@login_required(login_url='login')
def add_to_cart(request, pk):
    item = get_object_or_404(Item, id=pk)
    quantity = int(request.POST.get('quantity', 1))
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, item=item)
    
    if not created:
        cart_item.quantity += quantity
    else:
        cart_item.quantity = quantity
    cart_item.save()

    if request.headers.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
        return JsonResponse({'message': 'Item added to cart successfully!'})
    return redirect('cart_detail')


@login_required(login_url='login')
def cart_detail(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_items = cart.items.all()

    if request.method == 'POST':
        cart_item_id = request.POST.get('cart_item_id')
        quantity = request.POST.get('quantity')

        if 'quantity' in request.POST:
            try:
                cart_item = CartItem.objects.get(id=cart_item_id, cart=cart)
                cart_item.quantity = int(quantity)
                cart_item.save()
            except CartItem.DoesNotExist:
                # Handle the case where the cart item does not exist
                pass
        return redirect('cart_detail')

    total_price = sum(item.total_price for item in cart_items)

    context = {
        'cart': cart,
        'cart_items': cart_items,
        'total_price': total_price,
    }
    return render(request, 'shop/cart_detail.html', context)


@login_required(login_url='login')
def cart_deleteItem(request):
    if request.method == 'POST':
        cart_item_id = request.POST.get('cart_item_id')
        try:
            cart_item = CartItem.objects.get(id=cart_item_id, cart__user=request.user)
            cart_item.delete()
        except CartItem.DoesNotExist:
            # Handle the case where the item does not exist
            pass
        return redirect('cart_detail')
    else:
        return redirect('cart_detail')
    


def update_cart_item(request, pk):
    if request.method == 'POST':
        quantity = request.POST.get('quantity')
        print(f"Received quantity: {quantity} for CartItem ID: {pk}")
        
        if quantity and quantity.isdigit() and int(quantity) > 0:
            cart_item = get_object_or_404(CartItem, id=pk, cart__user=request.user)
            quantity = int(quantity)
            if quantity <= cart_item.item.quantity_available:
                cart_item.quantity = quantity
                cart_item.save()
                print(f"Updated CartItem {cart_item.id} to quantity {cart_item.quantity}")
            else:
                print(f"Invalid quantity {quantity} for CartItem {cart_item.id}")
        else:
            print(f"Invalid input quantity: {quantity}")
        
    return redirect('cart_detail')



@login_required(login_url='login')
def checkoutPage(request):
    cart = Cart.objects.get(user=request.user)
    cart_items = cart.items.all()
    subtotal = sum(item.total_price for item in cart_items)  # Tính tổng giá trị các mặt hàng trong giỏ hàng

    # shipping_form = ShippingAddressForm()
    # payment_form = PaymentForm()

    context = {
        'cart_items': cart_items,
        'subtotal': subtotal,
        # 'shipping_form': shipping_form,
        # 'payment_form': payment_form
    }

    return render(request, 'shop/checkout.html', context)


@login_required(login_url='login')
def user_info(request):
    user = request.user
    profile, created = UserProfile.objects.get_or_create(user=user)

    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            print('Thay đổi thành công')
            return redirect('user')
        else:
            print(form.errors)
    else:
        form = UserProfileForm(instance=profile)

    return render(request, 'shop/user.html', {'form': form})