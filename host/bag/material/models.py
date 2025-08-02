from django.db import models

# Create your models here.
class register(models.Model):
    name=models.CharField(max_length=30)
    email=models.EmailField(unique=True)
    number=models.IntegerField(unique=True)
    password=models.CharField(max_length=20)
class product_table(models.Model):
    name=models.CharField(max_length=30)
    price=models.IntegerField()
    quantity=models.CharField()
    image=models.ImageField()
class cart(models.Model):
    user_details=models.ForeignKey(register,on_delete=models.CASCADE)
    product_details=models.ForeignKey(product_table,on_delete=models.CASCADE)
    quantityes=models.IntegerField(default=1)
    totalprice=models.IntegerField()
class wishlist(models.Model):
    user_details=models.ForeignKey(register,on_delete=models.CASCADE)
    product_details=models.ForeignKey(product_table,on_delete=models.CASCADE)
class orders(models.Model):
    user_details = models.ForeignKey(register, on_delete=models.CASCADE)
    product_details = models.ForeignKey(product_table, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    amount = models.IntegerField()
    product_status = models.CharField(max_length=30, default='order placed')
    order_date = models.DateTimeField()
class PasswordReset(models.Model):
    user_details = models.ForeignKey(register,on_delete = models.CASCADE)
    token = models.CharField(max_length=255)
