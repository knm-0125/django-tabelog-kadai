from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth import login
from .models import Shop, Review, Category, Favorite

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
            login(request, user)
            return redirect('top')
        else:
            return render(request, 'nagoyameshi/login.html',{
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
        password = request.POST.get('password')

        user = User.objects.create_user(
            username=username,
            password=password
        )

        login(request, user)
        return redirect('top')

    return render(request, 'nagoyameshi/register.html')

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