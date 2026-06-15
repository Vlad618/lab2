from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from .models import Mod, Category, Rating, NewsletterSubscription, Order, OrderItem
from .forms import RatingForm, NewsletterForm, UserRegistrationForm, PaymentForm


def get_common_context(request):
    return {
        "categories": Category.objects.all(),
        "newsletter_form": NewsletterForm(),
        "cart_count": len(request.session.get('cart', [])),
    }


def home(request):
    category_id = request.GET.get('category')
    mods = Mod.objects.all()

    if category_id:
        mods = mods.filter(category_id=category_id)

    context = get_common_context(request)
    context.update({
        "title": "Головна сторінка",
        "mods": mods,
    })

    return render(request, "main/home.html", context)


def mod_detail(request, mod_id):
    mod = get_object_or_404(Mod, id=mod_id)
    
    if request.method == 'POST' and 'score' in request.POST:
        if not request.user.is_authenticated:
            return redirect('login')
        form = RatingForm(request.POST)
        if form.is_valid():
            rating = form.save(commit=False)
            rating.mod = mod
            rating.save()
            return redirect('mod_detail', mod_id=mod.id)
    
    context = get_common_context(request)
    context.update({
        "title": mod.name,
        "mod": mod,
        "rating_form": RatingForm(),
    })
    return render(request, "main/mod_detail.html", context)


def category_detail(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    mods = Mod.objects.filter(category=category)
    
    context = get_common_context(request)
    context.update({
        "title": f"Категорія: {category.name}",
        "category": category,
        "mods": mods,
    })
    return render(request, "main/category_detail.html", context)


def add_to_cart(request, mod_id):
    cart = request.session.get('cart', [])
    if mod_id not in cart:
        cart.append(mod_id)
        request.session['cart'] = cart
    return redirect('view_cart')


def view_cart(request):
    cart_ids = request.session.get('cart', [])
    mods = Mod.objects.filter(id__in=cart_ids)
    total_price = sum(mod.price for mod in mods)
    
    context = get_common_context(request)
    context.update({
        "title": "Кошик",
        "mods": mods,
        "total_price": total_price,
    })
    return render(request, "main/cart.html", context)


def remove_from_cart(request, mod_id):
    cart = request.session.get('cart', [])
    if mod_id in cart:
        cart.remove(mod_id)
        request.session['cart'] = cart
    return redirect('view_cart')


@login_required
def checkout(request):
    cart_ids = request.session.get('cart', [])
    if not cart_ids:
        return redirect('home')
    
    mods = Mod.objects.filter(id__in=cart_ids)
    total_price = sum(mod.price for mod in mods)

    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            order = Order.objects.create(user=request.user, total_price=total_price, is_completed=True)
            for mod in mods:
                OrderItem.objects.create(order=order, mod=mod, price=mod.price)
            
            request.session['cart'] = []
            return redirect('profile')
    else:
        form = PaymentForm()
    
    context = get_common_context(request)
    context.update({
        "title": "Оформлення замовлення",
        "mods": mods,
        "total_price": total_price,
        "form": form,
    })
    return render(request, "main/checkout.html", context)


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserRegistrationForm()
    
    context = get_common_context(request)
    context.update({"form": form, "title": "Реєстрація"})
    return render(request, "main/auth/register.html", context)


@login_required
def profile(request):
    if request.user.is_staff:
        orders = Order.objects.all().order_by('-created_at')
    else:
        orders = Order.objects.filter(user=request.user).order_by('-created_at')
    
    context = get_common_context(request)
    context.update({
        "title": "Особистий кабінет",
        "orders": orders,
    })
    return render(request, "main/profile.html", context)


from django.core.mail import send_mail
from django.conf import settings
import random
import string
from django.contrib.auth.models import User
from .models import PasswordResetCode
from django.contrib.auth.forms import SetPasswordForm

def custom_password_reset(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        user = User.objects.filter(email=email).first()
        if user:
            code = ''.join(random.choices(string.digits, k=6))
            PasswordResetCode.objects.filter(user=user).delete()
            PasswordResetCode.objects.create(user=user, code=code)
            
            send_mail(
                'Код відновлення пароля',
                f'Ваш код для відновлення пароля: {code}\nКод дійсний протягом 15 хвилин.',
                settings.DEFAULT_FROM_EMAIL,
                [email],
                fail_silently=False,
            )
            request.session['reset_email'] = email
            return redirect('password_reset_verify')
    
    context = get_common_context(request)
    context.update({"title": "Відновлення пароля"})
    return render(request, "main/auth/password_reset_form.html", context)

def custom_password_reset_verify(request):
    email = request.session.get('reset_email')
    if not email:
        return redirect('password_reset')
    
    if request.method == 'POST':
        code = request.POST.get('code')
        user = User.objects.filter(email=email).first()
        reset_code = PasswordResetCode.objects.filter(user=user, code=code).first()
        
        if reset_code and reset_code.is_valid():
            request.session['code_verified'] = True
            return redirect('password_reset_confirm_custom')
        else:
            error = "Невірний або прострочений код."
            context = get_common_context(request)
            context.update({"title": "Введіть код", "error": error})
            return render(request, "main/auth/password_reset_verify.html", context)

    context = get_common_context(request)
    context.update({"title": "Введіть код"})
    return render(request, "main/auth/password_reset_verify.html", context)

def custom_password_reset_confirm(request):
    email = request.session.get('reset_email')
    verified = request.session.get('code_verified')
    if not email or not verified:
        return redirect('password_reset')
    
    user = User.objects.filter(email=email).first()
    if request.method == 'POST':
        form = SetPasswordForm(user, request.POST)
        if form.is_valid():
            form.save()
            PasswordResetCode.objects.filter(user=user).delete()
            del request.session['reset_email']
            del request.session['code_verified']
            return redirect('password_reset_complete_custom')
    else:
        form = SetPasswordForm(user)
    
    context = get_common_context(request)
    context.update({"title": "Новий пароль", "form": form})
    return render(request, "main/auth/password_reset_confirm.html", context)

def subscribe_newsletter(request):
    if request.method == 'POST':
        form = NewsletterForm(request.POST)
        if form.is_valid():
            form.save()
            # Можна додати повідомлення про успіх
    return redirect(request.META.get('HTTP_REFERER', 'home'))