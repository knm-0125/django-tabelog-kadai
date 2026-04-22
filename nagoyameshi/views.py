from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.urls import reverse
from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth import login
from .models import Shop, Review, Category, Favorite, Reservation

def top(request):
    shops = Shop.objects.all()
    categories = Category.objects.all()

    keyword = request.GET.get('keyword')
    category_id = request.GET.get('category')

    if keyword:
        shops = shops.filter(name__icontains=keyword)

    if category_id:
        shops = shops.filter(category_id=category_id)

    sort = request.GET.get('sort')

    if sort == 'name_asc':
        shops = shops.order_by('name')
    elif sort == 'name_desc':
        shops = shops.order_by('-name')
    elif sort == 'new':
        shops = shops.order_by('-id')
    elif sort == 'old':
        shops = shops.order_by('id')

    context = {
        'shops': shops,
        'categories': categories,
    }
    return render(request, 'nagoyameshi/top.html', context)

def shop_detail(request, shop_id):
    shop = get_object_or_404(Shop, id=shop_id)
    reviews = Review.objects.filter(shop=shop)

    context = {
        'shop': shop,
        'reviews': reviews,
    }
    return render(request, 'nagoyameshi/shop_detail.html', context)

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect('top')
            else:
                return render(request, 'nagoyameshi/login.html', {
                    'error': 'メール認証が完了していません'
                })
        else:
            return render(request, 'nagoyameshi/login.html', {
                'error': 'ユーザー名またはパスワードが違います'
            })

    return render(request, 'nagoyameshi/login.html')

def logout_view(request):
    logout(request)
    return redirect('top')

@login_required
def review_create(request, shop_id):
    shop = get_object_or_404(Shop, id=shop_id)

    if request.method == 'POST':
        score = request.POST.get('score')
        comment = request.POST.get('comment')

        Review.objects.create(
            user=request.user,
            shop=shop,
            score=score,
            comment=comment
        )
        return redirect('shop_detail', shop_id=shop.id)

    return render(request, 'nagoyameshi/review_form.html', {'shop':shop})

@login_required
def reservation_create(request, shop_id):
    shop = get_object_or_404(Shop, id=shop_id)

    if request.method == 'POST':
        reserved_date = request.POST.get('reserved_date')
        reserved_time = request.POST.get('reserved_time')
        number_of_people = request.POST.get('number_of_people')

        Reservation.objects.create(
            user=request.user,
            shop=shop,
            reserved_date=reserved_date,
            reserved_time=reserved_time,
            number_of_people=number_of_people,
        )
        messages.success(request, "予約が完了しました！")

        return redirect('reservation_list')

    context = {
        'shop': shop
    }
    return render(request, 'nagoyameshi/reservation_form.html', context)

@login_required
def reservation_list(request):
    reservations = Reservation.objects.filter(user=request.user).order_by('-reserved_date', '-reserved_time')

    context = {
        'reservations' : reservations
    }
    return render(request, 'nagoyameshi/reservation_list.html', context)

@login_required
def reservation_cancel(request, reservation_id):
    reservation = get_object_or_404(Reservation, id=reservation_id, user=request.user)

    if request.method == 'POST':
        reservation.delete()
        return redirect('reservation_list')

    context = {
        'reservation' : reservation
    }
    return render(request, 'nagoyameshi/reservation_cancel.html', context)

@login_required
def add_favorite(request, shop_id):
    shop = get_object_or_404(Shop, id=shop_id)

    Favorite.objects.get_or_create(
        user=request.user,
        shop=shop
    )

    return redirect('shop_detail', shop_id=shop.id)

@login_required
def favorite_list(request):
    favorites = Favorite.objects.filter(user=request.user)

    context = {
        'favorites': favorites
    }

    return render(request, 'nagoyameshi/favorite_list.html', context)

@login_required
def remove_favorite(request, favorite_id):
    favorite =get_object_or_404(Favorite, id=favorite_id, user=request.user)
    favorite.delete()
    return redirect('favorite_list')

def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )
        user.is_active = False
        user.save()

        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)

        verify_url = request.build_absolute_uri(
            reverse('verify_email', kwargs={'uidb64': uid, 'token': token})
        )

        send_mail(
            subject='メール認証のご案内',
            message=f'以下のURLをクリックして認証を完了してください。\n{verify_url}',
            from_email=None,
            recipient_list=[email],
        )
        print(verify_url)

        return render(request, 'nagoyameshi/email_sent.html')

    return render(request, 'nagoyameshi/register.html')

def verify_email(request, uidb64, token):
    try:

        uid = force_str(urlsafe_base64_decode(uidb64))

        user = User.objects.get(pk=uid)

    except:

        user = None

    if user is not None and default_token_generator.check_token(user, token):

        user.is_active = True

        user.save()

        return render(request, 'nagoyameshi/email_verified.html')

    else:

        return render(request, 'nagoyameshi/email_invalid.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('top')
        else:
            return render(request, 'nagoyameshi/login.html', {
                'error': 'ユーザー名またはパスワードが違います'
            })
    return render(request, 'nagoyameshi/login.html')