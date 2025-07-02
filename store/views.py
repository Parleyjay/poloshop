from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Product, Category, Cart, CartItem, ShippingAddress, Customer
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User

from .forms import ProductForm, CategoryForm

# FOR DISPLAYING THE PRODUCTS ON THE HOME PAGE
def home(request):
    products = Product.objects.all()
    context = {'products': products}
    return render(request, 'home.html', context)

# CATEGORY FUNCTIONS

def create_category(request):
    if not request.user.is_authenticated:
        messages.error(request, 'You must be logged in to create a category.')
        return redirect('login')

    if not (request.user.is_superuser or (hasattr(request.user, 'customer') and request.user.customer.user_type == 'seller')):
        messages.error(request, 'You must be a seller to create a category.')
        return redirect('home')

    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('all_category')
    else:
        form = CategoryForm()

    context = {'form': form}
    return render(request, 'create_category.html', context)

def edit_category(request, id):
    if not request.user.is_authenticated:
        messages.error(request, 'You must be logged in to edit a category.')
        return redirect('login')

    category = Category.objects.get(id=id)

    if not (request.user.is_superuser or category.creator == request.user):
        messages.error(request, 'You are not authorized to edit this category.')
        return redirect('all_category')

    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            return redirect('all_category')
    else:
        form = CategoryForm(instance=category)

    context = {'category': category, 'form': form}
    return render(request, 'edit_category.html', context)

def all_category(request):
    categories = Category.objects.all()
    context = {'categories': categories}
    return render(request, 'all_category.html', context)

def category_context(request):
    return {'categories': Category.objects.all()}

def category_detail(request, id):
    category = Category.objects.get(id=id)
    products = category.products.all()
    context = {'category': category, 'products': products}
    return render(request, 'category_detail.html', context)

def delete_category(request, id):
    category = Category.objects.get(id=id)
    if not (request.user.is_superuser or category.creator == request.user):
        messages.error(request, 'You are not authorized to edit this category.')
        return redirect('all_category')

    if request.method == 'POST':
        category.delete()
        return redirect('all_category')

    context = {'category': category}
    return render(request, 'edit_category.html', context)

# PRODUCT FUNCTIONS

def create_product(request):
    if not (request.user.is_superuser or (hasattr(request.user, 'customer') and request.user.customer.user_type == 'seller')):
        messages.error(request, 'You must be a seller to create a product.')
        return redirect('home')

    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = ProductForm()

    context = {'form': form}
    return render(request, 'create_product.html', context)

def product_detail(request, id):
    product = Product.objects.get(id=id)
    context = {'product': product}
    return render(request, 'product_detail.html', context)

def edit_product(request, id):
    product = Product.objects.get(id=id)
    if not (request.user.is_superuser or product.creator == request.user):
        messages.error(request, 'You are not authorized to edit this product.')
        return redirect('home')

    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            return redirect('product_detail', id=product.id)
    else:
        form = ProductForm(instance=product)

    context = {'product': product, 'form': form}
    return render(request, 'edit_product.html', context)

def delete_product(request, id):
    product = Product.objects.get(id=id)
    if not (request.user.is_superuser or product.creator == request.user):
        messages.error(request, 'You are not authorized to delete this product.')
        return redirect('home')

    if request.method == 'POST':
        product.delete()
        return redirect('home')

    context = {'product': product}
    return render(request, 'edit_product.html', context)

# CART FUNCTIONS

def cart(request):
    if not request.user.is_authenticated:
        messages.error(request, 'You must be logged in to view the cart.')
        return redirect('login')

    customer = getattr(request.user, 'customer', None)
    if customer:
        cart = Cart.objects.filter(customer=customer, complete=False).first()
        if not cart:
            cart = Cart.objects.create(customer=customer, complete=False)
        items = CartItem.objects.select_related('product').filter(cart=cart)
    else:
        messages.error(request, 'Please login.')
        return redirect('login')

    context = {'cart': cart, 'items': items}
    return render(request, 'cart.html', context)

def add_to_cart(request, id):
    customer = getattr(request.user, 'customer', None)
    if not customer:
        messages.error(request, 'You must be logged in as a customer.')
        return redirect('login')

    cart = Cart.objects.filter(customer=customer, complete=False).first()
    if not cart:
        cart = Cart.objects.create(customer=customer, complete=False)

    product = get_object_or_404(Product, id=id)
    item = CartItem.objects.filter(cart=cart, product=product).first()

    if item:
        item.quantity += 1
        item.save()
    else:
        CartItem.objects.create(cart=cart, product=product, quantity=1)

    return redirect('home')

def remove_from_cart(request, id):
    customer = getattr(request.user, 'customer', None)
    if not customer:
        messages.error(request, 'You must be logged in as a customer.')
        return redirect('login')

    cart = Cart.objects.filter(customer=customer, complete=False).first()
    if not cart:
        messages.warning(request, 'No active cart found.')
        return redirect('cart')

    product = get_object_or_404(Product, id=id)
    item = CartItem.objects.filter(cart=cart, product=product).first()

    if item:
        if item.quantity > 1:
            item.quantity -= 1
            item.save()
        else:
            item.delete()
    else:
        messages.info(request, 'Item not found in cart.')

    return redirect('cart')

def increase_quantity(request, id):
    cart, created = Cart.objects.get_or_create(customer=request.user.customer, complete=False)
    product = get_object_or_404(Product, id=id)
    item = CartItem.objects.filter(cart=cart, product=product).first()

    if item:
        item.quantity += 1
        item.save()

    return redirect('cart')

def checkout(request):
    if not request.user.is_authenticated:
        messages.error(request, 'You must be logged in to view the cart.')
        return redirect('login')

    customer = getattr(request.user, 'customer', None)
    if customer:
        cart = Cart.objects.filter(customer=customer, complete=False).first()
        if not cart:
            cart = Cart.objects.create(customer=customer, complete=False)
        items = CartItem.objects.select_related('product').filter(cart=cart)
        shipping_address = ShippingAddress.objects.filter(customer=request.user, cart=cart).first()
    else:
        messages.error(request, 'Please login.')
        return redirect('login')

    context = {'cart': cart, 'items': items, 'shipping_address': shipping_address}
    return render(request, 'checkout.html', context)

def shipping_address(request):
    if not request.user.is_authenticated:
        messages.error(request, 'You must be logged in.')
        return redirect('login')

    customer = getattr(request.user, 'customer', None)
    if not customer:
        messages.error(request, 'Customer profile not found.')
        return redirect('login')

    cart = Cart.objects.filter(customer=customer, complete=False).first()
    if not cart:
        messages.error(request, 'No active cart found.')
        return redirect('cart')

    if request.method == 'POST':
        address = request.POST.get('address', '').strip()
        city = request.POST.get('city', '').strip()
        region = request.POST.get('region', '').strip()
        phone = request.POST.get('phone', '').strip()

        if not all([address, city, region, phone]):
            messages.error(request, 'All fields are required.')
            return redirect('shipping_address')

        ShippingAddress.objects.update_or_create(
            customer=request.user,
            cart=cart,
            defaults={
                'address': address,
                'city': city,
                'region': region,
                'phone': phone
            }
        )

        messages.success(request, 'Shipping address saved successfully.')
        return redirect('checkout')

    return render(request, 'shipping_address.html')

# USER FUNCTIONS

def all_customer(request):
    if not request.user.is_superuser:
        messages.error(request, 'You are not authorized to view this page.')
        return redirect('home')

    customers = Customer.objects.all()
    context = {'customers': customers}
    return render(request, 'all_customer.html', context)

def customer_detail(request, id):
    if not request.user.is_superuser:
        messages.error(request, 'You are not authorized to view this page.')
        return redirect('home')

    customer = Customer.objects.get(id=id)
    context = {'customer': customer}
    return render(request, 'customer_detail.html', context)

def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if password != confirm_password:
            messages.error(request, 'Passwords do not match!')
            return redirect('register')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists')
            return redirect('register')

        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already registered')
            return redirect('register')

        if '@' not in email or '.' not in email:
            messages.error(request, 'Invalid email address')
            return redirect('register')

        user = User.objects.create_user(username=username, email=email, password=password)
        customer = Customer.objects.create(user=user, name=username, email=email)

        return redirect('login')

    return render(request, 'register.html')

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Invalid username or password')
            return redirect('login')

    return render(request, 'login.html')

def user_logout(request):
    logout(request)
    return redirect('home')
