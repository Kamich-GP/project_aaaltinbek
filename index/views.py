from django.shortcuts import render, redirect
from .models import Category, Product, Cart
from django.contrib.auth.models import User
from django.contrib.auth import login, logout
from .forms import RegForm
from django.views import View
import telebot

bot = telebot.TeleBot('TOKEN')
admin_id = 'ADMIN_ID'

# Create your views here.
def home_page(request):
    # Достаем данные из БД
    categories = Category.objects.all()
    products = Product.objects.all()
    # Передаем данные на Frontend
    context = {"categories": categories, "products": products}
    return render(request, 'home.html', context)

def category_page(request, pk):
    # Достаем данные из БД
    category = Category.objects.get(id=pk)
    products = Product.objects.filter(product_category=category)
    # Передаем данные на Frontend
    context = {"category": category, "products": products}
    return render(request, 'category.html', context)

def product_page(request, pk):
    # Достаем данные из БД
    product = Product.objects.get(id=pk)
    # Передаем данные на Frontend
    context = {"product": product}
    return render(request, 'product.html', context)

class Register(View):
    template_name = 'registration/register.html'

    def get(self, request):
        form = RegForm
        context = {"form": form}
        return render(request, self.template_name, context)

    def post(self, request):
        form = RegForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password1')

            user = User.objects.create_user(username=username,
                                            email=email,
                                            password=password)
            user.save()
            login(request, user)
            return redirect('/')

def search(request):
    if request.method == 'POST':
        searched_product = request.POST.get('search_product')
        product = Product.objects.filter(product_name__iregex=searched_product)
        context = {}
        if product:
            context.update(user_pr=searched_product, products=product)
        else:
            context.update(user_pr=searched_product, products='')
        return render(request, 'result.html', context)

def logout_view(request):
    logout(request)
    return redirect('/')

def add_to_cart(request, pk):
    if request.method == 'POST':
        product = Product.objects.get(id=pk)
        user_amount = int(request.POST.get('pr_amount'))
        if 1 <= user_amount <= product.product_count:
            Cart.objects.create(user_id=request.user.id,
                                user_product=product,
                                user_pr_amount=user_amount).save()
            return redirect('/')
    return redirect(f'/product/{pk}')

def del_from_cart(request, pk):
    Cart.objects.filter(user_product=Product.objects.get(id=pk)).delete()
    return redirect('/cart')

def cart_page(request):
    user_cart = Cart.objects.filter(user_id=request.user.id)
    totals = [round(t.user_pr_amount * t.user_product.product_price, 2) for t in user_cart]
    context = {}
    if user_cart:
        context.update(cart=user_cart, total=round(sum(totals), 2))
    else:
        context.update(cart="", total=0)
    if request.method == 'POST':
        text = f'Новый заказ!\nКлиент: {User.objects.get(id=request.user.id).email}\n\n'
        new_totals = []
        for i in user_cart:
            product = Product.objects.get(id=i.user_product.id)
            user_amount = int(request.POST.get(f'amount_{product.id}'))
            product.product_count = product.product_count - user_amount
            product.save(update_fields=['product_count'])
            new_totals.append(round(product.product_price * user_amount, 2))
            text += f'Товар: {product}\nКоличество: {user_amount}\n'
        text += f'Итого: ${round(sum(new_totals, 2))}'
        bot.send_message(admin_id, text)
        user_cart.delete()
        return redirect('/')
    return render(request, 'cart.html', context)
