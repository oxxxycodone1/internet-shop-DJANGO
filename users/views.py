# views.py
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegisterForm
from django.contrib.auth.decorators import login_required
from main.models import CartItem

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, f'Аккаунт успешно создан!')
            return redirect('login')  # Перенаправление на страницу входа
    else:
        form = UserRegisterForm()
    return render(request, 'registration/register.html', {'form': form})

@login_required
def profile(request):
    # Предположим, что товары в корзине связаны с пользователем
    cart_items = CartItem.objects.filter(cart__user=request.user)

    return render(request, 'registration/profile.html', {
        'cart_items': cart_items,
    })