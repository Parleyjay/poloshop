from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from datetime import datetime, date


from . import forms


# FOR DISPLAYING THE PRODUCTS ON THE HOME PAGE
# def home(request):
#     products = Product.objects.filter(product_status=1).order_by('-date_created')[:10]  # Display only active products
#
#
#     context = {
#                'products': products}
#     return render(request, 'home.html', context)


    
@login_required(login_url="login")
def account_detail(request):
    try:
        addresses = ShippingAddress.objects.filter(customer=request.user)
        # print(addresses)
        context = {
            
            "addresses": addresses,
        }
        return render(request, 'account_detail.html', context)
    except Exception as e:
        return render(request, 'error.html', {'error': str(e)})



    

# CATEGORY FUNCTIONS

@login_required(login_url="login") 
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

@login_required(login_url="login") 
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


@login_required(login_url="login") 
def category_context(request):
    return {'categories': Category.objects.all()}

 
def category_detail(request, id):
    category = Category.objects.get(id=id)
    products = category.products.all()
    context = {'category': category, 'products': products}
    return render(request, 'category_detail.html', context)

@login_required(login_url="login") 
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




#!!!!!!!!!!!!!!!!!!!! BRAND !!!!!!!!!!!!!!!!!!!
@login_required(login_url="login") 
def create_brand(request):
    if request.method == 'POST':
        form = BrandForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('create_product')
    
    else:
        form = BrandForm()

    context = {'form':form}
    return render(request, 'create_brand.html', context)



# PRODUCT FUNCTIONS
@login_required(login_url="login") 
def create_product(request):
    if not (request.user.is_superuser or (hasattr(request.user, 'customer') and request.user.customer.user_type == 'seller')):
        messages.error(request, 'You must be a seller to create a product.')
        return redirect('home')

    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            product = form.save(commit= False)
            product.creator = request.user
            product.save()
            messages.success(request, 'Product created successfully.')
            return redirect('home')
    else:
        form = ProductForm()
        

    context = {'form': form}
    return render(request, 'create_product.html', context)


def product_detail(request, id):
    product = Product.objects.get(id=id)
    reviews = Review.objects.filter(product=product).order_by('-created_date')
    context = {'product': product, 'reviews': reviews}
    return render(request, 'product_detail.html', context)

@login_required(login_url="login") 
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

@login_required(login_url="login") 
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




#INVENTORY FUNCTION
@login_required(login_url="login") 
def create_inventory(request):
    if request.method == 'POST':
        form = InventoryForm(request.POST)
        if form.is_valid():
            inventory = form.save(commit=False)
            inventory.creator = request.user
            inventory.save()
            messages.success(request, 'Inventory updated succesful')
            return redirect('home')
        
    else:
        form = InventoryForm(request.POST)
    
    context = {'form':form}
    return render(request, 'create_inventory.html', context)



# ADD SAVED PRODUCT
@login_required(login_url="login") 
def add_savedproduct(request, id):
    product = get_object_or_404(Product, id=id)
    saved, created = SavedProducts.objects.get_or_create(user=request.user, product=product)

    if created:
        messages.success(request, f"'{product.name}' has been added to your saved products.")
    else:
        messages.info(request, f"'{product.name}' is already in your saved products.")

    return redirect('product_detail', id=id)  # Make sure product_detail URL uses product_id


# SAVED PRODUCTS LIST
@login_required(login_url="login") 
def saved_products_list(request):
    saved_products = SavedProducts.objects.filter(user=request.user).select_related('product')
    context = {'saved_products': saved_products}
    return render(request, 'saved_products.html', context)


# REMOVE SAVED PRODUCT
@login_required(login_url="login") 
def remove_savedproduct(request, id):
    product = get_object_or_404(Product, id=id)
    SavedProducts.objects.filter(user=request.user, product=product).delete()
    messages.success(request, f"'{product.name}' has been removed from your saved products.")
    return redirect('saved_products')



# REVIEW FUNCTION
@login_required(login_url="login") 
def add_review(request, id):
    product = get_object_or_404(Product, id=id)
    
    # Prevent multiple reviews by the same user
    if Review.objects.filter(product=product, user=request.user).exists():
        messages.info(request, "You have already reviewed this product.")
        return redirect('product_detail', id=id)

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.product = product
            review.user = request.user
            review.save()
            messages.success(request, "Your review has been submitted.")
            return redirect('product_detail', id=id)
    else:
        form = ReviewForm()
            
        
    context = {'form':form, 'product':product}
    return render(request, 'add_review.html', context)

@login_required(login_url="login") 
def remove_review(request, id):
    if request.method == 'POST':
        review = get_object_or_404(Review, id=id, user=request.user)
        review.delete()
        messages.success(request, f"'{review.title}' has been deleted.")
        return redirect('product_detail', id=review.product.id)



# CART FUNCTIONS
@login_required(login_url="login")
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


@login_required(login_url="login")
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

@login_required(login_url="login")
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

@login_required(login_url="login")
def increase_quantity(request, id):
    cart, created = Cart.objects.get_or_create(customer=request.user.customer, complete=False)
    product = get_object_or_404(Product, id=id)
    item = CartItem.objects.filter(cart=cart, product=product).first()

    if item:
        item.quantity += 1
        item.save()

    return redirect('cart')

@login_required(login_url="login")
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

    context = {'cart': cart,
            'items': items,
            'shipping_address': shipping_address

            }
    return render(request, 'checkout.html', context)


@login_required(login_url="login")
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
            #messages.error(request, 'All fields are required.')
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




@login_required(login_url="login")
def edit_address(request, id):
    print("Edit address view function called")
    try:
        address = ShippingAddress.objects.get(id=id)
        print(f"Address customer: {address.customer}, Request user: {request.user}")
        if address.customer != request.user:
            print("Customer and user do not match")
            messages.error(request, 'You are not authorized to edit this address.')
            return redirect('account_detail')

        if request.method == 'POST':
            form = ShippingAddressForm(request.POST, instance=address)
            if form.is_valid():
                form.save()
                return redirect('account_detail')
        else:
            form = ShippingAddressForm(instance=address)

        context = {'address': address, 'form': form}
        return render(request, 'edit_address.html', context)
    except Exception as e:
        print(f"An error occurred: {e}")
        messages.error(request, 'An error occurred.')
        return redirect('account_detail')







# USER FUNCTIONS

@login_required(login_url="login") 
def all_customer(request):
    if not request.user.is_superuser:
        messages.error(request, 'You are not authorized to view this page.')
        return redirect('home')

    customers = Customer.objects.all()
    context = {'customers': customers}
    return render(request, 'all_customer.html', context)

@login_required(login_url="login") 
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

def staff_login(request):
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



@login_required(login_url="login") 
def orders(request):
    carts = Cart.objects.all()
    context = {'carts': carts}
    return render(request, 'orders.html', context)




def payment_success(request):
    customer = getattr(request.user, 'customer', None)
    if customer:
        cart = Cart.objects.filter(customer=customer, complete=False).first()
        if cart:
            cart.complete = True
            cart.save()
    return render(request, 'payment_success.html')


def payment_cancelled(request):
    return render(request, 'payment_cancelled.html')


def completed_order_view(request):
    if not request.user.is_authenticated:
        messages.error(request, 'You must be logged in to view your orders.')
        return redirect('login')

    # Get the latest order for this user
    order = Order.objects.filter(customer=request.user).order_by('-id').first()
    if not order:
        messages.info(request, 'You have no completed orders.')
        return render(request, 'orders_complete.html', {'order': None})

    # Get items from the related cart
    items = CartItem.objects.select_related('product').filter(cart=order.cart)

    context = {
        'order': order,
        'items': items,
        'shipping_address': order.shipping_address,
    }
    return render(request, 'orders_complete.html', context)


def all_orders(request):
    orders = Order.objects.all().order_by('-created_at')
    context = {'orders': orders}
    return render(request, 'orders.html', context)

def order_detail(request, id):
    order = get_object_or_404(Order, id=id)
    items = CartItem.objects.select_related('product').filter(cart=order.cart)
    context = {'order': order, 'items': items}
    return render(request, 'order_detail.html', context)


