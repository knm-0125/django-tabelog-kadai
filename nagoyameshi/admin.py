from django.contrib import admin
from .models import Shop, Category, Profile, Review, Reservation, Favorite

admin.site.register(Shop)
admin.site.register(Category)
admin.site.register(Profile)
admin.site.register(Review)
admin.site.register(Reservation)
admin.site.register(Favorite)