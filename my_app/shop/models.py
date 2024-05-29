from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from decimal import Decimal

class Topic(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name
    

class Item(models.Model):
    host = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    topic = models.ForeignKey(Topic, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=20, decimal_places=2)
    sale_price = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True)
    image = models.ImageField(upload_to='items/', null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    participants = models.ManyToManyField(User, related_name='participants', blank=True)
    quantity_available = models.PositiveIntegerField(default=0)  # Trường mới để quản lý số lượng
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return f"{self.name} - {self.host.username if self.host else 'No Host'}"
    


class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    body = models.TextField()
    updated = models.DateTimeField(auto_now=True)
    create = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-create']    
    
    def __str__(self):
        return self.body[0:50]


class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    created = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Cart of {self.user.username}"

    
class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name='items', on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    @property
    def total_price(self):
        if self.item.sale_price is not None:
            return self.item.sale_price * self.quantity
        else:
            return self.item.price * self.quantity

    def __str__(self):
        return f"{self.quantity} of {self.item.name}"


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    country = models.CharField(max_length=100, blank=True, null=True)
    first_name = models.CharField(max_length=50, blank=True, null=True)
    last_name = models.CharField(max_length=50, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    state = models.CharField(max_length=100, blank=True, null=True)
    postal_code = models.CharField(max_length=20, blank=True, null=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)

    def __str__(self):
        return f"Profile of {self.user.username}"


# class Order(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='orders')
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
#     total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
#     status = models.CharField(max_length=20, choices=[
#         ('pending', 'Pending'),
#         ('completed', 'Completed'),
#         ('canceled', 'Canceled')
#     ], default='pending')
    
#     def __str__(self):
#         return f"Order {self.id} by {self.user.username}"

#     def calculate_total_price(self):
#         total = Decimal(0)
#         for item in self.items.all():
#             total += item.total_price()
#         self.total_p
