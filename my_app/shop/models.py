from django.db import models
from django.contrib.auth.models import User

class MyModel(models.Model):
    username = models.CharField(max_length=100)
    password = models.IntegerField()

    def __str__(self):
        return self.name
    

class Items(models.Model):
    host= models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=100)  # Tên của mặt hàng
    price = models.DecimalField(max_digits=10, decimal_places=2)  # Giá tiền của mặt hàng
    image = models.ImageField(upload_to='items/', null=True, blank=True)  # Hình ảnh của mặt hàng, có thể null
    description = models.TextField(null=True, blank=True)
    # updated = models.DateTimeField(auto_now=True)
    # create = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name