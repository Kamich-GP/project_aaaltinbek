from django.shortcuts import render, redirect
from .models import Category, Product, Cart
from django.contrib.auth.models import User
from django.contrib.auth import login, logout
from .forms import RegForm
from django.views import View

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
