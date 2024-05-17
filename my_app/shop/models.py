from django.db import models


# class User(models.Model):
#     name = models.CharField(max_length=100)
#     age = models.IntegerField()

#     def __str__(self):
#         return self.name
    


# class Product(models.Model):
#     id = models.AutoField(primary_key=True)  # Tự động tạo id
#     name = models.CharField(max_length=100)  # Tên sản phẩm
#     price = models.DecimalField(max_digits=10, decimal_places=2)  # Giá bán
#     quantity = models.IntegerField()  # Số lượng

#     def __str__(self):
#         return self.name