from django.urls import path
from . import views

urlpatterns = [
    path('', views.top, name='top'),
    path('shop/<int:shop_id>/', views.shop_detail, name='shop_detail'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('shop/<int:shop_id>/review/', views.review_create, name='review_create'),
    path('shop/<int:shop_id>/favorite/', views.add_favorite, name='add_favorite'),
    path('favorites/', views.favorite_list, name='favorite_list'),
    path('favorites/<int:favorite_id>/delete/', views.remove_favorite, name='remove_favorite'),
    path('register/', views.register_view, name='register'),
    path('shops/<int:shop_id>/reserve/', views.reservation_create, name='reservation_create'),
    path('reservations/', views.reservation_list, name='reservation_list'),
    path('reservations/<int:reservation_id>/cancel/', views.reservation_cancel, name='reservation_cancel'),
    path('verify-email/<uidb64>/<token>/', views.verify_email, name='verify_email'),
]