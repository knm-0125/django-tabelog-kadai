from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Shop(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=100)
    description = models.TextField()
    address = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_paid_member = models.BooleanField(default=False)
    postal_code = models.CharField(max_length=20, blank=True)
    address = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return self.user.username

class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE)
    score = models.IntegerField()
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
       return f"{self.user.username} - {self.shop.name}"

class Reservation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE)
    reserved_date = models.DateField()
    reserved_time = models.TimeField()
    number_of_people = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.shop.name}"

class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username}- {self.shop.name}"

    class Meta:
        unique_together = ('user', 'shop')